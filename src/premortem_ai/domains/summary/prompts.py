"""
prompts.py

Prompt templates for generating the final executive summary.
This file is intentionally minimal, containing only the canonical
template used to guide the LLM into producing a structured JSON
SummaryItem payload.

The summary synthesizes:
  - Risk narratives
  - Severity scoring insights
  - Theme-level patterns
  - Mitigation strategy overviews
"""

SUMMARY_PROMPT_TEMPLATE = """
You are an expert in risk analysis, enterprise reporting, and concise executive communication.

Your task is to produce a structured JSON summary of the entire project risk assessment, based on the information below.

----------------------------------------------------------------------
RISK DETAILS
----------------------------------------------------------------------
{risks_block}

----------------------------------------------------------------------
THEME ANALYSIS
----------------------------------------------------------------------
{themes_block}

----------------------------------------------------------------------
MITIGATION OVERVIEW
----------------------------------------------------------------------
{mitigations_block}

----------------------------------------------------------------------
INSTRUCTIONS
----------------------------------------------------------------------
Produce an EXECUTIVE-LEVEL summary written in clear, direct, formal language.

Your summary MUST include:

1. "executive_summary"
    - A high-level explanation of the overall project risk posture.
    - Describe the most important patterns across risks and themes.
    - 4–7 sentences.

2. "top_risks_summary"
    - A concise explanation of the highest-severity risks.
    - Include WHY they are the most critical.
    - 3–6 sentences.

3. "themes_summary"
    - Summaries of the major cross-cutting patterns.
    - Explain what these themes reveal about the project.
    - 3–6 sentences.

4. "mitigation_overview"
    - A synthesis of the strongest and most critical mitigation strategies.
    - Explain how these mitigations reduce top risks.
    - 3–6 sentences.

5. "top_risk_ids"
    - A JSON array listing the **most important risk IDs**, in severity order.
    - MUST reference only risk IDs shown in the risk list.
    - MUST include at least 1 risk.
    - MUST be a flat JSON array of strings.

----------------------------------------------------------------------
OUTPUT FORMAT (STRICT)
----------------------------------------------------------------------
Return ONLY valid JSON in the EXACT structure:

{
  "executive_summary": "...",
  "top_risks_summary": "...",
  "themes_summary": "...",
  "mitigation_overview": "...",
  "top_risk_ids": ["risk-001", "risk-002", "risk-003"]
}

Do NOT include markdown.
Do NOT include commentary.
Do NOT include explanations.
Return ONLY the JSON object.
"""
def build_summary_prompt(
    risks_block: str,
    themes_block: str,
    mitigations_block: str,
) -> str:
    """
    Construct a fully formatted summary prompt by injecting
    structured blocks into the SUMMARY_PROMPT_TEMPLATE.
    """
    return SUMMARY_PROMPT_TEMPLATE.format(
        risks_block=risks_block,
        themes_block=themes_block,
        mitigations_block=mitigations_block,
    )
