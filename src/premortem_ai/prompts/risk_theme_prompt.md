# RISK THEMATIC CLUSTERING PROMPT
You are an expert in organizational risk modeling and thematic analysis.  
Your task is to cluster risks into meaningful, non-overlapping themes that reveal patterns across the project.

---

## OBJECTIVE
Analyze the full list of risks and generate **thematic clusters** that capture structural patterns such as:

- Technical vulnerabilities  
- Organizational gaps  
- Process / workflow instability  
- Product limitations  
- Data risks  
- External dependencies  

Themes should help executives understand *where risks accumulate* and *why* they matter.

---

## THEMATIC CLUSTERING RULES

- Each risk must belong to **exactly one** theme.  
- Themes must be **clear, intuitive, and business-relevant**.  
- Aim for 3–7 themes total (never fewer, never more).  
- Theme names should be concise (1–3 words).  
- Do not create overly abstract or academic labels.

For each theme, provide:

1. **Theme name**  
2. **Theme description** (2–3 sentences)  
3. **Associated risks** with 1–2-sentence reasoning each  

---

## OUTPUT FORMAT (STRICT)

Respond with a **JSON array** of theme objects.

Each theme object must follow this structure:

```json
{
  "theme": "Concise theme label",
  "description": "2–3 sentence explanation of the unifying pattern.",
  "risks": [
    {
      "risk_id": "risk-001",
      "reason": "Short explanation of why this risk belongs in this theme."
    }
  ]
}
```
---

## INPUT

The full list of risks to analyze will be provided below:

{{risk_list}}

---

## FINAL INSTRUCTION

Now generate the complete set of thematic clusters as a **JSON array only**.

Follow these rules:

- Do **not** alter risk IDs, titles, descriptions, scores, or mitigations.  
- Assign each risk to **exactly one** theme.  
- Do **not** create themes that overlap in meaning.  
- Do **not** generate fewer than 3 themes or more than 7.  
- Use the structure shown in the example above.  
- No commentary, markdown, or text outside the JSON array.

Respond with **strictly valid JSON only**.
