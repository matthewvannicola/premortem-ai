# PreMortem AI — Pipeline Architecture

The PreMortem AI pipeline transforms a free-text project description into a structured, risk-intelligence report with scoring, thematic clustering, mitigation recommendations, summarization, and an export-ready PDF.

The system is engineered for:

- deterministic LLM execution  
- strict JSON-schema validation  
- component-level isolation  
- predictable and reproducible outputs  

This makes the pipeline suitable for enterprise, audit-ready environments.

---

## Architecture Summary

The pipeline is implemented using modular Pipedream components that each perform a single, well-defined transformation.  
Every component enforces strict JSON schemas, ensuring that data flowing through the system is validated, normalized, and contract-bound.

### Execution Flow

Data moves through the pipeline in a linear, deterministic sequence:

```
discovery → scoring → themes → mitigation → summary → final_report → pdf_export
```

### Key Architectural Features

- **Component Isolation**  
  Each step runs independently, receives only the fields it needs, and produces a validated output.

- **Schema-Driven Contracts**  
  All input/output structures are enforced with JSON schema to ensure reproducibility and predictable downstream behavior.

- **Deterministic Processing**  
  Scoring and normalization logic guarantee consistent results across repeated executions.

- **Retry Workflow**  
  A separate retry mechanism re-executes only the failing step, using exponential backoff, without recomputing the full pipeline.

- **Separation of Responsibilities**  
  Components handle:
  - extraction  
  - scoring  
  - clustering  
  - mitigation planning  
  - summarization  
  - report assembly  
  - PDF generation  

This architecture enables predictable performance, clear boundaries, and enterprise-grade maintainability.

---

## Component Responsibilities

The pipeline is composed of seven modular components.  
Each performs a single, deterministic transformation and passes a validated JSON object to the next stage.

### Discovery
Extracts raw risks, assumptions, uncertainties, and hidden failure modes from the project description.

Produces:
```json
{
  "risks": [
    {
      "id": "risk-001",
      "title": "Concise risk title",
      "description": "Detailed explanation of the risk",
      "category": "Operational | Technical | Financial | etc."
    }
  ]
}
```

Notes:

- This is the first structured object produced by the pipeline.
- All downstream components depend on risk_id integrity.
- Risk ordering remains stable for reproducibility.

---

### Scoring

Purpose:  
Apply a deterministic scoring model to each discovered risk, producing quantitative measures of likelihood, impact, and overall severity.

Adds the following fields to every risk:

- `likelihood_score` (0–1)
- `impact_score` (0–1)
- `severity_score` (0–1, derived)

Example output shape:
```json
{
  "risks": [
    {
      "id": "risk-001",
      "title": "Concise risk title",
      "description": "Detailed explanation",
      "category": "Operational",
      "likelihood_score": 0.4,
      "impact_score": 0.7,
      "severity_score": 0.28
    }
  ]
}
```

Notes:

- Scoring is deterministic for identical input.
- Severity scores preserve ordering for downstream prioritization.
- No new risks are created or removed during scoring.

---

# **Themes Component**

## **Purpose**
The **Themes Component** analyzes the full set of discovered risks and identifies higher-order patterns that indicate structural weaknesses or recurring failure modes.  
Themes provide an abstraction layer above individual risks so leadership can track cross-project patterns, prioritize systemic mitigations, and guide portfolio-level decisions.

## **Example Output Shape**
```jsonc
{
  "themes": [
    {
      "theme_id": "theme-001",
      "name": "Unclear Ownership & Accountability",
      "description": "Multiple risks indicate role ambiguity across engineering and product teams.",
      "related_risk_ids": ["risk-003", "risk-014", "risk-027"],
      "occurrence_count": 3
    }
  ]
}
```

Notes

- Themes emerge from clustering logic over risk text, metadata, and semantic similarity; they are not hand-picked labels.
- Each theme must reference only valid risk_id values; the pipeline rejects orphaned or mismatched IDs.
- Themes must remain concise, interpretable, and minimally overlapping to preserve executive readability.
- The themes array is consumed by downstream mitigation, summary, and PDF report components to maintain consistent reasoning across the system.

---

# **Micro-Group 4 — Mitigations Component**

## **Purpose**
The **Mitigations Component** translates each validated risk into a set of actionable, context-aware mitigation strategies.  
It ensures every risk has a path toward reduction, ownership clarification, or operational stabilization. This component is critical for turning analysis into execution-ready guidance.

## **Example Output Shape**
```jsonc
{
  "mitigations": [
    {
      "risk_id": "risk-014",
      "mitigation_id": "mitigation-014-01",
      "actions": [
        "Define explicit technical ownership for onboarding flows.",
        "Create a cross-functional escalation path for unresolved dependencies."
      ],
      "effort_level": "medium",
      "confidence": 0.88
    }
  ]
}
```

Notes

- The component enforces one-to-many mapping: each risk may yield multiple mitigation strategies.
- Mitigations must be specific, non-generic, and tied directly to the originating risk text and theme classification.
- The pipeline requires that every mitigation contains:
  - A valid risk_id
  - At least one actionable step
  - A normalized effort level (low, medium, high)
  - A confidence score aligned with the scoring engine
-These records are used by the Report Builder and Summary Generator to create consistent leadership-ready deliverables.

