"""
Prompt templates for the Mitigation domain.

This module defines the LLM prompt used to generate targeted mitigation
recommendations for each risk. Prompts are isolated for auditability,
version control, and consistency across environments.
"""

MITIGATION_PROMPT = """
You are a senior risk mitigation specialist. For each risk provided,
produce a set of clear, actionable mitigation recommendations that reduce
likelihood, impact, or both.

Return ONLY a JSON list in the following structure:
[
  {
    "risk_id": "risk-xxxxxx",
    "actions": [
      "specific mitigation step 1",
      "specific mitigation step 2"
    ],
    "rationale": "1–2 sentence explanation for why these actions help"
  }
]

Guidelines:
- Mitigation actions must be specific and implementable
- Avoid vague or high-level advice
- Tie recommended actions to risk severity and contributing factors
- If theme context is provided, incorporate it into your reasoning
- Do NOT generate new risk IDs
- Do NOT include fields outside the schema
- The output MUST be valid JSON

Here are the risks requiring mitigation:

```json
{risks}
```
""".strip()
