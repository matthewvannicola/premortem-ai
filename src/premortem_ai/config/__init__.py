"""
Public configuration interface for the PreMortem AI system.

Provides:
    - settings: system-wide immutable configuration
    - PIPELINE_CONFIG: tunable execution configuration for pipeline stages
"""

from .settings import settings
from .pipeline_configs import PIPELINE_CONFIG

__all__ = ["settings", "PIPELINE_CONFIG"]
