# API Reference

This document defines the input contracts, output formats, schema expectations, and processing guarantees for the PreMortem AI automation pipeline.

All components follow strict validation rules to ensure deterministic, machine-readable behavior.

---

## 1. Input Specification

PreMortem AI accepts a single project brief containing:

```json
{
  "project_title": "string (required)",
  "description": "string (required)",
  "team_context": "string (optional)",
  "timeline": "string (optional)",
  "additional_notes": "string (optional)"
}
```

---

## 2. Output Specification (Primary Risk Dataset)

All LLM passes must return structured JSON matching the following schema.

This is validated against:

```
schemas/risk_output.schema.json
```

### Expected Output Structure

```json
{
  "risk_id": "string",
  "category": "Technical | Operational | Product | Organizational",
  "description": "string",
  "probability": "Low | Medium | High",
  "impact": "Low | Medium | High",
  "severity": "integer (1–5)",
  "recommendation": "string"
}
```

### Field Requirements

- **risk_id** — auto-generated UUID-like identifier  
- **category** — normalized enum value  
- **description** — LLM-generated risk explanation  
- **probability / impact** — strictly validated enums  
- **severity** — deterministic integer computed by severity engine  
- **recommendation** — action-oriented mitigation guidance  

### Output Guarantees

- All enum fields are normalized before scoring  
- JSON must strictly match schema (no extra or missing fields)  
- Severity is computed deterministically on every run  
- All risks in the output dataset must have unique IDs  
- The LLM may not add, rename, or reorder required fields  

---

## 3. Summary Output

The Summary Pass produces a high-level aggregated report used for executive visibility and downstream reporting.

### Expected Structure

```json
{
  "overall_risk_level": "Low | Medium | High",
  "key_themes": ["string"],
  "executive_summary": "string"
}
```

### Field Definitions

- **overall_risk_level**  
  A synthesized evaluation of total system/project risk based on severity distribution.

- **key_themes**  
  A list of recurring patterns or systemic issues identified across all risks.

- **executive_summary**  
  A concise narrative summarizing the project’s major risk areas, written in leadership-friendly language.

### Guarantees

- The Summary Pass always returns a valid JSON object.  
- `overall_risk_level` must be one of the defined enums.  
- `key_themes` must always be an array (even if only one item exists).  
- No additional fields are permitted.  

---

## 4. Reporting Output

The Reporting Engine consolidates all validated LLM outputs into final deliverables suitable for stakeholders, leadership, or downstream automation.

### Generated Artifacts

- **Google Doc** — formatted executive report  
- **PDF export** — finalized, non-editable version  
- **JSON dataset** — machine-readable risk objects and summary fields  

All three outputs are generated in a single execution run and stored according to environment configuration.

---

### Metadata Structure

Each execution includes a metadata object describing the environment, retry behavior, and model usage:

```json
{
  "run_id": "uuid",
  "timestamp": "ISO-8601",
  "retry_count": "integer",
  "model_used": "gpt-5.1 | gpt-4.1 fallback",
  "pipeline_version": "string (e.g., v1.3.0)"
}
```

### Reporting Guarantees

- Reports are generated **only after all JSON passes validation**  
- Metadata is logged to Notion (see audit log spec)  
- PDF and Google Doc exports always reflect the **same underlying dataset**  
- Fallback model usage is recorded for traceability  
- Reports cannot be produced from partially valid datasets  

---

## 5. Error Handling & Retries

PreMortem AI uses strict schema validation, deterministic retry behavior, and model fallback logic to ensure reliable execution.

---

### A. Schema Validation Failures

If LLM output does not match the expected schema:

1. **Auto-correction attempt** is applied  
2. **Re-inference** is performed using the same model  
3. If failures persist, the system switches to the **fallback model**

Example failure types:

- Malformed JSON  
- Missing required fields  
- Invalid enum values  
- Empty arrays or objects  
- Mis-typed field names  

All failures are logged to the audit layer.

---

### B. Hard Failure Conditions

A run is considered irrecoverable if:

- All retries AND the fallback model fail validation  
- Summary output is incomplete  
- Severity computation cannot be performed  
- Report export fails due to invalid dataset  

In this scenario:

- The run is marked **failed**  
- Partial output is captured for debugging  
- All metadata is logged for traceability  

---

### C. Guarantees

- No invalid data moves to the reporting layer  
- Retries are deterministic (max retries defined in configuration)  
- Fallback model is ALWAYS lower-cost + high-reliability  
- All errors produce structured audit entries  

---

## 6. Fallback Logic

