"""
Prompt templates for the Themes domain.

This module defines the prompt used to cluster risks into higher-level
themes. Prompts are isolated for versioning, auditability, and clean
separation between language assets and execution logic.
"""

THEME_CLUSTERING_PROMPT = """
You are an expert in risk analysis and thematic clustering. Given the list
of risks below, group them into meaningful higher-level themes that reflect
shared issues, systemic drivers, or common root causes.

Return ONLY a JSON list of theme objects with the following structure:
[
  {
    "name": "short theme title",
    "description": "1–2 sentence explanation of what ties these risks together",
    "risk_ids": ["risk-xxxxxx", "risk-yyyyyy"]
  }
]

Requirements:
- Identify 3–6 distinct themes
- Each theme must contain at least two risks
- No duplicate, trivial, or overly broad themes
- Theme names must be concise and descriptive
- The output MUST be valid JSON

Here is the full set of risks (including severity values):

```json
{risks}
""".strip()
