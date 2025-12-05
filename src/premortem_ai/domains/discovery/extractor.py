"""
Risk discovery engine for the PreMortem AI pipeline.

This module extracts raw risks from the project description using
LLM-assisted analysis. It is the first and most critical domain stage,
as all downstream scoring, theming, and mitigation depend on the
quality and structure of the discovered risks.

Responsibilities:
    - Prepare the discovery prompt
    - Call the model through the integrations layer
    - Normalize and clean raw LLM output
    - Ensure each item contains basic required fields
"""

from typing import List, Dict, Any

from premortem_ai.integrations.openai_client import llm_json
from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.domains.discovery.prompts import DISCOVERY_PROMPT


# ---------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------

def _clean_risk_item(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize and sanitize a single raw risk item to ensure predictable structure.

    Expected raw fields from the LLM:
        - "title"
        - "description"

    Additional fields (IDs, scoring, etc.) will be added downstream.
    """

    title = normalize_text(raw.get("title", ""))
    description = normalize_text(raw.get("description", ""))

    return {
        "title": title,
        "description": description,
    }


def _process_model_response(payload: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert the model's raw output into clean, schema-ready risk items.
    """

    cleaned = []
    for item in payload:
        cleaned.append(_clean_risk_item(item))
    return cleaned


# ---------------------------------------------------------------------
# Public Entrypoint
# ---------------------------------------------------------------------

def run_discovery(project_description: str, model: str) -> List[Dict[str, Any]]:
    """
    Execute the risk discovery stage.

    Args:
        project_description (str): Raw user/system input describing the project.
        model (str): Selected model identifier from the orchestrator.

    Returns:
        list[dict]: A list of cleaned risk items, suitable for schema validation.
    """

    prompt = DISCOVERY_PROMPT.format(description=project_description)

    # LLM call is delegated to the integrations layer.
    raw_output = llm_json(
        prompt=prompt,
        model=model,
        response_format="list",  # Expecting a list of JSON objects
    )

    if not isinstance(raw_output, list):
        raise ValueError("Discovery step expected the model to return a list of objects.")

    return _process_model_response(raw_output)


__all__ = ["run_discovery"]
