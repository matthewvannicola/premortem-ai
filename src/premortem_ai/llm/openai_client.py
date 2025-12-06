"""
openai_client.py

Thin, governed wrapper around the OpenAI API used by PreMortem AI.

Responsibilities:
    - Provide a stable interface for LLM inference
    - Normalize API errors into domain-specific exceptions
    - Centralize model routing (settings.MODEL_VERSION, overrides, etc.)
    - Provide retry and backoff logic for improved resiliency
    - Keep dependencies isolated so the rest of the system stays portable

This module is intentionally minimal but enterprise-ready.
"""

import time
from typing import Dict, Any, Optional

from openai import OpenAI, APIError, APIConnectionError, RateLimitError, Timeout
from premortem_ai.config import settings
from premortem_ai.exceptions import (
    ModelInvocationError,
    DependencyError,
)

# ------------------------------------------------------------------------------
# Client Initialization
# ------------------------------------------------------------------------------

_client = OpenAI(api_key=settings.OPENAI_API_KEY)


# ------------------------------------------------------------------------------
# LLM Client Wrapper
# ------------------------------------------------------------------------------

class LLMClient:
    """
    High-level LLM interface used by the orchestrator and analysis service.

    Provides:
        - deterministic model selection
        - retry/backoff behavior
        - structured output formatting
        - consistent exception handling

    This wrapper ensures the rest of the codebase never imports raw OpenAI
    client calls directly.
    """

    def __init__(self, model: Optional[str] = None, max_retries: int = 3):
        self.model = model or settings.MODEL_VERSION
        self.max_retries = max_retries

    # --------------------------------------------------------------------------
    # Unified text completion / response API
    # --------------------------------------------------------------------------
    def run(self, prompt: str, model_override: Optional[str] = None) -> str:
        """
        Execute a prompt against the model and return raw text.

        Args:
            prompt (str): Normalized LLM prompt.
            model_override (Optional[str]): Optional temporary model version.

        Returns:
            str: Raw LLM response text.

        Raises:
            ModelInvocationError: For any LLM-related issues.
            DependencyError: For network/transport/runtime failures.
        """

        model_name = model_override or self.model

        backoff = 1.0
        for attempt in range(1, self.max_retries + 1):
            try:
                response = _client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=settings.MAX_TOKENS,
                    temperature=settings.TEMPERATURE,
                )

                # Standard OpenAI response normalization
                return response.choices[0].message["content"].strip()

            except RateLimitError as exc:
                # Retry on rate limits
                if attempt < self.max_retries:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                raise ModelInvocationError(f"Rate limit exceeded: {exc}") from exc

            except (Timeout, APIConnectionError) as exc:
                # Retry transient connection problems
                if attempt < self.max_retries:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                raise DependencyError(f"LLM network failure: {exc}") from exc

            except APIError as exc:
                # Transient API errors with HTTP 5xx may be retried
                if exc.status and 500 <= exc.status < 600 and attempt < self.max_retries:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                raise ModelInvocationError(f"LLM API error: {exc}") from exc

            except Exception as exc:
                raise ModelInvocationError(f"Unexpected LLM invocation error: {exc}") from exc

        # Should never reach here
        raise ModelInvocationError("Exhausted LLM retry attempts with no success.")


# ------------------------------------------------------------------------------
# Factory for DI or multi-model scenarios
# ------------------------------------------------------------------------------

def get_llm_client(model: Optional[str] = None) -> LLMClient:
    """
    Factory used by:
        - orchestrator
        - analysis service
        - CLI/runtime utilities

    Provides:
        - default model routing
        - override support
        - explicit dependency injection for tests
    """
    return LLMClient(model=model)
