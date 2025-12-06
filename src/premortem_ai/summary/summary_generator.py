"""
summary_generator.py

Enterprise-grade engine for converting LLM-generated summary JSON
into a validated SummaryItem object.

Responsibilities:
    • Validate strict JSON structure from LLM
    • Normalize narrative fields
    • Validate referenced risk IDs
    • Construct SummaryItem models
    • Provide deterministic, repeatable output
"""

from typing import Dict, Any, List

from premortem_ai.summary.models import SummaryItem
from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.core.logger import info, warning, error
from premortem_ai.exceptions import (
    ValidationError,
    CrossReferenceError,
    ModelInvocationError,
)


# ----------------------------------------------------------------------
# PUBLIC API
# ----------------------------------------------------------------------

def parse_summary_output(
    risks: Dict[str, Any],
    llm_output: Dict[str, Any],
) -> SummaryItem:
    """
    Convert LLM summary JSON → SummaryItem.

    Args:
        risks: dict[risk_id -> RiskItem]
        llm_output: JSON dict returned by the LLM

    Returns:
        SummaryItem
    """

    # --------------------------------------------------------------
    # Top-level must be a JSON object
    # --------------------------------------------------------------
    if not isinstance(llm_output, dict):
        raise ValidationError("Summary output must be a JSON object.")

    # Required fields
    required_keys = [
        "executive_summary",
        "top_risks_summary",
        "themes_summary",
        "mitigation_overview",
        "top_risk_ids",
    ]

    for key in required_keys:
        if key not in llm_output:
            raise ValidationError(f"Summary output missing required key '{key}'.")

    # --------------------------------------------------------------
    # Extract + normalize narrative fields
    # --------------------------------------------------------------
    exec_summary = normalize_text(llm_output["executive_summary"])
    top_risks_summary = normalize_text(llm_output["top_risks_summary"])
    themes_summary = normalize_text(llm_output["themes_summary"])
    mitigation_overview = normalize_text(llm_output["mitigation_overview"])

    # --------------------------------------------------------------
    # Validate top_risk_ids
    # --------------------------------------------------------------
    raw_ids = llm_output["top_risk_ids"]

    if not isinstance(raw_ids, list):
        raise ValidationError("top_risk_ids must be a list of risk IDs.")

    cleaned_ids: List[str] = []
    for rid in raw_ids:
        rid = str(rid).strip()

        if rid not in risks:
            raise CrossReferenceError(
                f"Summary references unknown risk ID '{rid}'."
            )

        if rid not in cleaned_ids:
            cleaned_ids.append(rid)

    if len(cleaned_ids) == 0:
        raise ValidationError("Summary must include at least one top risk ID.")

    # --------------------------------------------------------------
    # Construct model
    # --------------------------------------------------------------
    try:
        summary = SummaryItem(
            executive_summary=exec_summary,
            top_risks_summary=top_risks_summary,
            themes_summary=themes_summary,
            mitigation_overview=mitigation_overview,
            top_risk_ids=cleaned_ids,
        )

        info("Successfully constructed SummaryItem from LLM output.")
        return summary

    except Exception as e:
        error(f"Unexpected error building SummaryItem: {e}")
        raise ModelInvocationError(f"Failed to create SummaryItem: {e}")
