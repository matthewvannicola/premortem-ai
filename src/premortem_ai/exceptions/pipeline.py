"""
exceptions/pipeline.py

Exceptions related to pipeline execution failures.
"""

from __future__ import annotations

from .base import PremortemException


class PipelineExecutionError(PremortemException):
    """Raised when the pipeline fails during execution."""


class PipelineStateError(PremortemException):
    """Raised when pipeline state becomes invalid or inconsistent."""
