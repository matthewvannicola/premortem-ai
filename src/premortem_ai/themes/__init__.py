"""
Themes domain for the PreMortem AI pipeline.

This domain clusters individual risks into higher-level thematic groups
based on shared patterns, underlying drivers, and systemic issues.

The Themes stage is critical for:
    - Revealing macro-level problem areas
    - Improving interpretability for stakeholders
    - Providing structured input to mitigation generation
    - Enhancing summary and reporting layers

Design Principles:
    - Theme extraction is a hybrid process (LLM + deterministic grouping)
    - Outputs MUST conform to the themes schema
    - Each theme receives its own generated theme_id downstream
"""

from .theme_clusterer import run_theme_clustering

__all__ = [
    "run_theme_clustering",
]
