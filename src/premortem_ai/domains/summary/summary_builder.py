"""
summary_builder.py

High-level orchestration for generating the executive summary using the LLM.

Responsibilities:
    • Construct the summary-generation prompt
    • Invoke the governed LLMClient
    • Parse the output using the summary generator
    • Return a validated SummaryItem
"""

from typing import Dict, Any, List

from premortem_ai.llm import get_llm_client, resolve_model_version
from premortem_ai.domains.summary.prompts import build_summary_prompt
from premortem_ai.domains.summary.summary_generator import parse_summary_output
from premortem_ai.exceptions import ModelInvocationError
from premortem_ai.core.logger import info, error


def run_summary(
    risks: Dict[str, Any],
    scores: Dict[str, Any],
    themes: List[Any],
    mitigations: List[Any],
    model_override: str = None,
):
    """
    Main entrypoint for generating an executive summary using the LLM.

    Args:
        risks: dict[risk_id -> RiskItem]
        scores: dict[risk_id -> ScoreItem]
        themes: list[ThemeItem]
        mitigations: list[MitigationItem]
        model_override: optional model version override

    Returns:
        SummaryItem
    """

    # -------------------------------------------------------------
    # Build prompt
    # -------------------------------------------------------------
    prompt = build_summary_prompt(risks, scores, themes, mitigations)

    # -------------------------------------------------------------
    # Select LLM model
    # -------------------------------------------------------------
    model = resolve_model_version(model_override)

    llm = get_llm_client()

    # -------------------------------------------------------------
    # Invoke LLM
    # -------------------------------------------------------------
    try:
        llm_json = llm.generate_json(prompt=prompt, model=model)

    except Exception as e:
        error(f"Summary generation LLM failure: {e}")
        raise ModelInvocationError(f"LLM summary generation failed: {e}")

    # -------------------------------------------------------------
    # Parse JSON → SummaryItem
    # -------------------------------------------------------------
    try:
        summary_item = parse_summary_output(risks, llm_json)
        info("Successfully generated executive summary.")
        return summary_item

    except Exception as e:
        error(f"Summary parsing failure: {e}")
        raise
