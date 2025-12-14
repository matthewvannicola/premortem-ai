"""
openai_client.py

Governed OpenAI client wrapper for PreMortem AI.

Responsibilities:
- Encapsulate all OpenAI SDK interactions
- Enforce a stable calling contract for pipelines
- Perform minimal, safe parsing of model output
- Surface clear, domain-agnostic errors

This module MUST NOT:
- Contain business logic
- Know about domains (discovery, scoring, etc.)
- Perform schema validation beyond basic JSON decoding
"""

import json
from typing import Any, Optional

from openai import OpenAI

from premortem_ai.config import settings
from premortem_ai.exceptions import ModelInvocationError
from premortem_ai.utils.logger import info, error


# ---------------------------------------------------------------------------
# Singleton OpenAI client
# ---------------------------------------------------------------------------

_client: Optional[OpenAI] = None


def _get_openai_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


# ---------------------------------------------------------------------------
# Public factory
# ---------------------------------------------------------------------------

def get_llm_client() -> "LLMClient":
    """
    Factory method used by all pipelines and domain services.

    Returns:
        LLMClient instance with governed execution methods
    """
    return LLMClient()


# ---------------------------------------------------------------------------
# LLM Client Abstraction
# ---------------------------------------------------------------------------

class LLMClient:
    """
    Stable LLM execution interface for PreMortem AI.

    This class intentionally exposes a SMALL surface area.
    Pipelines should never talk to OpenAI directly.
    """

    def run(self, *, prompt: str, model_override: str) -> Any:
        """
        Execute a prompt against the OpenAI API and return parsed JSON output.

        Args:
            prompt: Fully-rendered prompt string
            model_override: Fully-resolved model name (already governed)

        Returns:
            Parsed JSON output (list or dict)

        Raises:
            ModelInvocationError: On API failure or invalid JSON
        """

        info(f"Invoking LLM with model='{model_override}'")

        try:
            client = _get_openai_client()

            response = client.responses.create(
                model=model_override,
                input=prompt,
            )

            raw_text = response.output_text

        except Exception as exc:
            error(f"OpenAI invocation failed: {exc}")
            raise ModelInvocationError(
                f"OpenAI invocation failed: {exc}"
            ) from exc

        # ---------------- JSON Parsing Boundary ----------------

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as exc:
            error("LLM returned non-JSON output")
            error(f"Raw LLM output:\n{raw_text}")
            raise ModelInvocationError(
                "LLM output was not valid JSON"
            ) from exc
