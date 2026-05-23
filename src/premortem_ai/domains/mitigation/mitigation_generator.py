"""
mitigation_generator.py

LLM-powered mitigation strategy generator for the PreMortem AI pipeline.
Outputs structured mitigation recommendations for each risk.
"""

from typing import Dict, List
from premortem_ai.models import RiskItem, MitigationItem
from premortem_ai.llm import get_llm_client, resolve_model_version
from premortem_ai.domains.mitigation.prompts import MITIGATION_PROMPT
from premortem_ai.exceptions import ValidationError, ModelInvocationError
from premortem_ai.utils.logger import info, error
from premortem_ai.config import PIPELINE_CONFIG


# --------------------------------------------------------
# VALIDATION
# --------------------------------------------------------

def _validate_item(item: dict, risk_id: str):
    """Ensures mitigation fields exist and are valid."""
    required = ["action", "rationale", "priority"]
    for field in required:
        if field not in item:
            raise ValidationError(
                f"Mitigation for risk {risk_id} missing '{field}': {item}"
            )

    if item["priority"] not in ("low", "medium", "high"):
        raise ValidationError(
            f"Invalid priority '{item['priority']}' for risk {risk_id}."
        )


# --------------------------------------------------------
# MAIN ENTRYPOINT
# --------------------------------------------------------

def generate_mitigations(
    risks: Dict[str, RiskItem],
    model_override: str = None
) -> Dict[str, List[MitigationItem]]:
    """
    Generate mitigation recommendations for each risk.

    Returns:
        dict[risk_id -> list[MitigationItem]]
    """
    llm = get_llm_client()
    model = resolve_model_version(model_override)

    results: Dict[str, List[MitigationItem]] = {}

    info(f"Generating mitigations for {len(risks)} risks...")

    for rid, risk in risks.items():
        prompt = MITIGATION_PROMPT.format(
            risk_id=rid,
            title=risk.title,
            description=risk.description,
        )

        try:
            raw_list = llm.generate_json(
                prompt=prompt,
                model=model,
            )
        except Exception as exc:
            error(f"Mitigation LLM failed for {rid}: {exc}")
            raise ModelInvocationError(f"Mitigation failure for {rid}: {exc}")

        if not isinstance(raw_list, list):
            raise ValidationError(
                f"Mitigation output for {rid} must be a JSON list."
            )

        mitigations: List[MitigationItem] = []

        # Limit number of mitigations based on config
        max_items = PIPELINE_CONFIG.max_mitigations_per_risk
        raw_list = raw_list[:max_items]

        for item in raw_list:
            _validate_item(item, rid)

            mitigation_id = f"{rid}-mit-{len(mitigations) + 1}"

            mitigations.append(
                MitigationItem(
                    mitigation_id=mitigation_id,
                    risk_id=rid,
                    action=item["action"],
                    rationale=item["rationale"],
                    priority=item["priority"],
                )
            )

        results[rid] = mitigations

    info("Mitigation generation complete.")
    return results


# --------------------------------------------------------
# BACKWARDS COMPATIBILITY WRAPPER
# --------------------------------------------------------

def run_mitigation_stage(*, context, request) -> None:
    """
    Pipeline stage entrypoint for mitigation generation.

    Reads scored risks from the pipeline context,
    generates mitigation strategies, and writes
    results back into the context.
    """
    if not hasattr(context, "scores") or not context.scores:
        raise ValueError("No scored risks available for mitigation stage.")

    mitigations = generate_mitigations(
        risks=context.risks,
        model_override=request.model_version_override,
    )

    context.mitigations = mitigations
