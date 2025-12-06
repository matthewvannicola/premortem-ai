"""
model_router.py

Enterprise-grade model routing & governance layer for PreMortem AI.

This module centralizes all logic for determining which LLM model should be used
for a given pipeline execution. It ensures:

    - Deterministic, governed model selection
    - Validation of user-provided overrides
    - Support for multi-model task segmentation
    - Config-driven model registries (future extensibility)
    - Observability hooks for invalid override attempts

This router purposely isolates model governance concerns from the OpenAI client,
orchestrators, and pipelines.
"""

from typing import Optional, List
from premortem_ai.config import settings
from premortem_ai.exceptions import ConfigurationError
from premortem_ai.observability.metrics import model_routing_total


# ---------------------------------------------------------------------------
# Model Registry — governed allowlist
# ---------------------------------------------------------------------------

def load_allowed_models() -> List[str]:
    """
    Load the allowed model registry.

    Priority:
        1. settings.ALLOWED_MODELS (if exposed for enterprise governance)
        2. Hard-coded safe defaults

    This architecture lets companies enforce governed model policies in production.
    """
    if hasattr(settings, "ALLOWED_MODELS") and settings.ALLOWED_MODELS:
        return settings.ALLOWED_MODELS

    # Safe defaults (compile-time)
    return [
        "gpt-5.1",
        "gpt-5.1-reasoning",
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4o",
    ]


ALLOWED_MODELS = load_allowed_models()


# ---------------------------------------------------------------------------
# Core Routing Logic
# ---------------------------------------------------------------------------

def resolve_model_version(override: Optional[str] = None) -> str:
    """
    Resolve a model for pipeline use.

    Routing priority:
        1. PipelineRequest.model_version_override
        2. settings.MODEL_VERSION
        3. First allowed model (governed fallback)

    Raises:
        ConfigurationError – if override is invalid or forbidden.
    """

    # ---------------------- 1. Explicit override ----------------------
    if override:
        clean = override.strip()

        if clean not in ALLOWED_MODELS:
            model_routing_total.labels(source="override", status="invalid").inc()
            raise ConfigurationError(
                f"Invalid model override '{clean}'. "
                f"Allowed models: {', '.join(ALLOWED_MODELS)}"
            )

        model_routing_total.labels(source="override", status="success").inc()
        return clean

    # ---------------------- 2. settings default -----------------------
    default_model = getattr(settings, "MODEL_VERSION", None)

    if default_model in ALLOWED_MODELS:
        model_routing_total.labels(source="settings", status="success").inc()
        return default_model

    # ---------------------- 3. Hard fallback --------------------------
    # Never break execution if settings are misconfigured.
    fallback = ALLOWED_MODELS[0]
    model_routing_total.labels(source="fallback", status="success").inc()
    return fallback


# ---------------------------------------------------------------------------
# Specialized Routing for Multi-Model Pipelines
# ---------------------------------------------------------------------------

def get_reasoning_model() -> str:
    """
    Select a model optimized for deep reasoning tasks.

    If enterprise governance or the environment removes reasoning models,
    this gracefully falls back to the primary pipeline resolver.
    """
    preferred = "gpt-5.1-reasoning"

    if preferred in ALLOWED_MODELS:
        model_routing_total.labels(source="reasoning", status="success").inc()
        return preferred

    # Fallback is not an error — just route to default
    model_routing_total.labels(source="reasoning", status="fallback").inc()
    return resolve_model_version()


def get_summarization_model() -> str:
    """
    Future use-case:
        Allows pipelines to use smaller, faster models for summarization tasks.
    """
    preferred = "gpt-4.1-mini"

    if preferred in ALLOWED_MODELS:
        model_routing_total.labels(source="summary", status="success").inc()
        return preferred

    model_routing_total.labels(source="summary", status="fallback").inc()
    return resolve_model_version()


# ---------------------------------------------------------------------------
# Validation Helper — used by orchestrators
# ---------------------------------------------------------------------------

def validate_model(model_name: str) -> None:
    """
    Validate that a model is approved for use.

    Raises:
        ConfigurationError  – if model_name is not permitted.
    """
    if model_name not in ALLOWED_MODELS:
        model_routing_total.labels(source="validate", status="invalid").inc()
        raise ConfigurationError(
            f"Model '{model_name}' is not approved. "
            f"Allowed models: {', '.join(ALLOWED_MODELS)}"
        )

    model_routing_total.labels(source="validate", status="success").inc()
