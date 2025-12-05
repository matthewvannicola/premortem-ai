"""
Mitigation generation engine for the PreMortem AI pipeline.

This module produces targeted, actionable mitigation recommendations for
each risk by combining:
    - the risk description
    - severity scoring outputs
    - thematic context (optional)
    - structured LLM guidance

Mitigation outputs must be concrete, practical, and aligned with the
governance and project-risk frameworks used in enterprise delivery.
"""

from typing import List, Dict, Any

from premortem_ai.integrations.openai_client import llm_json
from premortem_ai.domains.mitigation.prompts import MITIGATION_PROMPT
from premortem_ai.core.normalize_text import normalize_text


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------

def _clean_mitigation_item(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a mitigation recommendation returned by the LLM.

    Expected fields:
        - "risk_id": ID of the risk being mitigated
        - "actions": list of concrete mitigation steps
        - "rationale": short explanation for the recommendation
    """

    risk_id = raw.get("risk_id")
    actions = raw.get("actions", [])
    rationale = normalize_text(raw.get("rationale", ""))

    if not isinstance(actions, list):
        actions = []

    # Normalize each action
    actions = [normalize_text(a).capitalize() for a in actions if isinstance(a, str)]

    return {
        "risk_id": risk_id,
        "actions": actions,
        "rationale": rationale.capitalize() if rationale else "",
    }


def _process_model_response(payload: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert raw LLM mitigation list into normalized mitigation objects."""
    cleaned = []
    for item in payload:
        cleaned.append(_clean_mitigation_item(item))
    return cleaned


# ---------------------------------------------------------------------
# Public Entrypoint
# ---------------------------------------------------------------------

def run_mitigation_generation(
    risks: List[Dict[str, Any]],
    scores: List[Dict[str, Any]],
    themes: List[Dict[str, Any]] = None,
    model: str = "gpt-4.1"
) -> List[Dict[str, Any]]:
    """
    Generate mitigation recommendations for each individual risk.

    Args:
        risks (list[dict]): Risk objects (risk_id, title, description)
        scores (list[dict]): Severity scoring results aligned by risk_id
        themes (list[dict] or None): Optional theme context
        model (str): Model identifier for LLM inference

    Returns:
        list[dict]: Schema-ready mitigation recommendation objects.
    """

    # Prepare unified LLM payload per risk
    combined_payload = []
    for r in risks:
        rid = r["risk_id"]
        severity = next((s for s in scores if s["risk_id"] == rid), None)

        if severity is None:
            raise ValueError(f"No severity score found for risk_id {rid}")

        theme_ids = []
        if themes:
            for t in themes:
                if rid in t.get("risk_ids", []):
                    theme_ids.append(t.get("name"))

        combined_payload.append({
            "risk_id": rid,
            "title": r["title"],
            "description": r["description"],
            "severity": severity["severity"],
            "themes": theme_ids,
        })

    prompt = MITIGATION_PROMPT.format(risks=combined_payload)

    raw_output = llm_json(
        prompt=prompt,
        model=model,
        response_format="list"
    )

    if not isinstance(raw_output, list):
        raise ValueError("Mitigation generation expected a JSON list of mitigation objects.")

    return _process_model_response(raw_output)


__all__ = ["run_mitigation_generation"]
