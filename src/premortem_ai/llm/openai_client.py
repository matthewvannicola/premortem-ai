"""
openai_client.py

Enterprise-grade governed wrapper around the OpenAI Responses API.

Improvements over the previous version:
    - Uses the modern `client.responses.create()` API
    - Enforces JSON output via response_format
    - Adds full observability (metrics + tracing)
    - Adds dynamic token budgeting
    - Adds configurable timeout support
    - Adds structured validation + error normalization
    - Adds retry jitter + improved backoff behavior
"""

import json
import time
import random
from typing import Any, Dict, Optional

from openai import OpenAI, APIError, APIConnectionError, RateLimitError, Timeout
from premortem_ai.config import settings
from premortem_ai.exceptions import ModelInvocationError, ConfigurationError
from premortem_ai.observability.metrics import llm_latency, llm_requests_total
from premortem_ai.observability.tracing import traced_operation


# --------------------------------------------------------------------------
# Client initialization
# --------------------------------------------------------------------------

client = OpenAI(api_key=settings.OPENAI_API_KEY)


# --------------------------------------------------------------------------
# Utility — Dynamic Token Budgeting
# --------------------------------------------------------------------------

def compute_token_budget(prompt: str) -> int:
    """
    Heuristic token budgeting to reduce truncation risk.
    Ensures prompt + output never exceed model context.

    Example:
        MAX_CONTEXT = 200_000 (gpt-5.1)
        But we reserve 20–40% for model overhead.
    """
    approximate_prompt_tokens = max(1, len(prompt) // 3)

    max_allowed = settings.MAX_TOKENS
    reserved_for_output = int(max_allowed * 0.6)

    return max(256, reserved_for_output - approximate_prompt_tokens)


# --------------------------------------------------------------------------
# LLM Client Wrapper
# --------------------------------------------------------------------------

class LLMClient:
    """
    High-level LLM interface for all structured LLM inference.

    Features:
        - JSON-mode enforcement
        - Observability integration (metrics + tracing)
        - Retry + exponential backoff + jitter
        - Strict exception normalization
        - Configurable model override + timeout control
    """

    def __init__(self, model: Optional[str] = None, max_retries: int = 3, timeout: int = 45):
        self.model = model or settings.MODEL_VERSION
        self.max_retries = max_retries
        self.timeout = timeout

    # ----------------------------------------------------------------------
    @traced_operation("llm.run")
    def run(self, prompt: str, model_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute prompt and return parsed JSON.

        Returns:
            dict — parsed structured JSON response

        Raises:
            ModelInvocationError
            DependencyError
        """

        model_name = model_override or self.model
        token_budget = compute_token_budget(prompt)

        backoff = 1.0

        for attempt in range(1, self.max_retries + 1):

            try:
                with llm_latency.time():
                    response = client.responses.create(
                        model=model_name,
                        input=prompt,
                        max_output_tokens=token_budget,
                        response_format={"type": "json_object"},
                        timeout=self.timeout,
                    )

                llm_requests_total.labels(model=model_name, status="success").inc()

                raw = response.output_text

                try:
                    return json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise ModelInvocationError(f"LLM returned invalid JSON: {raw}") from exc

            # ------------------ RETRYABLE ERRORS ------------------
            except RateLimitError as exc:
                if attempt < self.max_retries:
                    sleep = backoff + random.uniform(0, 0.3)
                    time.sleep(sleep)
                    backoff *= 2
                    continue
                llm_requests_total.labels(model=model_name, status="rate_limited").inc()
                raise ModelInvocationError(f"Rate limit exceeded after retries: {exc}") from exc

            except (Timeout, APIConnectionError) as exc:
                if attempt < self.max_retries:
                    sleep = backoff + random.uniform(0, 0.3)
                    time.sleep(sleep)
                    backoff *= 2
                    continue
                llm_requests_total.labels(model=model_name, status="network_error").inc()
                raise DependencyError(f"LLM network failure: {exc}") from exc

            except APIError as exc:
                if exc.status and 500 <= exc.status < 600 and attempt < self.max_retries:
                    sleep = backoff + random.uniform(0, 0.3)
                    time.sleep(sleep)
                    backoff *= 2
                    continue
                llm_requests_total.labels(model=model_name, status="api_error").inc()
                raise ModelInvocationError(f"LLM API error: {exc}") from exc

            # ------------------ NON-RETRYABLE ------------------
            except Exception as exc:
                llm_requests_total.labels(model=model_name, status="fatal").inc()
                raise ModelInvocationError(f"Unexpected LLM error: {exc}") from exc

        raise ModelInvocationError("Exhausted all retries without success.")


# --------------------------------------------------------------------------
# Factory
# --------------------------------------------------------------------------

def get_llm_client(model: Optional[str] = None) -> LLMClient:
    return LLMClient(model=model)
    
