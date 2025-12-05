"""
Prompt templates for the Scoring domain.

This module defines the LLM prompt used to evaluate likelihood, impact,
and rationale for each risk. Prompts are isolated here for versioning,
auditability, and reuse across multiple scoring components.

The goal: produce stable, schema-aligned scoring signals that can be
combined with deterministic rule-based scores.
"""

SCORING_PROMPT = """
You are a senior risk analyst. Evaluate the following project risk and
assign severity metrics using a structured, objective approach.

Return ONLY a JSON object in the following shape:
{
  "likelihood": <0-10 integer>,
  "impact": <0-10 integer>,
  "rationale": "1-2 sentence explanation"
}

Scoring Guidelines:
- likelihood: How probable the risk is (0 = very unlikely, 10 = almost certain)
- impact: How damaging the risk would be (0 = minimal, 10 = catastrophic)
- Use clear, concise reasoning in the rationale.
- DO NOT include severity; it will be computed downstream.
- DO NOT include IDs or extra fields.
- The output MUST be valid JSON.

Risk Title:
"{title}"

Risk Description:
"{description}"
""".strip()
