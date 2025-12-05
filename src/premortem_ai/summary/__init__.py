"""
Summary domain for the PreMortem AI pipeline.

This domain synthesizes the full analytical output of earlier stages—
risks, scores, themes, and mitigations—into a concise, executive-ready
narrative summary. The summary serves as the high-level interpretation
layer for strategic stakeholders, enabling rapid understanding of the
most critical project concerns.

Core responsibilities:
    - Interpret aggregated risk + severity signals
    - Highlight systemic patterns from the Themes stage
    - Summarize recommended mitigations at a strategic level
    - Produce schema-aligned summary artifacts for downstream reporting
"""

from .summary_builder import run_summary

__all__ = [
    "run_summary",
]
