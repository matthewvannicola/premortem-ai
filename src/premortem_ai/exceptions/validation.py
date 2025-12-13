"""
exceptions/validation.py

Validation-related exceptions for PreMortem AI.

Covers:
- schema mismatches
- cross-reference validation
- data integrity and consistency errors

These errors represent deterministic, user-correctable failures.
"""

from __future__ import annotations

from .base import PremortemException


class ValidationError(PremortemException):
    """
    Base class for all validation failures.

    Raised when user-provided input or derived data
    violates expected constraints.
    """
    pass


class SchemaValidationError(ValidationError):
    """
    Raised when a payload does not conform to the expected schema.

    Examples:
        - missing required fields
        - invalid field types
        - malformed JSON structures
    """
    pass


class CrossReferenceError(ValidationError):
    """
    Raised when identifiers reference missing or invalid objects.

    Examples:
        - score refers to nonexistent risk
        - theme references nonexistent risk
        - mitigation references missing risk IDs
    """
    pass


class DataConsistencyError(ValidationError):
    """
    Raised when numeric or structural values are inconsistent.

    Examples:
        - invalid severity range
        - negative values where forbidden
        - duplicate or unordered identifiers
    """
    pass
