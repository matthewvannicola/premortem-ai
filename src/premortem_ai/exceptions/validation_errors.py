"""
validation_errors.py

Validation-specific exceptions for the PreMortem AI system.

This module defines errors related to:
    - canonical model validation
    - schema alignment failures
    - cross-reference inconsistencies (e.g., missing risk_ids)
    - normalization / preprocessing constraints
    - unsafe or malformed pipeline inputs

These exceptions are intentionally kept separate from general runtime errors
to allow API / CLI / SDK layers to respond with precise error messages.
"""

from .errors import PreMortemError


class ValidationError(PreMortemError):
    """
    Base class for all validation-related issues.

    Raised when:
        - canonical models fail structural validation
        - Pydantic constraints are violated
        - pipeline inputs are malformed
        - missing required fields or unexpected shapes
    """

    pass


class SchemaValidationError(ValidationError):
    """
    Raised when a canonical model fails its JSON Schema alignment or invariants.

    Examples:
        - RiskReport references a risk_id that does not exist
        - ScoreItem severity mismatch (e.g., 4 * 5 != 18)
        - ThemeItem contains duplicate risk_ids
        - MitigationItem steps not ordered or missing fields
    """

    pass


class CrossReferenceError(ValidationError):
    """
    Raised when linked objects reference each other incorrectly.

    Examples:
        - ScoreItem references unknown risk_id
        - MitigationItem contains invalid or missing risk references
        - Summary.top_risks references non-existent risks
    """

    pass


class NormalizationError(ValidationError):
    """
    Raised when text normalization or preprocessing detects invalid content.

    Examples:
        - unsupported characters after normalization
        - malformed unicode in project description
        - normalization pipeline failures
    """

    pass


class InputPayloadError(ValidationError):
    """
    Raised when incoming raw API/CLI payloads fail initial validation before
    being parsed into PipelineRequest.

    Examples:
        - missing 'project_description'
        - non-string fields
        - negative values where positive required
    """

    pass
