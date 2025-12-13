"""
settings.py

Centralized configuration for PreMortem AI.

This module:
- Loads all sensitive values from environment variables
- Provides a single, typed Settings object used by the system
- Ensures API keys are never stored in source control
"""

import os
from dataclasses import dataclass


def require_env(key: str) -> str:
    """
    Retrieve a required environment variable.
    Raises a clear error if the key is missing.
    """
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Missing required environment variable: {key}\n"
            f"Set it before running the system.\n"
        )
    return value


@dataclass
class Settings:
    """
    Strongly typed central configuration object.
    All environment-driven values flow through this class.
    """

    # -------------------------
    # API Keys
    # -------------------------
    OPENAI_API_KEY: str

    # -------------------------
    # Model Defaults
    # -------------------------
    MODEL_VERSION: str = os.getenv("MODEL_VERSION", "gpt-5.2")

    # -------------------------
    # Environment Metadata
    # -------------------------
    ENVIRONMENT: str = os.getenv("PREMORTEM_ENV", "local")
    LOG_LEVEL: str = os.getenv("PREMORTEM_LOG_LEVEL", "INFO")


# Global settings instance used across the project
settings = Settings(
    OPENAI_API_KEY=require_env("OPENAI_API_KEY"),
)
