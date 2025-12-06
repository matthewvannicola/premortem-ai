"""
validation_errors.py

Validation-related exceptions for PreMortem AI.
Covers schema mismatches, cross-reference validation, and data integrity.
"""

from .base import PreMortemError


class ValidationError(PreMortemError):
    """General validation failure."""
    pass


class SchemaValidationError(ValidationError):
    """Raised when a payload does not conform to the expected schema."""
    pass


class CrossReferenceError(ValidationError):
    """
    Raised when identifiers reference missing or invalid objects.

    Examples:
        • score refers to nonexistent risk
        • theme references nonexistent risk
        • missing mitigation IDs
    """
    pass


class DataConsistencyError(ValidationError):
    """
    Raised when numeric or structural values are inconsistent.

    Examples:
        • invalid severity range
        • negative values where forbidden
        • unordered or duplicate identifiers
    """
    pass
