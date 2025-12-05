"""
Prompt templates for the Discovery domain.

This module contains the LLM prompt used to extract raw risks from the
project description. Prompts are isolated in dedicated modules to ensure:
    - Version control clarity
    - Reusability across pipeline components
    - Separation between language assets and execution code
"""

# ---------------------------------------------------------------------
# Risk Discovery Prompt Template
# ---------------------------------------------------------------------

DISCOVERY_PROMPT = """
You are an expert risk analyst. Given the project description below,
identify clear, distinct risk statements that could lead to delays,
quality issues, cost overruns, operational failures, or unmet objectives.

Return ONLY a JSON list of objects in the following shape:
[
  {
    "title": "short risk title",
    "description": "1-2 sentence explanation of the risk"
  }
]

Requirements:
- Identify 10–20 meaningful risks
- No duplicates or trivial restatements
- Titles must be concise and descriptive
- Descriptions must provide useful context
- DO NOT include IDs, scores, themes, or mitigations
- Output MUST be valid JSON

Project Description:
\"\"\"{description}\"\"\"
""".strip()
