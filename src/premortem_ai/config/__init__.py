"""
Configuration package for PreMortem AI.

This package centralizes environment-agnostic configuration for:
    - pipeline behavior
    - model selection
    - global settings
    - environment overrides (future)
    - version governance

Public Exports:
    - settings            : global Settings instance
    - PIPELINE_CONFIG     : structured defaults used by orchestrator & service layers

Downstream modules should import from here to ensure a single source of truth:
    from premortem_ai.config import settings, PIPELINE_CONFIG
"""

from .settings import settings
from .pipeline_configs import PIPELINE_CONFIG

__all__ = [
    "settings",
    "PIPELINE_CONFIG",
]
