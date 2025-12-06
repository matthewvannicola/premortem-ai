"""
errors.py

Defines the core exception hierarchy for the PreMortem AI system.

This module provides:
    - A structured, extensible foundation for domain-specific errors
    - Clear separation between system, pipeline, and service layer failures
    - Predictable exception types that API / CLI / SDK consumers can rely on

All exceptions here are intentionally lightweight and free of side effects.
"""


class PreMortemError(Exception):
    """
    Base error for all PreMortem AI exceptions.

    All other custom exceptions inherit from this class, making it easy for
    callers to catch *only* PreMortem-specific issues:
    
        try:
            ...
        except PreMortemError:
            handle_domain_issue()
    """

    pass


class PipelineExecutionError(PreMortemError):
    """
    Raised when a failure occurs within the pipeline orchestration process.

    Examples:
        - LLM inference errors
        - invalid intermediate structures
        - component initialization failures
        - unexpected runtime exceptions during a pipeline stage
    """

    pass


class ModelInvocationError(PreMortemError):
    """
    Raised when communication with the LLM backend fails.

    Examples:
        - timeout
        - API transport failures
        - unauthorized / invalid credentials
        - malformed response formats
    """

    pass


class ConfigurationError(PreMortemError):
    """
    Raised when required configuration is missing or invalid.

    Examples:
        - invalid pipeline version override
        - unknown model routing strategy
        - improperly formatted settings values
    """

    pass


class DependencyError(PreMortemError):
    """
    Raised when an external dependency fails.

    Examples:
        - network outages
        - missing Python packages
        - I/O or filesystem issues
        - environment misconfiguration
    """

    pass
