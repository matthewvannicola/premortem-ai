"""
Mitigation domain for the PreMortem AI pipeline.

This domain generates actionable mitigation recommendations for each risk
and theme. Mitigation outputs help teams translate abstract risk insights
into concrete, practical next steps that reduce impact or likelihood.

Core responsibilities:
    - Interpret risks, themes, and severity profiles
    - Generate targeted mitigation actions using LLM guidance
    - Ensure outputs comply with the mitigation schema
    - Produce consistent, auditable mitigation objects downstream
"""

from .mitigation_engine import run_mitigation_generation

__all__ = [
    "run_mitigation_generation",
]
