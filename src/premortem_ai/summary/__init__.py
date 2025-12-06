"""
Public API for executive summary generation.

This module exposes stable, high-level functions for building
summary prompts, invoking the LLM, and parsing summary results.

Internal utilities remain encapsulated to preserve a clean,
governed API surface for the pipeline and service layers.
"""

from .prompts import build_summary_prompt
from .summary_generator import parse_summary_output
from .summary_builder import run_summary

__all__ = [
    "build_summary_prompt",
    "parse_summary_output",
    "run_summary",
]
