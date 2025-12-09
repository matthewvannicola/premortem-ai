"""
discovery_engine.py

Enterprise-grade risk discovery engine for the PreMortem AI pipeline.
Uses governed LLMClient + strict JSON parsing to extract structured risks.
"""

from typing import Dict
from premortem_ai.llm import get_llm_client, resolve_model_version
from premortem_ai.domains.discovery.prompts import DISCOVERY_PROMPT
from premortem_ai.domains.discovery.formatting import apply_risk_formatting
from premortem_ai.models import RiskItem
from premortem_ai.core.id_generation import generate_risk_id
from premortem_ai.exceptions import ModelInvocationError, ValidationError
from premortem_ai.utils.logger import info, error


# ---------------------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------------------

def _validate_item(item: dict) -> None:
    """Ensure required fields exist."""
    if "title" not in item or "description" not in item:
        raise ValidationError(
            f"Risk item missing required fields: {item}"
        )


def _convert_to_models(risks: list) -> Dict[str, RiskItem]:
    """Convert cleaned risks into RiskItem models with generated IDs."""
    results = {}

    for raw in risks:
        rid = generate_risk_id()
        results[rid] = RiskItem(
            risk_id=rid,
            title=raw["title"],
            description=raw["description"],
        )

    return results


# ---------------------------------------------------------
# PUBLIC ENTRYPOINT
# ---------------------------------------------------------

def run_discovery(project_description: str, model_override: str = None) -> Dict[str, RiskItem]:
    """
    Run the LLM-powered risk discovery step.

    Returns:
        dict[risk_id -> RiskItem]
    """
    llm = get_llm_client()
    model = resolve_model_version(model_override)

    prompt = DISCOVERY_PROMPT.format(description=project_description)

    try:
        raw_output = llm.generate_json(
            prompt=prompt,
            model=model,
        )
    except Exception as exc:
        error(f"LLM discovery failed: {exc}")
        raise ModelInvocationError(f"Risk discovery LLM failure: {exc}")

    if not isinstance(raw_output, list):
        raise ValidationError("Discovery LLM output must be a JSON list.")

    # Validate raw output
    for item in raw_output:
        _validate_item(item)

    # Apply formatting rules
    cleaned = apply_risk_formatting(raw_output)

    # Convert to RiskItem domain models
    info(f"Discovered {len(cleaned)} risks.")
    return _convert_to_models(cleaned)

def run_discovery_stage(project_description: str, model_override: str | None = None) -> Dict[str, RiskItem]:
    """
    Backwards-compatible wrapper used by the pipeline.

    Historically the pipeline imported `run_discovery_stage`; the new
    implementation exposes `run_discovery`. This adapter preserves that
    contract without changing callers.
    """
    return run_discovery(project_description=project_description, model_override=model_override)
