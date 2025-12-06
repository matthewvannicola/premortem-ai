"""
mitigation_generator.py

Enterprise-grade mitigation generation engine for PreMortem AI.

Responsibilities:
    • Parse LLM mitigation JSON output
    • Validate schema correctness
    • Normalize titles, descriptions, and actions
    • Construct MitigationItem + MitigationAction models
    • Validate risk references
    • Generate stable IDs via id_generation utilities
    • Log warnings and errors
    • Guarantee deterministic output ordering
"""

from typing import Dict, Any, List

from premortem_ai.models import MitigationItem, MitigationAction
from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.core.id_generation import generate_mitigation_id
from premortem_ai.core.logger import info, warning, error
from premortem_ai.exceptions import (
    ValidationError,
    CrossReferenceError,
    ModelInvocationError,
)


# ----------------------------------------------------------------------
# PUBLIC API
# ----------------------------------------------------------------------

def parse_mitigation_output(
    risks: Dict[str, Any],
    llm_output: Dict[str, Any],
) -> List[MitigationItem]:
    """
    Convert LLM mitigation output JSON → List[MitigationItem].

    Args:
        risks: dict[risk_id -> RiskItem]
        llm_output: JSON dict returned by LLM mapping risk_id -> mitigation object

    Returns:
        List[MitigationItem]
    """

    if not isinstance(llm_output, dict):
        raise ValidationError("Mitigation output MUST be a JSON object { risk_id: {...}, ... }")

    mitigations: List[MitigationItem] = []

    for risk_id, raw_obj in llm_output.items():
        try:
            item = _build_mitigation_item(risk_id, raw_obj, risks)
            mitigations.append(item)

        except ValidationError as e:
            warning(f"Invalid mitigation for {risk_id}: {e}")
            continue

        except Exception as e:
            error(f"Unexpected error parsing mitigation for {risk_id}: {e}")
            raise ModelInvocationError(f"Unhandled mitigation generation error: {e}")

    # Deterministic ordering (by risk_id)
    mitigations.sort(key=lambda m: m.risk_ids[0])

    info(f"Constructed {len(mitigations)} mitigations.")
    return mitigations


# ----------------------------------------------------------------------
# INTERNAL VALIDATION + CONSTRUCTION
# ----------------------------------------------------------------------

def _build_mitigation_item(
    risk_id: str,
    raw: Dict[str, Any],
    risks: Dict[str, Any],
) -> MitigationItem:
    """
    Build a validated MitigationItem from one LLM mitigation object.
    """

    if risk_id not in risks:
        raise CrossReferenceError(f"Mitigation references unknown risk_id '{risk_id}'.")

    # Validate required fields
    if not isinstance(raw, dict):
        raise ValidationError(f"Mitigation for {risk_id} must be an object.")

    if "title" not in raw or "description" not in raw or "actions" not in raw:
        raise ValidationError(
            f"Mitigation for {risk_id} missing required keys: title, description, actions"
        )

    title = normalize_text(raw["title"])
    description = normalize_text(raw["description"])
    raw_actions = raw["actions"]

    if not isinstance(raw_actions, list):
        raise ValidationError(f"Mitigation.actions for {risk_id} must be a list.")

    if len(raw_actions) < 1:
        raise ValidationError(f"Mitigation for {risk_id} must define at least 1 action.")

    # Build MitigationAction objects
    actions: List[MitigationAction] = []
    for idx, act in enumerate(raw_actions):
        if not isinstance(act, str):
            raise ValidationError(f"Action #{idx} for {risk_id} must be a string.")

        actions.append(
            MitigationAction(
                action_id=f"{generate_mitigation_id()}-a{idx+1}",
                description=normalize_text(act),
            )
        )

    # Construct MitigationItem
    item = MitigationItem(
        mitigation_id=generate_mitigation_id(),
        title=title,
        description=description,
        risk_ids=[risk_id],
        actions=actions,
    )

    return item
