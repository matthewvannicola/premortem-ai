"""
Severity scoring engine for the PreMortem AI pipeline.

This domain stage enriches each discovered risk with a structured severity
profile using a hybrid method:
    1. Deterministic rule-based scoring (repeatable, testable)
    2. LLM-assisted scoring for contextual nuance
    3. Aggregation of rule-based and LLM scores into a final severity value

Scoring output structure (per risk):
{
    "risk_id": "...",
    "likelihood": <0–10>,
    "impact": <0–10>,
    "severity": <0–10>,
    "rationale": "short explanation"
}

This structured output feeds directly into the Themes and Mitigation stages.
"""

from typing import List, Dict, Any

from premortem_ai.integrations.openai_client import llm_json
from premortem_ai.domains.scoring.severity_rules import rule_based_score
from premortem_ai.domains.scoring.aggregator import aggregate_scores
from premortem_ai.domains.scoring.prompts import SCORING_PROMPT


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------

def _prepare_scoring_prompt(risk: Dict[str, Any]) -> str:
    """Format the scoring prompt for a specific risk."""
    return SCORING_PROMPT.format(
        title=risk.get("title", ""),
        description=risk.get("description", "")
    )


def _llm_score(risk: Dict[str, Any], model: str) -> Dict[str, Any]:
    """
    Call the LLM to generate contextual scoring signals.
    Expected output shape:
    {
        "likelihood": number,
        "impact": number,
        "rationale": "..."
    }
    """
    prompt = _prepare_scoring_prompt(risk)

    llm_result = llm_json(
        prompt=prompt,
        model=model,
        response_format="object"
    )

    if not isinstance(llm_result, dict):
        raise ValueError("LLM scoring response must be a JSON object.")

    return {
        "likelihood": llm_result.get("likelihood", 0),
        "impact": llm_result.get("impact", 0),
        "rationale": llm_result.get("rationale", "").strip(),
    }


# ---------------------------------------------------------------------
# Public Entrypoint
# ---------------------------------------------------------------------

def run_scoring(risks: List[Dict[str, Any]], model: str) -> List[Dict[str, Any]]:
    """
    Execute the risk scoring stage.

    Args:
        risks (list[dict]): Normalized risks from the discovery stage.
        model (str): Selected LLM model identifier.

    Returns:
        list[dict]: A list of scoring objects aligned with the scoring schema.
    """

    scored = []

    for risk in risks:
        # 1. Deterministic rule-based scoring
        rule_scores = rule_based_score(risk)

        # 2. LLM contextual scoring
        llm_scores = _llm_score(risk, model=model)

        # 3. Aggregate both into a final severity profile
        final_scores = aggregate_scores(rule_scores, llm_scores)

        scored.append(
            {
                "risk_id": risk.get("risk_id"),
                "likelihood": final_scores["likelihood"],
                "impact": final_scores["impact"],
                "severity": final_scores["severity"],
                "rationale": final_scores["rationale"],
            }
        )

    return scored


__all__ = ["run_scoring"]
