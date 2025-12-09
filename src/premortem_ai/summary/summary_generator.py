"""
summary_generator.py

Enterprise-grade engine for converting LLM-generated summary JSON
into a validated SummaryItem object.
"""

from typing import Dict, Any, List

from premortem_ai.summary.models import SummaryItem
from premortem_ai.domains.shared.text import collapse_whitespace, ensure_sentence
from premortem_ai.utils.logger import info, warning, error
from premortem_ai.exceptions import (
    ValidationError,
    CrossReferenceError,
    ModelInvocationError,
)


def _clean_text(value: str) -> str:
    """Apply consistent cleaning pipeline."""
    return ensure_sentence(collapse_whitespace(value))


# ----------------------------------------------------------------------
# PUBLIC API — PARSER
# ----------------------------------------------------------------------

def parse_summary_output(
    risks: Dict[str, Any],
    llm_output: Dict[str, Any],
) -> SummaryItem:
    """Convert LLM summary JSON → SummaryItem."""

    if not isinstance(llm_output, dict):
        raise ValidationError("Summary output must be a JSON object.")

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

    # Clean narrative fields
    exec_summary = _clean_text(llm_output["executive_summary"])
    top_risks_summary = _clean_text(llm_output["top_risks_summary"])
    themes_summary = _clean_text(llm_output["themes_summary"])
    mitigation_overview = _clean_text(llm_output["mitigation_overview"])

    # Validate top risk ids
    raw_ids = llm_output["top_risk_ids"]
    if not isinstance(raw_ids, list):
        raise ValidationError("top_risk_ids must be a list of risk IDs.")

    cleaned_ids = []
    for rid in raw_ids:
        rid = str(rid).strip()
        if rid not in risks:
            raise CrossReferenceError(f"Summary references unknown risk ID '{rid}'.")
        if rid not in cleaned_ids:
            cleaned_ids.append(rid)

    if not cleaned_ids:
        raise ValidationError("Summary must include at least one top risk ID.")

    try:
        summary = SummaryItem(
            executive_summary=exec_summary,
            top_risks_summary=top_risks_summary,
            themes_summary=themes_summary,
            mitigation_overview=mitigation_overview,
            top_risk_ids=cleaned_ids,
        )

        summary = summary.normalize()

        info("Successfully constructed SummaryItem from LLM output.")
        return summary

    except Exception as e:
        error(f"Unexpected error building SummaryItem: {e}")
        raise ModelInvocationError(f"Failed to create SummaryItem: {e}")


# ----------------------------------------------------------------------
# BACKWARDS COMPATIBILITY — STAGE WRAPPER
# ----------------------------------------------------------------------

def run_summary_stage(
    risks: Dict[str, Any],
    scores: Dict[str, Any],
    themes: Dict[str, Any],
    mitigations: Dict[str, Any],
    model_override: str | None = None,
):
    """
    Backwards-compatible wrapper calling the actual summary builder.
    Imported lazily to avoid circular import.
    """
    from premortem_ai.summary.summary_builder import generate_summary

    return generate_summary(
        risks=risks,
        scores=scores,
        themes=themes,
        mitigations=mitigations,
        model_override=model_override,
    )
