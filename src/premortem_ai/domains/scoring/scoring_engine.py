"""
LLM-powered scoring stage of the PreMortem AI pipeline.
Computes likelihood, impact, and severity for each discovered risk.
"""

from typing import Dict, List, Optional, Tuple, Any   # <-- ADD THIS LINE

from premortem_ai.models import RiskItem, ScoreItem
from premortem_ai.llm import get_llm_client, resolve_model_version
from premortem_ai.domains.scoring.prompts import SCORING_PROMPT
from premortem_ai.domains.scoring.severity_engine import compute_severity
from premortem_ai.domains.scoring.severity_rules import apply_severity_rules
from premortem_ai.exceptions import ValidationError, ModelInvocationError
from premortem_ai.utils.logger import info, error
from premortem_ai.config import PIPELINE_CONFIG


# ------------------------------------------------------------
# INTERNAL VALIDATION
# ------------------------------------------------------------

def _validate_llm_output(data: dict, risk_id: str):
    """
    Ensure required LLM-provided scoring signals exist and are valid.

    NOTE:
    - Severity is intentionally NOT validated here.
    - Severity is a derived metric computed deterministically by the system.
    """
    for field in ("likelihood", "impact"):
        if field not in data:
            raise ValidationError(
                f"Missing '{field}' in scoring output for risk {risk_id}"
            )

        val = data[field]
        if not isinstance(val, int) or not (1 <= val <= PIPELINE_CONFIG.score_buckets):
            raise ValidationError(
                f"Invalid score '{field}={val}' for risk {risk_id}. "
                f"Expected 1-{PIPELINE_CONFIG.score_buckets}"
            )


# ------------------------------------------------------------
# MAIN ENTRYPOINT
# ------------------------------------------------------------

def run_scoring(risks: Dict[str, RiskItem], model_override: str = None) -> Dict[str, ScoreItem]:
    """
    Run the scoring stage of the pipeline.

    Args:
        risks: dict[risk_id -> RiskItem]
    Returns:
        dict[risk_id -> ScoreItem]
    """
    llm = get_llm_client()
    model = resolve_model_version(model_override)
    results: Dict[str, ScoreItem] = {}

    info(f"Scoring {len(risks)} risks...")

    for rid, risk in risks.items():
        prompt = SCORING_PROMPT.format(
            title=risk.title,
            description=risk.description
        )

        try:
            llm_scores = llm.run(
            prompt=prompt,
            model_override=model,
        )       

        except Exception as exc:
            error(f"Scoring LLM failed for {rid}: {exc}")
            raise ModelInvocationError(
                f"Failed scoring LLM call for {rid}: {exc}"
            )

        _validate_llm_output(llm_scores, rid)

        # ------------------------------------------------------------
        # Apply custom severity calculation utilities
        # ------------------------------------------------------------
        computed_severity = compute_severity(
            likelihood=llm_scores["likelihood"],
            impact=llm_scores["impact"]
        )

        adjusted_severity = apply_severity_rules(
            base_severity=computed_severity,
            model_output_severity=llm_scores["severity"],
        )

        # ------------------------------------------------------------
        # Create ScoreItem
        # ------------------------------------------------------------
        results[rid] = ScoreItem(
            risk_id=rid,
            likelihood=llm_scores["likelihood"],
            impact=llm_scores["impact"],
            severity=adjusted_severity,
        )

    info(f"Completed scoring for {len(results)} risks.")
    return results


# ------------------------------------------------------------
# PIPELINE ENTRYPOINT
# ------------------------------------------------------------

def run_scoring_stage(*, context, request) -> None:
    """
    Pipeline stage entrypoint for scoring.

    Reads discovered risks from the pipeline context,
    runs LLM-powered scoring, and writes results back
    into the context.
    """
    if not context.risks:
        raise ValidationError("No risks available for scoring stage.")

    scored = run_scoring(
        risks=context.risks,
        model_override=request.model_version_override,
    )

    context.scores = scored
