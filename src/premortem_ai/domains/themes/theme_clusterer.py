"""
theme_clusterer.py

LLM-powered risk theming stage of the PreMortem AI pipeline.
Clusters scored risks into high-level themes.
"""

from typing import Dict, List
from premortem_ai.models import RiskItem, ThemeItem
from premortem_ai.llm import get_llm_client, resolve_model_version
from premortem_ai.domains.themes.prompts import THEME_PROMPT
from premortem_ai.exceptions import ValidationError, ModelInvocationError
from premortem_ai.utils.logger import info, error
from premortem_ai.config import PIPELINE_CONFIG


# --------------------------------------------------------
# INTERNAL HELPERS
# --------------------------------------------------------

def _build_risks_block(risks: Dict[str, RiskItem]) -> str:
    """Formats risks into a textual bullet list for the theme prompt."""
    lines = []
    for rid, risk in risks.items():
        lines.append(f"- {rid}: {risk.title} — {risk.description}")
    return "\n".join(lines)


def _validate_theme_output(item: dict):
    """Validate LLM theme structure."""
    if "theme_name" not in item or "rationale" not in item or "risk_ids" not in item:
        raise ValidationError(f"Theme item missing fields: {item}")

    if not isinstance(item["risk_ids"], list):
        raise ValidationError(f"Invalid risk_ids type: {item}")


# --------------------------------------------------------
# PUBLIC ENTRYPOINT
# --------------------------------------------------------

def generate_themes(risks: Dict[str, RiskItem], model_override: str = None) -> Dict[str, ThemeItem]:
    """
    Run the risk theming stage.

    Args:
        risks: dict[risk_id -> RiskItem]

    Returns:
        dict[theme_id -> ThemeItem]
    """
    if len(risks) < PIPELINE_CONFIG.min_risks_for_theming:
        info("Not enough risks for theming — skipping theme generation.")
        return {}

    llm = get_llm_client()
    model = resolve_model_version(model_override)

    prompt = THEME_PROMPT.format(
        risks_block=_build_risks_block(risks)
    )

    try:
        raw = llm.generate_json(prompt=prompt, model=model)

    except Exception as exc:
        error(f"Theme clustering LLM failure: {exc}")
        raise ModelInvocationError(f"Theme clustering failed: {exc}")

    if not isinstance(raw, list):
        raise ValidationError("Theme LLM output must be a JSON list.")

    results = {}
    theme_counter = 1

    for item in raw:
        _validate_theme_output(item)

        theme_id = f"theme-{theme_counter:03}"
        theme_counter += 1

        results[theme_id] = ThemeItem(
            theme_id=theme_id,
            theme_name=item["theme_name"],
            rationale=item["rationale"],
            risk_ids=item["risk_ids"],
        )

    info(f"Generated {len(results)} themes.")
    return results


# --------------------------------------------------------
# PIPELINE STAGE ENTRYPOINT
# --------------------------------------------------------

def run_theme_stage(*, context, request) -> None:
    """
    Pipeline stage entrypoint for theme clustering.

    Orchestrator contract:
        handler(context=context, request=request)

    Reads discovered risks from PipelineContext,
    clusters them into themes, and writes results
    back into the context.
    """
    if not getattr(context, "risks", None):
        raise ValueError("No risks available for theme clustering stage.")

    themes = generate_themes(
        risks=context.risks,
        model_override=getattr(request, "model_version_override", None),
    )

    context.themes = themes
