"""
Score aggregation utilities for the PreMortem AI pipeline.

This module merges deterministic rule-based scores with LLM-assisted
contextual scores into a final severity profile.

Aggregation Goals:
    - Balance repeatability (rules) with nuance (LLM)
    - Maintain a transparent weighting strategy suitable for governance
    - Produce stable 0–10 scores aligned with the scoring schema
    - Provide a rationale that explains how the final score was formed
"""

from typing import Dict


# ---------------------------------------------------------------------
# Aggregation Weights
# ---------------------------------------------------------------------
# These weights can be tuned over time; they remain constant by default
# to ensure predictable behavior across client environments.
RULE_WEIGHT = 0.5
LLM_WEIGHT = 0.5


# ---------------------------------------------------------------------
# Public Aggregation Logic
# ---------------------------------------------------------------------

def aggregate_scores(rule_scores: Dict, llm_scores: Dict) -> Dict:
    """
    Merge rule-based and LLM scores into a final severity profile.

    Args:
        rule_scores (dict): Output from rule_based_score()
        llm_scores (dict): Output from _llm_score()

    Returns:
        dict:
        {
            "likelihood": <0–10>,
            "impact": <0–10>,
            "severity": <0–10>,
            "rationale": "combined explanation"
        }
    """

    # Weighted likelihood
    likelihood = (
        (rule_scores.get("likelihood", 0) * RULE_WEIGHT)
        + (llm_scores.get("likelihood", 0) * LLM_WEIGHT)
    )

    # Weighted impact
    impact = (
        (rule_scores.get("impact", 0) * RULE_WEIGHT)
        + (llm_scores.get("impact", 0) * LLM_WEIGHT)
    )

    # Severity as combined normalized value
    severity = (likelihood + impact) / 2

    # Ensure scoring remains within schema-safe bounds
    likelihood = min(max(round(likelihood), 0), 10)
    impact = min(max(round(impact), 0), 10)
    severity = min(max(round(severity), 0), 10)

    # Combined rationale for auditability
    rationale = (
        f"Hybrid scoring applied: "
        f"rule_likelihood={rule_scores.get('likelihood')}, "
        f"llm_likelihood={llm_scores.get('likelihood')}, "
        f"rule_impact={rule_scores.get('impact')}, "
        f"llm_impact={llm_scores.get('impact')}. "
        f"Final severity={severity}."
    )

    return {
        "likelihood": likelihood,
        "impact": impact,
        "severity": severity,
        "rationale": rationale,
    }


__all__ = ["aggregate_scores"]
