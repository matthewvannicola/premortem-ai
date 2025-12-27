THEME_PROMPT = """
You are an expert risk analyst.

Given the following list of risks:

{risks_block}

Cluster these risks into meaningful themes. For each theme, provide:

- theme_name: short category title
- rationale: 1–2 sentence explanation
- risk_ids: list of risk IDs that belong to this theme

Return ONLY valid JSON in this format:

[
  {{
    "theme_name": "...",
    "rationale": "...",
    "risk_ids": ["risk-001", "risk-002"]
  }}
]
"""