"""
Public scoring API for PreMortem AI.

This module exposes the high-level scoring functions used across
pipelines, services, and orchestration layers.

Internal rule engines and prompt templates remain private to maintain
a stable, governed API surface.
"""

from .severity_engine import compute_scores_for_risks
from .prompts import build_scoring_prompt

__all__ = [
    "compute_scores_for_risks",
    "build_scoring_prompt",
]
