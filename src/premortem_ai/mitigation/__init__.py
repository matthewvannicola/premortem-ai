"""
Public API for mitigation generation.

This module exposes the high-level mitigation components used by
pipeline orchestration and reporting layers.

Internal logic, engines, and helper functions remain encapsulated
to preserve a stable, governed API surface.
"""

from .prompts import build_mitigation_prompt
from .mitigation_generator import parse_mitigation_output

__all__ = [
    "build_mitigation_prompt",
    "parse_mitigation_output",
]
