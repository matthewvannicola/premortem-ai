SCORING_PROMPT = """
You are an expert risk analyst.

Given the following risk:

Title:
{title}

Description:
{description}

Assign the following values:

- likelihood: integer 1–5
- impact: integer 1–5
- severity: integer 1–5 (your expert judgment)

Return only valid JSON in this format:

{{
  "likelihood": <1-5>,
  "impact": <1-5>,
  "severity": <1-5>
}}
"""
