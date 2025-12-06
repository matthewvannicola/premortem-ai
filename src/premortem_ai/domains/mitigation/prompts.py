MITIGATION_PROMPT = """
You are an expert in risk mitigation strategy.

Given the following risk:

Risk ID: {risk_id}
Title: {title}
Description: {description}

Generate actionable mitigation strategies. For each mitigation, include:

- "action": a short action-focused statement
- "rationale": a 1–2 sentence explanation
- "priority": one of ["low", "medium", "high"]

Return ONLY valid JSON in this format:

[
  {
    "action": "...",
    "rationale": "...",
    "priority": "high"
  }
]
"""
