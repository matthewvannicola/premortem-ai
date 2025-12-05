# PreMortem AI — Data Flow Diagram

This document illustrates the end-to-end flow of data through the PreMortem AI
pipeline, from unstructured project input to the final schema-validated
`RiskReport`. Each stage produces a deterministic, validated artifact that is
consumed by the next stage.

---

# 1. High-Level Data Flow

```text
          ┌─────────────────────────────┐
          │     Project Description     │
          └─────────────────────────────┘
                       │
                       ▼
          ┌─────────────────────────────┐
          │          Discovery          │
          │       extract risks         │
          └─────────────────────────────┘
                       │
                       ▼
          ┌─────────────────────────────┐
          │           Scoring           │
          │      score + aggregate      │
          └─────────────────────────────┘
                       │
                       ▼
          ┌─────────────────────────────┐
          │            Themes           │
          │       cluster patterns      │
          └─────────────────────────────┘
                       │
                       ▼
          ┌─────────────────────────────┐
          │         Mitigation          │
          │      generate actions       │
          └─────────────────────────────┘
                       │
                       ▼
          ┌─────────────────────────────┐
          │           Summary           │
          │      synthesize output      │
          └─────────────────────────────┘
                       │
                       ▼
          ┌─────────────────────────────┐
          │        Final Report         │
          │  validated RiskReport.json  │
          └─────────────────────────────┘
```

---

# 2. Detailes Stage-by-Stage Flow

Each stage includes:
- Input contract
- LLM interaction (if applicable)
- Normalization + schema validation
- Output artifact passed downstream

# 2.1 Discovery Stage
Input:
  - project_description (string)

LLM Interaction:
  - structured extraction → JSON array of risk candidates

Core Processing:
  - normalization
  - ID generation (risk-xxxxx)
  - schema validation (risk_item.schema.json)

Output:
  risks[]

# 2.2 Scoring Stage

Input:
  - risks[]

Processing:
  - deterministic scoring rules (likelihood, impact)
  - LLM-assisted contextual scoring
  - severity aggregation
  - schema validation (scoring.schema.json)

Output:
  scores[]

# 2.3 Themes Stage

Input:
  - risks[]
  - scores[]

LLM Interaction:
  - thematic clustering via structured prompt

Processing:
  - theme ID assignment (theme-xxxxx)
  - membership mapping (risk_ids → themes)
  - schema validation

Output:
  themes[]


#2.4 Mitigation Stage

Input:
  - risks[]
  - scores[]
  - themes[]

LLM Interaction:
  - structured mitigation generation (JSON only)

Processing:
  - normalization and de-duplication
  - schema validation (mitigation.schema.json)

Output:
  mitigations[]

#2.5 Summary Stage

Input:
  - risks[]
  - scores[]
  - themes[]
  - mitigations[]

LLM Interaction:
  - executive-level narrative synthesis

Processing:
  - health score calculation
  - top-risk extraction
  - schema validation (summary.schema.json)

Output:
  summary{}

---

# 3. Final Assembly (RiskReport)

The orchestrator constructs the final output:
```
RiskReport:
  risks: [...]         # canonical risk entities
  scores: [...]        # probability / impact scoring outputs
  themes: [...]        # normalized cross-risk themes
  mitigations: [...]   # recommended actions
  summary: {...}       # executive-level narrative
  metadata: {...}      # execution + model metadata
```
All artifacts are validated against `risk_report.schema.json` to ensure structural integrity before downstream consumption.

---

# 4. Error Handling & Recovery

The pipeline supports:
- LLM retry logic (malformed JSON, incomplete fields)
- deterministic fallback scoring
- stage-level hard stops on schema violations
- full traceability of intermediate JSON artifacts

---

# 5. Data Provenance

Every domain contributes structured, validated artifacts that can be:
- logged
- audited
- reproduced
- version-controlled

Ensuring consistent behavior across all inference runs.

---

This data flow model provides a transparent, end-to-end view of how PreMortem AI transforms raw project data into structured, analyzable risk intelligence.
