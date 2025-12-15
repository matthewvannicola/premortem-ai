"""
discovery_engine.py

Enterprise-grade risk discovery engine for the PreMortem AI pipeline.
Uses governed LLMClient + strict validation to extract structured risks.
"""

from typing import Dict, List

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
    """Ensure required fields exist in a discovered risk item."""
    if not isinstance(item, dict):
        raise ValidationError(f"Risk item must be an object, got: {type(item)}")

    if "title" not in item or "description" not in item:
        raise ValidationError(f"Risk item missing required fields: {item}")


def _convert_to_models(risks: List[dict]) -> Dict[str, RiskItem]:
    """Convert cleaned risks into RiskItem models with generated IDs."""
    results: Dict[str, RiskItem] = {}

    for raw in risks:
        rid = generate_risk_id()
        results[rid] = RiskItem(
            risk_id=rid,
            title=raw["title"],
            description=raw["description"],
        )

    return results


# ---------------------------------------------------------
# CORE DISCOVERY FUNCTION
# ---------------------------------------------------------

def run_discovery(
    project_description: str,
    model_override: str = None
) -> Dict[str, RiskItem]:
    """
    Run the LLM-powered risk discovery step.

    Returns:
        Mapping of risk_id -> RiskItem
    """
    llm = get_llm_client()
    model = resolve_model_version(model_override)

    prompt = DISCOVERY_PROMPT.format(description=project_description)

    try:
        raw_output = llm.run(
            prompt=prompt,
            model_override=model
        )
    except Exception as exc:
        error(f"LLM discovery failed during invocation: {exc}")
        raise ModelInvocationError(
            f"Risk discovery LLM failure: {exc}"
        ) from exc

    if not isinstance(raw_output, list):
        raise ValidationError(
            "Discovery LLM output must be a list of risk objects."
        )

    for item in raw_output:
        _validate_item(item)

    cleaned = apply_risk_formatting(raw_output)

    info(f"Discovered {len(cleaned)} risks.")
    return _convert_to_models(cleaned)


# ---------------------------------------------------------
# PIPELINE ENTRYPOINT
# ---------------------------------------------------------

def run_discovery_stage(*, context, request) -> None:
    """
    Pipeline stage entrypoint.
    """
    risks = run_discovery(
        project_description=request.project_description,
        model_override=request.model_version_override
    )

    context.risks = risks


    # Write discovery output into pipeline context
    context.risks = risks
