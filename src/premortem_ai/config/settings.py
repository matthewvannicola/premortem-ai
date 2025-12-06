"""
settings.py

Centralized, immutable configuration state for the PreMortem AI system.
This module governs all default behaviors, including:

    - LLM model versioning
    - timeouts and retry policies
    - domain-level risk/theme/mitigation settings
    - tracing, metrics, and logging behavior
    - global pipeline defaults

All values may be overridden with environment variables,
ensuring production-safe configuration surfaces.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # -------------------------------------------------------------
    # LLM Model Configuration
    # -------------------------------------------------------------
    DEFAULT_MODEL: str = "gpt-5.1"

    # Canonical model version used by the model_router and LLM client
    MODEL_VERSION: str = os.getenv("PREMORTEM_MODEL_VERSION", "gpt-5.1")

    # Timeout for LLM calls (seconds)
    MODEL_TIMEOUT_SECONDS: int = int(os.getenv("PREMORTEM_MODEL_TIMEOUT", 30))

    # -------------------------------------------------------------
    # Risk Discovery Defaults
    # -------------------------------------------------------------
    DEFAULT_MAX_RISKS: int = int(os.getenv("PREMORTEM_MAX_RISKS", 50))

    # Risk clustering / latent structure options
    ENABLE_LATENT_THEME_INFERENCE: bool = (
        os.getenv("PREMORTEM_ENABLE_LATENT_THEMES", "false").lower() == "true"
    )

    # -------------------------------------------------------------
    # Scoring Defaults
    # -------------------------------------------------------------
    DEFAULT_SCORE_MODEL: str = os.getenv(
        "PREMORTEM_SCORE_MODEL", "gpt-5.1-reasoning"
    )

    # Number of 1–5 scale buckets used for risk scoring
    SCORE_BUCKETS: int = int(os.getenv("PREMORTEM_SCORE_BUCKETS", 5))

    # -------------------------------------------------------------
    # Mitigation Defaults
    # -------------------------------------------------------------
    MAX_MITIGATIONS_PER_RISK: int = int(
        os.getenv("PREMORTEM_MAX_MITIGATIONS_PER_RISK", 3)
    )

    # -------------------------------------------------------------
    # Summary Defaults
    # -------------------------------------------------------------
    ENABLE_SUMMARY: bool = (
        os.getenv("PREMORTEM_ENABLE_SUMMARY", "true").lower() == "true"
    )

    # -------------------------------------------------------------
    # Observability
    # -------------------------------------------------------------
    ENABLE_TRACING: bool = (
        os.getenv("PREMORTEM_ENABLE_TRACING", "false").lower() == "true"
    )

    ENABLE_METRICS: bool = (
        os.getenv("PREMORTEM_ENABLE_METRICS", "false").lower() == "true"
    )

    LOG_LEVEL: str = os.getenv("PREMORTEM_LOG_LEVEL", "INFO")

    # -------------------------------------------------------------
    # Pipeline Defaults
    # -------------------------------------------------------------
    PIPELINE_VERSION: str = os.getenv("PREMORTEM_PIPELINE_VERSION", "v1")

    INCLUDE_METADATA_IN_RESPONSE: bool = (
        os.getenv("PREMORTEM_INCLUDE_METADATA", "true").lower() == "true"
    )


# -----------------------------------------------------------------
# Global Settings Instance (Singleton Pattern)
# -----------------------------------------------------------------

settings = Settings()
