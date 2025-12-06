"""
prompts.py

Prompt templates for generating structured mitigation strategies for risks.

This prompt enforces:
    • STRICT JSON output
    • Consistent mitigation structure
    • Clear multi-step action lists
    • Compatibility with MitigationItem + MitigationAction models
    • No hallucinated fields or commentary
"""

MITIGATION_INSTRUCTIONS = """
You are an expert risk mitigation strategist. Your task is to generate a set of
mitigation strategies for each project risk, informed by risk descriptions,
scores, and theme groupings.

FOLLOW THESE RULES STRICTLY:

1. For each risk, produce a mitigation object containing:
       - "title": a short, 4–10 word summary of the recommended mitigation
       - "description": a 1–2 sentence explanation of the mitigation strategy
       - "actions": a list of 2–6 concrete, actionable steps

2. ACTION REQUIREMENTS:
       - Each action MUST be a short imperative instruction (e.g., "Define ownership",
         "Create contingency plan", "Establish vendor contract review")
       - NO generic filler actions
       - NO vague fluff like "monitor the situation"
       - Actions MUST be directly related to the specific risk

3. OUTPUT SCHEMA (STRICT):
{
  "risk-00001": {
    "title": "<short title>",
    "description": "<one or two sentence explanation>",
    "actions": [
      "<step 1>",
      "<step 2>",
      "<step 3>"
    ]
  },
  "risk-00002": {
    ...
  }
}

4. DO NOT:
       - Add commentary or explanation
       - Include markdown
       - Change risk IDs
       - Invent new risks
       - Add fields beyond title, description, actions

5. ENSURE:
       - Every risk_id provided has a corresponding mitigation
       - JSON must be valid and parseable
"""

def build_mitigation_prompt(risks: dict, themes: list) -> str:
    """
    Construct the LLM prompt for generating mitigations.

    Args:
        risks: dict[str, RiskItem]
        themes: list[ThemeItem]

    Returns:
        str: fully assembled mitigation generation prompt
    """

    # Build the risk description block
    risk_lines = []
    for rid, risk in risks.items():
        risk_lines.append(f'  "{rid}": "{risk.description.strip()}"')
    risks_block = ",\n".join(risk_lines)

    # Build theme context block
    theme_lines = []
    for theme in themes:
        theme_lines.append(
            f'- {theme.name}: risks {", ".join(theme.risk_ids)}'
        )
    theme_block = "\n".join(theme_lines) if theme_lines else "No themes identified."

    return f"""
{MITIGATION_INSTRUCTIONS}

PROJECT RISKS:
{{
{risks_block}
}}

THEME CONTEXT:
{theme_block}

Return ONLY the JSON object described above.
""".strip()
