"""
severity_engine.py

Core scoring engine for PreMortem AI.

Responsible for:
    • Applying severity rules (likelihood × impact)
    • Validating LLM scoring outputs
    • Providing deterministic fallback scoring
    • Constructing ScoreItem objects
    • Ensuring compatibility with RiskItem and domain models
"""

from typing import Optional, Dict, Any

from premortem_ai.models import ScoreItem
from premortem_ai.exceptions import ValidationError, ModelInvocationError
from premortem_ai.core.logger import info, warning, error

from .severity_rules import (
    compute_severity_score,
    resolve_likelihood,
    resolve_impact,
    fallback_score,
)


# ----------------------------------------------------------------------
# LLM SCORING PARSE LOGIC
# ----------------------------------------------------------------------

def parse_llm_scoring_output(risk_id: str, llm_output: Dict[str, Any]) -> ScoreItem:
    """
    Parse an LLM scoring response and convert it into a ScoreItem.

    Expected LLM output schema (validated upstream):
        {
            "risk_id": "risk-00001",
            "likelihood": "high",
            "impact": "critical"
        }
    """

    try:
        raw_likelihood = llm_output.get("likelihood")
        raw_impact = llm_output.get("impact")

        if raw_likelihood is None or raw_impact is None:
            raise ValidationError(
                f"LLM scoring output for risk {risk_id} is missing likelihood or impact."
            )

        likelihood = resolve_likelihood(raw_likelihood)
        impact = resolve_impact(raw_impact)

        severity = compute_severity_score(likelihood, impact)

        return ScoreItem(
            risk_id=risk_id,
            likelihood=likelihood,
            impact=impact,
            severity=severity,
        )

    except ValidationError as e:
        # LLM output invalid → fall back to deterministic scoring
        warning(
            f"Invalid LLM scoring output for risk {risk_id}: {e}. "
            "Falling back to system default scoring."
        )
        return fallback_score_item(risk_id)

    except Exception as e:
        # Unknown error → escalate
        error(f"Unexpected scoring error for risk {risk_id}: {e}")
        raise ModelInvocationError(
            f"Unexpected scoring failure for risk {risk_id}: {e}"
        )


# ----------------------------------------------------------------------
# FALLBACK SCORING
# ----------------------------------------------------------------------

def fallback_score_item(risk_id: str) -> ScoreItem:
    """
    Deterministic fallback scoring for when LLM scoring is unavailable
    or invalid.
    """

    severity = fallback_score()
    return ScoreItem(
        risk_id=risk_id,
        likelihood=3,
        impact=3,
        severity=severity,
    )


# ----------------------------------------------------------------------
# BULK SCORING FOR PIPELINES
# ----------------------------------------------------------------------

def compute_scores_for_risks(
    risks: Dict[str, Any], llm_scores: Optional[Dict[str, Any]] = None
) -> Dict[str, ScoreItem]:
    """
    Compute scores for a batch of risks.

    Args:
        risks: Dict of risk_id -> RiskItem
        llm_scores: Dict of risk_id -> LLM scoring JSON

    Returns:
        Dict[str, ScoreItem]: All scored risks
    """

    results: Dict[str, ScoreItem] = {}

    for risk_id, risk_item in risks.items():
        llm_score_data = llm_scores.get(risk_id) if llm_scores else None

        if llm_score_data:
            score_item = parse_llm_scoring_output(risk_id, llm_score_data)
        else:
            warning(f"No LLM scoring provided for {risk_id}. Using fallback scoring.")
            score_item = fallback_score_item(risk_id)

        results[risk_id] = score_item

    info(f"Computed severity scores for {len(results)} risks.")
    return results
