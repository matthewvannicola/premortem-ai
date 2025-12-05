"""
Theme clustering engine for the PreMortem AI pipeline.

This stage groups individual risks into higher-level thematic categories
based on conceptual similarity, shared underlying causes, or systemic
patterns. Themes improve interpretability and provide structure for
downstream mitigation and summary generation.

The clustering workflow:
    1. Provide the LLM with the full set of risks
    2. Receive JSON describing the themes and associated risk_ids
    3. Normalize and sanitize LLM output
    4. Produce schema-ready theme objects
"""

from typing import List, Dict, Any

from premortem_ai.integrations.openai_client import llm_json
from premortem_ai.domains.themes.prompts import THEME_CLUSTERING_PROMPT
from premortem_ai.core.normalize_text import normalize_text


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------

def _clean_theme_item(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a single theme object returned by the LLM.

    Expected fields:
        - "name": short descriptive theme title
        - "description": short explanation of the theme
        - "risk_ids": list of associated risk identifiers
    """

    name = normalize_text(raw.get("name", ""))
    description = normalize_text(raw.get("description", ""))
    risk_ids = raw.get("risk_ids", [])

    if not isinstance(risk_ids, list):
        risk_ids = []

    return {
        "name": name.capitalize() if name else "",
        "description": description.capitalize() if description else "",
        "risk_ids": risk_ids,
    }


def _process_model_response(payload: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert LLM output into normalized schema-ready theme objects."""
    cleaned = []
    for item in payload:
        cleaned.append(_clean_theme_item(item))
    return cleaned


# ---------------------------------------------------------------------
# Public Entrypoint
# ---------------------------------------------------------------------

def run_theme_clustering(
    risks: List[Dict[str, Any]],
    scores: List[Dict[str, Any]],
    model: str
) -> List[Dict[str, Any]]:
    """
    Execute LLM-assisted theme clustering.

    Args:
        risks (list[dict]): Risk objects from discovery (with risk_id).
        scores (list[dict]): Severity scoring objects (aligned by risk_id).
        model (str): Selected LLM model identifier.

    Returns:
        list[dict]: List of theme objects (schema-ready).
    """

    # Prepare compact LLM payload
    combined_payload = [
        {
            "risk_id": r.get("risk_id"),
            "title": r.get("title"),
            "description": r.get("description"),
            "severity": next(
                (s["severity"] for s in scores if s["risk_id"] == r["risk_id"]),
                None
            ),
        }
        for r in risks
    ]

    prompt = THEME_CLUSTERING_PROMPT.format(risks=combined_payload)

    raw_output = llm_json(
        prompt=prompt,
        model=model,
        response_format="list"
    )

    if not isinstance(raw_output, list):
        raise ValueError("Theme clustering expected a JSON list of theme objects.")

    return _process_model_response(raw_output)


__all__ = ["run_theme_clustering"]
