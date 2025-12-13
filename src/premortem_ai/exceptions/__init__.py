"""
premortem_ai.exceptions

Public exception surface for the PreMortem AI system.

Centralizes import access so callers can write:
    from premortem_ai.exceptions import ValidationError, ConfigurationError
"""

from .base import PremortemException
from .validation import (
    ValidationError,
    SchemaValidationError,
    CrossReferenceError,
    DataConsistencyError,
)
from .pipeline import (
    PipelineExecutionError,
    CrossReferenceError as PipelineCrossReferenceError,
)
from .model import ModelInvocationError
from .config import ConfigurationError

__all__ = [
    "PremortemException",
    "ValidationError",
    "SchemaValidationError",
    "CrossReferenceError",
    "DataConsistencyError",
    "PipelineExecutionError",
    "PipelineCrossReferenceError",
    "ModelInvocationError",
    "ConfigurationError",
]
