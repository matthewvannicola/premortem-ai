"""
PreMortem AI – Exception Package

This package defines the full structured exception hierarchy used across
the system. All errors raised by PreMortem AI components inherit from
`PreMortemError`, allowing callers to selectively catch:

    - domain-wide errors              (PreMortemError)
    - validation issues               (ValidationError + subtypes)
    - pipeline execution failures     (PipelineExecutionError)
    - model invocation errors         (ModelInvocationError)
    - configuration and dependency    issues
    - input payload errors

Modules:
    errors.py             → Core system + pipeline exception types
    validation_errors.py  → Structural, schema, and cross-reference validation
"""

from .errors import (
    PreMortemError,
    PipelineExecutionError,
    ModelInvocationError,
    ConfigurationError,
    DependencyError,
)

from .validation_errors import (
    ValidationError,
    SchemaValidationError,
    CrossReferenceError,
    NormalizationError,
    InputPayloadError,
)

__all__ = [
    # Base root error
    "PreMortemError",

    # Execution-level errors
    "PipelineExecutionError",
    "ModelInvocationError",
    "ConfigurationError",
    "DependencyError",

    # Validation-level errors
    "ValidationError",
    "SchemaValidationError",
    "CrossReferenceError",
    "NormalizationError",
    "InputPayloadError",
]
