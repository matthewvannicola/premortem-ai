"""
Deterministic rule-based scoring for the PreMortem AI pipeline.

This module provides baseline severity signals using transparent,
auditable heuristics. These rules complement LLM scoring by offering:
    - Repeatability across runs
    - Explainable logic suitable for governance
    - A stable baseline that reduces model variance

Rule-based scoring does NOT attempt to fully evaluate risk context — that
is handled by the LLM — but rather provides predictable anchors for the
final hybrid scoring model.
"""

from typing import Dict, Any
from premortem_ai.core.normalize_text import normalize_text


# ---------------------------------------------------------------------
# Internal Heuristic Rules
# ---------------------------------------------------------------------

KEYWORD_WEIGHTS = {
    "failure": 2,
    "delay": 2,
    "security": 3,
    "outage": 3,
    "dependency": 1,
    "integration": 1,
    "resource": 1,
    "budget": 2,
    "quality": 2,
    "scalability": 1,
}


def _keyword_score(text: str) -> int:
    """
    Score a piece of text based on weighted keyword presence.
    """

    text = normalize_text(text)
    score = 0

    for keyword, weight in KEYWORD_WEIGHTS.items():
        if keyword in text:
            score += weight

    return min(score, 10)  # cap for stability


def _length_score(description: str) -> int:
    """
    Estimate impact/likelihood using description clarity and length.
    Longer descriptions usually indicate more complexity or ambiguity.
    """

    length = len(description.split())
    if length > 40:
        return 4
    if length > 25:
        return 3
    if length > 10:
        return 2
    return 1


# ---------------------------------------------------------------------
# Public Rule Engine
# ---------------------------------------------------------------------

def rule_based_score(risk: Dict[str, Any]) -> Dict[str, int]:
    """
    Compute deterministic rule-based severity signals.

    Returns:
        {
            "likelihood": <0–10>,
            "impact": <0–10>,
            "rationale": "deterministic rationale text"
        }
    """

    title = risk.get("title", "")
    description = risk.get("description", "")

    kw_score = _keyword_score(title + " " + description)
    length_sig = _length_score(description)

    # Simple weighted model (tuned for clarity + auditability)
    likelihood = min(10, kw_score + length_sig)
    impact = min(10, kw_score + (length_sig * 2))

    rationale = (
        f"Rule-based scoring applied: keyword_score={kw_score}, "
        f"description_length_signal={length_sig}."
    )

    return {
        "likelihood": likelihood,
        "impact": impact,
        "rationale": rationale,
    }


__all__ = ["rule_based_score"]
