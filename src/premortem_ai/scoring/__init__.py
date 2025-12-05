"""
Scoring domain for the PreMortem AI pipeline.

This domain is responsible for evaluating risk severity using a hybrid
approach that combines deterministic scoring rules with LLM-assisted
judgment signals. The scoring stage enriches each risk with structured
metrics that downstream components (themes, mitigation, summary, reporting)
depend on.

Core responsibilities:
    - Apply deterministic severity rules
    - Invoke LLM scoring where needed for depth/nuance
    - Aggregate results into a final severity profile per risk
    - Produce schema-aligned structured scoring output
"""

from .severity_engine import run_scoring

__all__ = [
    "run_scoring",
]
