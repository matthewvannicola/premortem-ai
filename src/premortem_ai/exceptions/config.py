"""
exceptions/config.py

Configuration-related errors for PreMortem AI.
"""

from __future__ import annotations

from .base import PremortemException


class ConfigurationError(PremortemException):
    """
    Raised when required configuration is missing or invalid.

    Examples:
        - missing environment variables
        - invalid model configuration
        - unsupported runtime settings
    """
