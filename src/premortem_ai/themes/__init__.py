"""
Public API for theme clustering.

This module exposes the high-level theme generation utilities used by
pipeline orchestration, services, and downstream reporting layers.

Internal clustering logic and prompt construction remain encapsulated
to provide a stable, versioned contract.
"""

from .prompts import build_theme_prompt
from .theme_clusterer import parse_theme_output

__all__ = [
    "build_theme_prompt",
    "parse_theme_output",
]
