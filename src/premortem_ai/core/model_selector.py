"""
Model selection utilities for the PreMortem AI pipeline.

All LLM-dependent components must route through a single model-selection layer
to ensure consistent behavior, controlled upgrades, and auditability.

Design Features:
- Centralized configuration for default and fallback models.
- Environment-variable overrides for deployment environments.
- Deterministic selection logic to avoid unexpected drift.
- Human-readable errors when an unsupported model is requested.
"""

import os
from typing import Optional


# Supported / approved model identifiers.
SUPPORTED_MODELS = {
    "gpt-5.1",
    "gpt-4.1",
    "gpt-4.1-mini",
}


# System defaults — enterprise-friendly and easy to override via env vars.
DEFAULT_MODEL = os.getenv("PREMORTEM_MODEL", "gpt-5.1")
FALLBACK_MODEL = os.getenv("PREMORTEM_MODEL_FALLBACK", "gpt-4.1")


class ModelSelectionError(Exception):
    """Raised when an invalid or unsupported model identifier is requested."""


def _validate_model(model: str) -> None:
    """Internal helper to enforce model contracts."""
    if model not in SUPPORTED_MODELS:
        raise ModelSelectionError(
            f"Unsupported model '{model}'. Supported: {sorted(SUPPORTED_MODELS)}"
        )


def select_model(preferred: Optional[str] = None) -> str:
    """
    Select a valid model using a predictable, auditable strategy.

    Selection order:
        1. Explicitly requested model (if valid)
        2. System default model (env override or DEFAULT_MODEL)
        3. Fallback model (env override or FALLBACK_MODEL)

    Args:
        preferred (str | None): Explicitly requested model from a pipeline stage.

    Returns:
        str: A validated model identifier suitable for LLM inference.
    """

    # Case 1: A component explicitly requested a model
    if preferred:
        try:
            _validate_model(preferred)
            return preferred
        except ModelSelectionError:
            # Fall through to default → fallback
            pass

    # Case 2: Try system default
    try:
        _validate_model(DEFAULT_MODEL)
        return DEFAULT_MODEL
    except ModelSelectionError:
        pass

    # Case 3: Use fallback (must succeed or raise)
    _validate_model(FALLBACK_MODEL)
    return FALLBACK_MODEL


__all__ = [
    "select_model",
    "ModelSelectionError",
    "SUPPORTED_MODELS",
    "DEFAULT_MODEL",
    "FALLBACK_MODEL",
]
