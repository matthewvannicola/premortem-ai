"""
exceptions/base.py

Defines the root exception for all PreMortem AI errors.
Provides optional trace_id injection for structured logging and debugging.
"""


class PreMortemError(Exception):
    """
    Base class for all errors raised inside the PreMortem AI system.

    Supports:
        • trace_id           → enables cross-service correlation
        • message enrichment → consistent string formatting
    """

    def __init__(self, message: str, *, trace_id: str | None = None):
        super().__init__(message)
        self.trace_id = trace_id

    def __str__(self):
        base = super().__str__()
        if self.trace_id:
            return f"{base} [trace_id={self.trace_id}]"
        return base
