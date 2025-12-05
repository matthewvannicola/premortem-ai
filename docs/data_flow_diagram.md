# PreMortem AI — Data Flow Diagram

This document provides a detailed view of how PreMortem AI transforms raw, unstructured project context into a fully structured, validated `RiskReport`.
The pipeline emphasizes determinism, schema integrity, traceability, and repeatable LLM-augmented inference across every stage.

Each stage produces a contract-bound artifact that is consumed by downstream components, ensuring a reliable and auditable flow from input to final report generation.

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

# 2. Detailed Stage-by-Stage Flow

Each stage includes:
- Input contract
- LLM interaction (if applicable)
- Normalization + schema validation
- Output artifact passed downstream

# 2.1 Discovery Stage

Input:
  - `project_description` (string)

LLM Interaction:
  - structured extraction → JSON array of risk candidates

Core Processing:
  - normalization
  - ID generation (`risk-xxxxx`)
  - schema validation `risk_item.schema.json`

Output:
  `risks[]` — an array of typed, canonical risk objects

# 2.2 Scoring Stage

Input:
  - `risks[]`

Processing

- Hybrid scoring model combining:
  - deterministic likelihood / impact rules
  - LLM-assisted contextual weighting
- Aggregation of severity scores
- Validation against `scoring.schema.json`

Output:
  `scores[]` — probability, impact, and severity metadata for each risk

# 2.3 Themes Stage

Input:
  - `risks[]`
  - `scores[]`

LLM Interaction:
  - thematic clustering via structured prompt

Processing

- `theme-xxxxx` ID generation
- Membership mapping (risk_ids → themes)
- Schema validation

Output:
  `themes[]` — cross-risk abstraction layer enabling leadership interpretation


# 2.4 Mitigation Stage

Input:
  - `risks[]`
  - `scores[]`
  - `themes[]`

LLM Interaction:
  - Strict JSON-only generation of mitigation strategies aligned to individual risks and themes

Processing:
  - Normalization and de-duplication of generated actions
  - Validation against `mitigation.schema.json`

Output:
  `mitigations[]` — actionable risk-response guidance

# 2.5 Summary Stage

Input:
  - `risks[]`
  - `scores[]`
  - `themes[]`
  - `mitigations[]`

LLM Interaction:
  - Executive-level narrative synthesis representing the overall project risk posture

Processing

- Health score calculation
- Prioritization of top-risk narratives
- Validation against `summary.schema.json`

Output:
  `summary{}` — high-level, human-readable project risk summary

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
All fields undergo a final validation pass against `risk_report.schema.json` to ensure structural integrity, contract fidelity, and safe downstream consumption.

---

# 4. Error Handling & Recovery

The pipeline is designed for reliability under imperfect LLM outputs and enforces strict operational safeguards:

- Automatic retry logic for malformed or incomplete JSON
- Fail-fast enforcement on schema violations
- Deterministic fallback scoring pathways
- Full traceability of intermediate artifacts for auditability and debugging
- Logging of LLM prompts, responses, normalization steps, and validation results

These controls ensure predictable behavior across inference runs and prevent propagation of corrupted artifacts.

---

# 5. Data Provenance

PreMortem AI maintains an immutable lineage for every generated artifact:

- All intermediate objects (risks, scores, themes, mitigations, summary) are logged and version-tracked
- Every LLM-created output is normalized, validated, and replayable
- Inputs, prompts, schema versions, and runtime metadata are preserved for auditability
- Deterministic transformations guarantee reproducible outputs for identical inputs

This provenance model ensures enterprise-grade transparency and compliance with internal governance, quality assurance, and regulatory expectations.

---

# Summary

This data flow architecture provides a rigorous, transparent, and fully auditable pipeline that transforms unstructured project descriptions into rich, structured risk intelligence.
Through deterministic processing, schema-based validation, and carefully constrained LLM interactions, PreMortem AI delivers repeatable, enterprise-safe analysis designed for real-world engineering, product, and leadership workflows.
