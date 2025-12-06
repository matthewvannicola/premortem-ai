"""
prompts.py

Prompt templates for generating the executive summary of the PreMortem AI analysis.

This prompt enforces:
    • STRICT JSON output
    • Correct schema for SummaryItem
    • Deterministic narrative blocks
    • Identification of highest-severity risks
    • Zero hallucinations or added commentary
"""

SUMMARY_INSTRUCTIONS = """
You are an expert executive risk analyst. Your task is to generate a concise and
actionable executive summary of the project's risk posture, based on:

    • risk descriptions
    • scoring results
    • thematic analysis
    • mitigation strategy

FOLLOW THESE RULES STRICTLY:

1. Produce FOUR written narrative fields:
    - "executive_summary": 4–7 sentences summarizing the overall risk posture.
    - "top_risks_summary": 3–5 sentences synthesizing the highest-severity risks.
    - "themes_summary": 3–5 sentences describing systemic patterns across themes.
    - "mitigation_overview": 3–5 sentences summarizing the overall mitigation strength and gaps.

2. Produce "top_risk_ids":
    - A JSON array containing the IDs of the 3–5 highest-severity risks.
    - Use ONLY risk IDs provided.
    - Order them from highest → lower severity.

3. DO NOT:
    - Add markdown, bullet points, or formatting symbols.
    - Add fields other than the required schema.
    - Invent new risks or change risk IDs.
    - Include commentary, preamble, or explanation outside the JSON.

4. OUTPUT FORMAT (STRICT JSON):
{
    "executive_summary": "<narrative>",
    "top_risks_summary": "<narrative>",
    "themes_summary": "<narrative>",
    "mitigation_overview": "<narrative>",
    "top_risk_ids": ["risk-00001", "risk-00007", ...]
}
""".strip()


def build_summary_prompt(
    risks: dict,
    scores: dict,
    themes: list,
    mitigations: list
) -> str:
    """
    Construct a summary-generation prompt for the LLM.

    Args:
        risks: dict[str, RiskItem]
        scores: dict[str, ScoreItem]
        themes: list[ThemeItem]
        mitigations: list[MitigationItem]

    Returns:
        str: Fully assembled LLM prompt.
    """

    # ------------------------------------------------------------------
    # RISK BLOCK
    # ------------------------------------------------------------------
    risk_lines = []
    for rid, risk in risks.items():
        risk_lines.append(f'  "{rid}": "{risk.description.strip()}"')
    risks_block = ",\n".join(risk_lines)

    # ------------------------------------------------------------------
    # SCORE BLOCK
    # ------------------------------------------------------------------
    score_lines = []
    for rid, score in scores.items():
        score_lines.append(
            f'  "{rid}": {{"likelihood": {score.likelihood}, "impact": {score.impact}, "severity": {score.severity}}}'
        )
    scores_block = ",\n".join(score_lines)

    # ------------------------------------------------------------------
    # THEME BLOCK
    # ------------------------------------------------------------------
    theme_lines = []
    for theme in themes:
        theme_lines.append(
            f'- {theme.name}: risks {", ".join(theme.risk_ids)}'
        )
    themes_block = "\n".join(theme_lines) if theme_lines else "No themes identified."

    # ------------------------------------------------------------------
    # MITIGATION BLOCK
    # ------------------------------------------------------------------
    mitigation_lines = []
    for m in mitigations:
        mitigation_lines.append(
            f'- {m.title}: covers {", ".join(m.risk_ids)}'
        )
    mitigation_block = "\n".join(mitigation_lines) if mitigations else "No mitigations generated."

    # ------------------------------------------------------------------
    # FINAL PROMPT
    # ------------------------------------------------------------------
    return f"""
{SUMMARY_INSTRUCTIONS}

RISKS:
{{
{risks_block}
}}

SCORES:
{{
{scores_block}
}}

THEMES:
{themes_block}

MITIGATIONS:
{mitigation_block}

Return ONLY the strict JSON object described above.
""".strip()
