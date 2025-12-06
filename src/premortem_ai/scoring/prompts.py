"""
prompts.py

Prompt templates for LLM-driven risk scoring.

This prompt enforces:
    • Strict JSON output
    • Canonical severity categories
    • One scoring object per risk
    • Deterministic structure compatible with SeverityEngine
"""

SCORING_SYSTEM_INSTRUCTIONS = """
You are an expert risk analyst. Your task is to assign a likelihood and impact
rating to each project risk using standardized categories.

Follow these rules STRICTLY:

LIKELIHOOD OPTIONS (choose EXACTLY one):
    - "very low"
    - "low"
    - "medium"
    - "high"
    - "very high"

IMPACT OPTIONS (choose EXACTLY one):
    - "minimal"
    - "low"
    - "moderate"
    - "significant"
    - "critical"

DEFINITIONS:
    - likelihood: how probable the risk is to occur
    - impact: how severe the consequences would be if the risk occurs

OUTPUT FORMAT (STRICT JSON):
Produce a JSON object where each key is the risk_id and each value is an object:

{
    "risk-00001": {
        "likelihood": "<one of allowed likelihoods>",
        "impact": "<one of allowed impact categories>"
    },
    "risk-00002": {
        ...
    }
}

DO NOT add explanations.
DO NOT add commentary.
DO NOT add fields other than "likelihood" and "impact".
DO NOT output anything outside the JSON object.
""".strip()


def build_scoring_prompt(risks: dict) -> str:
    """
    Construct an LLM prompt for scoring a batch of risks.

    Args:
        risks: dict[str, RiskItem] mapping risk_id -> RiskItem

    Returns:
        str: Fully assembled LLM prompt
    """

    risk_descriptions = []
    for risk_id, risk in risks.items():
        risk_descriptions.append(f'"{risk_id}": "{risk.description}"')

    risks_block = ",\n".join(risk_descriptions)

    return f"""
{SCORING_SYSTEM_INSTRUCTIONS}

RISKS TO SCORE:
{{
{risks_block}
}}

Return ONLY the JSON object described above.
""".strip()
