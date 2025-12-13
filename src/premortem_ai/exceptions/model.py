"""
exceptions/model.py

Exceptions raised during model / LLM invocation.
"""

from __future__ import annotations

from .base import PremortemException


class ModelInvocationError(PremortemException):
    """
    Raised when an LLM call fails, times out, or returns invalid output.
    """
