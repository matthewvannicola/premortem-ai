"""
exceptions package export surface.

Centralizes import access for all exception types so callers can do:
    from premortem_ai.exceptions import ValidationError, ConfigurationError
"""

from .base import PremortemException
from .validation import (
    ValidationError,
    SchemaValidationError,
    CrossReferenceError,
    DataConsistencyError,
)
from .pipeline import PipelineExecutionError
from .model import ModelInvocationError
from .config import ConfigurationError

__all__ = [
    "PremortemException",
    "ValidationError",
    "SchemaValidationError",
    "CrossReferenceError",
    "DataConsistencyError",
    "PipelineExecutionError",
    "ModelInvocationError",
    "ConfigurationError",
]
