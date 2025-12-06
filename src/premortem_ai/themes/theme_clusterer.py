"""
theme_clusterer.py

Enterprise-grade theme clustering engine for PreMortem AI.

Responsibilities:
    • Parse the LLM-generated theme JSON
    • Validate schema correctness
    • Normalize name/description/risk references
    • Ensure all risk_ids exist
    • Deduplicate risk_ids
    • Generate stable ThemeItem objects
    • Handle errors with structured fallbacks
"""

from typing import List, Dict, Any

from premortem_ai.models import ThemeItem
from premortem_ai.core.logger import info, warning, error
from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.core.id_generation import generate_theme_id
from premortem_ai.exceptions import (
    ValidationError,
    ModelInvocationError,
    CrossReferenceError,
)


# ----------------------------------------------------------------------
# MAIN PARSER
# ----------------------------------------------------------------------

def parse_theme_output(risks: Dict[str, Any], llm_output: Any) -> List[ThemeItem]:
    """
    Convert LLM theme output JSON → List[ThemeItem].

    Args:
        risks: dict[risk_id -> RiskItem]
        llm_output: JSON array returned by LLM (already parsed)

    Returns:
        List[ThemeItem]
    """

    if not isinstance(llm_output, list):
        raise ValidationError("LLM theme output must be a JSON array.")

    themes: List[ThemeItem] = []

    for idx, raw_theme in enumerate(llm_output):
        try:
            theme_item = _build_theme_item(raw_theme, risks)
            themes.append(theme_item)

        except ValidationError as e:
            warning(f"Theme #{idx} is invalid: {e}")
            continue  # skip bad themes

        except Exception as e:
            error(f"Unexpected theme parsing error: {e}")
            raise ModelInvocationError(
                f"Unhandled error building theme from LLM output: {e}"
            )

    # Deterministic ordering (alphabetical by name)
    themes.sort(key=lambda t: t.name)

    info(f"Constructed {len(themes)} themes successfully.")
    return themes


# ----------------------------------------------------------------------
# INTERNAL THEME CONSTRUCTION
# ----------------------------------------------------------------------

def _build_theme_item(raw: Dict[str, Any], risks: Dict[str, Any]) -> ThemeItem:
    """
    Build and validate a ThemeItem object from raw LLM JSON.
    """

    if not isinstance(raw, dict):
        raise ValidationError("Theme entry must be a JSON object.")

    # Validate required fields
    if "name" not in raw or "description" not in raw or "risk_ids" not in raw:
        raise ValidationError(
            "Each theme must include 'name', 'description', and 'risk_ids'."
        )

    name = normalize_text(raw["name"])
    description = normalize_text(raw["description"])

    raw_ids = raw["risk_ids"]
    if not isinstance(raw_ids, list):
        raise ValidationError("risk_ids must be a list.")

    # Normalize, dedupe, and validate referenced risk_ids
    cleaned_ids = []
    for rid in raw_ids:
        rid = str(rid).strip()
        if rid not in risks:
            raise CrossReferenceError(f"Theme references unknown risk_id '{rid}'.")
        if rid not in cleaned_ids:
            cleaned_ids.append(rid)

    if len(cleaned_ids) < 1:
        raise ValidationError("Theme must include at least one valid risk_id.")

    return ThemeItem(
        theme_id=generate_theme_id(),
        name=name,
        description=description,
        risk_ids=cleaned_ids,
    )
