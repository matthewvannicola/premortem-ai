"""
settings.py

Global configuration object for PreMortem AI.

This module centralizes:
    - default model versions
    - pipeline versioning
    - global feature toggles
    - environment-aware overrides (future)
    - logging levels

All downstream modules should import from this file through:
    from premortem_ai.config import settings
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """
    Immutable settings object containing global configuration defaults.

    Over time this class can evolve to support:
        - environment variable overrides
        - dynamic backend selection (OpenAI, Azure, Anthropic)
        - feature flags
        - per-environment config files
    """

    # ----------------------------------------------------------------------
    # LLM Model Configuration
    # ----------------------------------------------------------------------
    DEFAULT_MODEL: str = "gpt-5.1"
    MODEL_TIMEOUT_SECONDS: int = 30

    # ----------------------------------------------------------------------
    # Pipeline Versioning
    # ----------------------------------------------------------------------
    DEFAULT_PIPELINE_VERSION: str = "v1.0.0"

    # ----------------------------------------------------------------------
    # Logging + Diagnostics
    # ----------------------------------------------------------------------
    LOG_LEVEL: str = "INFO"
    ENABLE_TRACING: bool = False
    ENABLE_METRICS: bool = False

    # ----------------------------------------------------------------------
    # Discovery / Scoring / Mitigation Defaults
    # ----------------------------------------------------------------------
    DEFAULT_MAX_RISKS: int = 50

    # Future fields might include:
    #   ENABLE_THEMES: bool
    #   ENABLE_MITIGATIONS: bool
    #   DEFAULT_SEVERITY_MODEL: str
    #   DEFAULT_CLUSTERING_STRATEGY: str


# Singleton instance used globally across the system
settings = Settings()
