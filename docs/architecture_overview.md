# Architecture Overview

This document provides a standalone explanation of the PreMortem AI system architecture.  
The goal is to offer a clear technical reference for engineers, reviewers, and collaborators.

---

## 1. Intake Layer

**Source:** Google Sheets  
**Trigger:** Pipedream (event-based)

- Project descriptions are entered into a structured Google Sheet template.
- Any update triggers a Pipedream workflow via the Google Sheets API.
- Input is normalized, validated, and prepared for LLM processing.

---

## 2. LLM Inference Layer

**Models:** GPT-5.1 (primary), GPT-4.1 (fallback), GPT-4o (summaries)

The system uses a **multi-pass inference pipeline**:

1. **Discovery Pass**  
   Extracts raw risk candidates from unstructured text.

2. **Scoring Pass**  
   Applies probability, impact, and severity scoring rules using deterministic logic.

3. **Summary Pass**  
   Produces an executive-ready summary for leadership.

All outputs must conform to strict JSON schemas.

---

## 3. Workflow Orchestration Layer

**Platform:** Pipedream

The orchestrator manages:

- Step-by-step execution  
- Retry rules and error handling  
- Conditional fallback models  
- Branching logic  
- Intermediate logging  

Each workflow run generates a `run_id` used for traceability.

---

## 4. Data Processing & Normalization

After each inference pass:

- JSON is validated against schemas  
- Enums are normalized  
- Improper values are clamped  
- Missing fields are auto-filled  
- Risk items are deduplicated  

Normalized data is merged into a canonical output dataset.

---

## 5. Severity Scoring Engine

Severity is calculated deterministically using:

- Probability  
- Impact  
- Category weighting (optional future expansion)  
- Rule-based overrides  

Severity values range from **1 (minimal)** to **5 (critical)**.

---

## 6. Reporting Layer

Final outputs include:

- A Google Doc report (executive-ready)
- A PDF export
- A JSON dataset
- Optional Notion log entries

Reports include:

- High-risk categories  
- The top 5 risks  
- Thematic clusters  
- Mitigation recommendations  

---

## 7. Audit Logging Layer

Each workflow execution creates:

- A `run_id`
- Timestamp metadata
- Error logs
- Retry counts
- Input + output snapshots
- Model version details

This enables:

- Traceability  
- Version comparison  
- Analytics  
- Compliance readiness  

---

## 8. End-to-End Flow Diagram (Text Version)

```
Google Sheets
↓ Trigger
Pipedream Workflow
↓ Normalize Input
LLM – Discovery Pass
↓ Schema Validation
LLM – Scoring Pass
↓ Normalization / Deduplication
LLM – Summary Pass
↓ Reporting Engine
PDF + Google Doc + JSON
↓
Notion Audit Log
```

---

# End of Document
