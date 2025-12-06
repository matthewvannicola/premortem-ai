"""
exceptions package export surface.

Centralizes import access for all exception types so callers can do:
    from premortem_ai.exceptions import ValidationError, ConfigurationError
"""

from .base import PreMortemError
from .errors import (
    ConfigurationError,
    DependencyError,
    ModelInvocationError,
    PipelineExecutionError,
    ServiceError,
    RetryableError,
)
from .validation_errors import (
    ValidationError,
    SchemaValidationError,
    CrossReferenceError,
    DataConsistencyError,
)

__all__ = [
    "PreMortemError",
    "ConfigurationError",
    "DependencyError",
    "ModelInvocationError",
    "PipelineExecutionError",
    "ServiceError",
    "RetryableError",
    "ValidationError",
    "SchemaValidationError",
    "CrossReferenceError",
    "DataConsistencyError",
]
