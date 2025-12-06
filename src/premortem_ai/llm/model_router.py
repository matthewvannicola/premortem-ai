"""
model_router.py

Centralized logic for selecting which LLM model to use for a given pipeline
execution. Ensures deterministic, governed model routing across the system.

Responsibilities:
    - Determine default model from global settings
    - Apply user-provided overrides (PipelineRequest.model_version_override)
    - Validate model names against an approved allowlist
    - Provide future extensibility for multi-model strategies (e.g., scoring model,
      expansion model, reasoning model, PDF model, etc.)
"""

from typing import Optional, List
from premortem_ai.config import settings
from premortem_ai.exceptions import ConfigurationError


# ---------------------------------------------------------------------------
# Approved or supported model list for governance
# ---------------------------------------------------------------------------

ALLOWED_MODELS: List[str] = [
    "gpt-5.1",
    "gpt-5.1-reasoning",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4o",
]


# ---------------------------------------------------------------------------
# Routing Logic
# ---------------------------------------------------------------------------

def resolve_model_version(override: Optional[str] = None) -> str:
    """
    Determine the correct LLM model to use.

    Priority:
        1. PipelineRequest.model_version_override (if provided)
        2. settings.MODEL_VERSION
        3. Hard fallback to the first allowed model (never happens in practice)

    Args:
        override: Optional model override from a PipelineRequest.

    Returns:
        str: Validated model name.

    Raises:
        ConfigurationError: If override is invalid.
    """

    # 1. If override provided, validate and return
    if override:
        clean = override.strip()
        if clean not in ALLOWED_MODELS:
            raise ConfigurationError(
                f"Invalid model override '{clean}'. "
                f"Allowed models: {', '.join(ALLOWED_MODELS)}"
            )
        return clean

    # 2. Apply default from settings
    if settings.MODEL_VERSION in ALLOWED_MODELS:
        return settings.MODEL_VERSION

    # 3. Fallback: safe default
    return ALLOWED_MODELS[0]


# ---------------------------------------------------------------------------
# Specialized future routing (optional extensibility)
# ---------------------------------------------------------------------------

def get_reasoning_model() -> str:
    """
    Alternate routing for reasoning-intensive tasks.

    Useful if you later separate:
        - risk discovery model
        - scoring model
        - summarization model

    Currently returns a pre-approved reasoning model or falls back gracefully.
    """
    preferred = "gpt-5.1-reasoning"

    if preferred in ALLOWED_MODELS:
        return preferred

    return resolve_model_version()  # fallback


def validate_model(model_name: str) -> None:
    """
    Explicit validation helper for orchestrator and service layers.

    Raises:
        ConfigurationError if model is not allowed.
    """
    if model_name not in ALLOWED_MODELS:
        raise ConfigurationError(
            f"Model '{model_name}' is not approved. Allowed models: {ALLOWED_MODELS}"
        )
