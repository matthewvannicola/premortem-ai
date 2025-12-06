"""
prompts.py

Prompt templates for generating risk themes using the LLM.

The prompt enforces:
    • Strict JSON output
    • Canonical theme structure
    • Deterministic schema
    • Zero hallucinated fields
    • Clean grouping logic

This matches the schema expected by ThemeClusterer and ThemeItem.
"""

THEME_INSTRUCTIONS = """
You are an expert risk analyst. Your task is to group related project risks
into consolidated THEMES.

A theme is a high-level conceptual grouping of 2–10 risks that share
a common underlying pattern.

FOLLOW THESE RULES STRICTLY:

1. Each theme MUST include:
      • a concise name (3–7 words)
      • a description (1 sentence)
      • a list of risk IDs that belong to the theme

2. DO NOT create a theme for a single risk unless no other grouping is possible.

3. DO NOT repeat risk IDs across themes unless there is strong justification.

4. KEEP THEME NAMES SHORT, SPECIFIC, AND NON-GENERIC.
   Bad examples:
      - "General Risks"
      - "Multiple Uncertainties"
   Good examples:
      - "Ambiguous Requirements Overlap"
      - "Unstable Vendor Dependencies"
      - "Missing Technical Ownership"

5. Only use risk IDs that are provided.
   DO NOT invent new risks.
   DO NOT rename risks.

6. Output ONLY a JSON array of theme objects.
   DO NOT add commentary or explanation.

OUTPUT SCHEMA (STRICT):
[
  {
    "name": "<short theme name>",
    "description": "<one-sentence explanation>",
    "risk_ids": ["risk-00001", "risk-00004", ...]
  },
  {
    ...
  }
]
""".strip()


def build_theme_prompt(risks: dict) -> str:
    """
    Construct an LLM prompt for clustering risks into themes.

    Args:
        risks: dict[str, RiskItem]

    Returns:
        str: Fully assembled LLM prompt
    """

    risk_lines = []
    for risk_id, risk in risks.items():
        # Prevents extremely long prompt drift
        summarized_desc = risk.description.strip()

        risk_lines.append(f'  "{risk_id}": "{summarized_desc}"')

    risks_block = ",\n".join(risk_lines)

    return f"""
{THEME_INSTRUCTIONS}

RISKS AVAILABLE FOR THEMING:
{{
{risks_block}
}}

Return ONLY the JSON array.
    """.strip()