PreMortem AI uses a tiered model strategy to maintain reliability and control execution costs.

If the primary model (`MODEL_PRIMARY`, typically GPT-5.1) fails to produce a valid schema-matching response after the configured retry limit, the system automatically falls back to a lower-cost, high-stability model (`MODEL_FALLBACK`, typically GPT-4.1).

---

### Fallback Sequence

```
Primary Model (GPT-5.1)
     ↓ fails after MAX_RETRIES
Fallback Model (GPT-4.1)
     ↓ retries inference → validate JSON
Success → continue pipeline
Failure → abort run + log to audit
```

---

### Design Principles

- **Resilience** — pipeline continues even if a model misbehaves  
- **Determinism** — fallback behavior is strictly defined and repeatable  
- **Cost Control** — expensive models only retry within their configured limit  
- **Traceability** — fallback activation is always recorded in metadata and audit logs  

---

### Guarantees

- Fallback is never triggered unless schema mismatch persists  
- All retries follow explicit configuration parameters  
- Audit logs record which model produced each inference pass  
- Reporting outputs always reflect the **final successfully validated dataset**

---

## 7. Execution Contract

The execution contract defines the conditions under which a pipeline run is considered **successful**, **recoverable**, or **failed**.  
This ensures deterministic behavior and consistent expectations across all components.

---

### A. Success Conditions

A run is marked **successful** when all of the following are true:

- All LLM passes produce **schema-valid JSON**  
- Auto-correction (if triggered) results in a valid dataset  
- Severity computation completes without errors  
- Summary output is fully populated and validated  
- All reporting artifacts (Google Doc, PDF, JSON) are generated  
- Audit logging to Notion completes successfully  
- Metadata for the run is stored without truncation  

These guarantees ensure the run can be trusted for decision-making and reporting.


---

### B. Recoverable Conditions

A run is considered **recoverable** when:

- Primary model fails but fallback model succeeds  
- One or more retries succeed after initial failure  
- Minor normalization issues are automatically corrected  
- Reporting artifacts succeed on retry after transient errors  

Recoverable runs are logged with appropriate flags for traceability.

---

### C. Failure Conditions

A run is marked **failed** when:

- Both primary and fallback models fail schema validation  
- JSON output cannot be corrected after retries  
- Severity calculation cannot be performed  
- Summary output is incomplete or missing required fields  
- Reporting fails repeatedly (e.g., PDF/Doc generation errors)  
- Audit logging fails in a way that prevents metadata capture  

All failures produce a structured error object for debugging and compliance.


---

### D. Guarantees

- No invalid or partially valid data proceeds into reporting  
- All outcomes (success, recoverable, failure) are explicitly logged  
- Execution behavior is deterministic and does not depend on model variance  
- The pipeline never "silently" completes with corrupted data  

---

## 8. Versioning

PreMortem AI captures version information for every run to ensure reproducibility, auditability, and compatibility across evolving models, schemas, and pipeline logic.

Version metadata is stored alongside the final dataset and audit log entries.

---

### A. Model Versioning

Each inference pass records:

- **Model name** (e.g., gpt-5.1, gpt-4.1)  
- **Version identifier** (as exposed by provider)  
- **Fallback usage** (true/false)  

Model versions allow teams to:

- Compare outputs from different model generations  
- Detect model drift  
- Reproduce historical runs when needed  

---

### B. Schema Versioning

Every validated output uses a specific schema version:

```
schemas/risk_output.schema.json (v1.x.x)
```

Schema versions enable:

- Backwards compatibility  
- Controlled schema changes  
- Enforcement of strict field requirements  
- Reliable parsing for downstream automation  

---

### C. Pipeline Versioning

Each execution includes a `pipeline_version` field representing the version of:

- Normalization logic  
- Retry behavior  
- Fallback rules  
- Scoring algorithms  
- Reporting functions  

This prevents mismatched data when pipeline logic evolves.

---

### D. Audit Log Versioning

All version information is stored in the audit layer:

```json
{
  "model_version": "string",
  "schema_version": "string",
  "pipeline_version": "string",
  "timestamp": "ISO-8601"
}
```

This gives enterprises:

- Full run lineage  
- Compliance-ready traceability  
- Forensic debugging capability  
- Confidence in historical data integrity  

---

### E. Guarantees

- Every run is fully reproducible when paired with its version metadata  
- Changes to schema or logic never silently break the pipeline  
- Version conflicts are surfaced during validation  
- Reporting outputs always reflect the versioned logic used during generation  

---

# End of Document
