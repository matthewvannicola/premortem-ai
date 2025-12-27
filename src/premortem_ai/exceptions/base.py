"""
exceptions/base.py

Root exception for all PreMortem AI errors.

Supports optional `trace_id` injection for structured logging and debugging.
"""

from __future__ import annotations


class PremortemException(Exception):
    """
    Base class for all errors raised inside the PreMortem AI system.

    Supports:
        - trace_id: enables cross-service correlation
        - consistent string formatting for safe surfacing
    """

    def __init__(self, message: str, *, trace_id: str | None = None):
        super().__init__(message)
        self.trace_id = trace_id

    def __str__(self) -> str:
        base = super().__str__()
        if self.trace_id:
            return f"{base} [trace_id={self.trace_id}]"
        return base
