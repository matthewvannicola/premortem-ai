"""
errors.py

System-level and pipeline-level exceptions for PreMortem AI.
All errors derive from PreMortemError to ensure unified error handling.
"""

from .base import PreMortemError


class ConfigurationError(PreMortemError):
    """Raised when system or pipeline configuration is invalid."""
    pass


class DependencyError(PreMortemError):
    """Raised when external dependencies fail (network, providers, file systems)."""
    pass


class ModelInvocationError(PreMortemError):
    """
    Raised when an LLM invocation fails:
        • API errors
        • malformed JSON
        • hallucinated or missing fields
        • timeout or rate limit
    """
    pass


class PipelineExecutionError(PreMortemError):
    """Raised when a pipeline step fails unexpectedly."""
    pass


class ServiceError(PreMortemError):
    """Raised when a high-level service (analysis_service) fails execution."""
    pass


class RetryableError(PreMortemError):
    """
    Raised when a transient failure occurs that should be retried.

    Examples:
        • Rate limits
        • Temporary upstream failure
        • Network instability
    """
    pass
