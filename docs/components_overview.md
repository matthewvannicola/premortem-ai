# Components Overview

This document provides a high-level description of all major components in the PreMortem AI system.  
Each component is independently testable, schema-validated, and designed for deterministic behavior across environments.

The system is composed of five primary layers:

1. **Input Normalization & Validation**
2. **Risk Discovery Engine**
3. **Scoring Engine**
4. **Theme Generator**
5. **Mitigation Generator**
6. **Summary Synthesizer**
7. **Schema & Determinism Framework**
8. **API Layer**

Each section below explains the purpose, inputs, outputs, and constraints of its respective component.

---

## 1. Input Normalization & Validation

### Purpose:

Ensures all incoming free-form text is transformed into a stable, machine-compatible form prior to LLM inference.

### Responsibilities:

- Unicode normalization (NFKC)
- Whitespace collapsing
- Removal of invisible/zero-width characters
- Type coercion to strings
- Safety trimming (length boundaries)
- Initial input validation

### Inputs:

```text
project_description: string (raw)
```

### Outputs:

```text
normalized_description: string (stable, deterministic)
```

### Determinism Guarantees:

Identical input text produces identical normalized output across all environments.

---

## 2. Risk Discovery Engine

### Purpose:

Extracts canonical `Risk` entities from unstructured language using a structured extraction prompt and schema validation.

### Responsibilities:

- Multi-risk extraction from free-form text
- Enforcing required fields (title, description, category)
- Assigning deterministic `risk_id` values
- Rejecting malformed outputs via schema validation

### Inputs:

```json
{
  "project_description": "<normalized text>"
}
```

### Outputs:

```json
{
  "risks": [ ...canonical Risk entities... ]
}
```

### Constraints:

- No duplicated risk titles
- Titles must be 1–2 sentences
- Categories must belong to the predefined taxonomy

---

## 3. Scoring Engine

### Purpose:

Assigns likelihood, impact, and severity to each discovered risk.

### Responsibilities:

- Normalize scoring language into stable numerical values
- Compute deterministic severity = likelihood × impact
- Generate rationale text
- Validate scoring object against schema

### Inputs:

```json
{ "risks": [ ... ] }
```

### Outputs:

```json
{ "scores": [ ...canonical Score entities... ] }
```

### Constraints:

- Likelihood ∈ [1,5]
- Impact ∈ [1,5]
- Severity must be computed, not inferred

---

## 4. Theme Generator

### Purpose:

Identify systemic patterns across risks and scores, producing higher-level `Theme` clusters.

### Responsibilities:

- Cluster related risks into thematic categories
- Enforce uniqueness of theme labels
- Validate membership lists
- Generate deterministic `theme_id` values

### Inputs:

```json
{
  "risks": [...],
  "scores": [...]
}
```

### Outputs:

```json
{
  "themes": [ ...canonical Theme entities... ]
}
```

### Determinism Guarantees:

Theme grouping logic ensures stable ordering and ID assignment for identical inputs.

---

## 5. Mitigation Generator

### Purpose:

Generate actionable, testable, and realistic mitigation steps for each risk/theme grouping.

### Responsibilities:

- Produce imperative action lists
- Ensure relevance to referenced risks/themes
- Enforce schema constraints
- Assign deterministic `mitigation_id` values

### Inputs:

```json
{
  "risks": [...],
  "scores": [...],
  "themes": [...]
}
```

### Outputs:

```json
{
  "mitigations": [ ...canonical Mitigation entities... ]
}
```

### Constraints:

- Actions must be testable (“Establish weekly sync checkpoints”), not vague (“Improve communication”).

---

## 6. Summary Synthesizer

### Purpose:

Produce an executive-level narrative and overall project health score.

### Responsibilities:

- Compute health score from aggregated scoring metrics
- Identify top risks
- Generate concise narrative text
- Validate structure via `summary.schema.json`

### Inputs:

```json
{
  "risks": [...],
  "scores": [...],
  "themes": [...],
  "mitigations": [...]
}
```

### Outputs:

```json
{
  "summary": { "health_score": <int>, "top_risks": [...], "narrative": "<string>" }
}
```

### Constraints:

- Narrative must remain concise and schema-bounded
- Health score must be deterministic

---

## 7. Schema & Determinism Framework

### Purpose:

Ensure all components produce machine-valid, deterministic, and reproducible output.

### Responsibilities:

- JSON Schema enforcement
- Stable ID generation
- Stable ordering of arrays and fields
- Zero-tolerance rejection of malformed model outputs
- Canonicalization of all entity types into strict shapes

### Guarantees:

- No nondeterministic ordering
- No inconsistent ID formatting
- No unvalidated payloads entering downstream components

---

## 8. API Layer

### Purpose:

Expose each pipeline component (and the full pipeline) through stable, versioned endpoints.

### Responsibilities:

- Serve `/analysis` (full pipeline)
- Serve modular endpoints (`/analysis/discovery`, `/analysis/score`, etc.)
- Apply authentication policies
- Surface structured error responses
- Enforce rate limits (optional)
- Maintain stable `/api/v1` contract

### Outputs:

Deterministic, schema-validated responses that conform to:

- `risk_item.schema.json`
- `score_item.schema.json`
- `theme_item.schema.json`
- `mitigation_item.schema.json`
- `summary.schema.json`
- `risk_report.schema.json`

---

## Summary

The system is designed as a deterministic, schema-driven, multi-stage pipeline where each component is independently testable and produces stable outputs. Together, these components form the foundation of PreMortem AI’s automated risk-analysis capability.
