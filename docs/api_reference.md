# PreMortem AI — API Reference

The PreMortem AI API exposes a deterministic, schema-validated interface for generating structured risk intelligence from unstructured project descriptions.
All endpoints return strict JSON and conform to the domain entities defined in:

- `docs/domain_model.md`
- `docs/risk_model.md`
- `schemas/*.schema.json`
- `docs/data_flow_diagram.md`

This API reference describes the request/response formats, validation rules, error models, and versioning strategy for all supported endpoints.

## 1. Base URL & Versioning

The PreMortem AI API is organized under a stable, versioned namespace to ensure long-term compatibility for all clients.

### Base URL:

```
/api/v1
```

### Content Types:

```
Accept:       application/json
Content-Type: application/json
```

### Versioning Strategy:

The API follows a semantic, non-breaking versioning model:

- v1 defines the stable contract for all current endpoints.
- Additive changes (e.g., new fields, metadata) may be introduced within v1 as long as they are backward compatible.
- Any contract-breaking change requires a new major version (`v2`, `v3`, etc.).
- JSON Schemas (`schemas/*.schema.json`) serve as the authoritative definition for all response shapes.

---

## 2. Authentication

Authentication controls access to the PreMortem AI API in production environments.
Local development workflows may disable authentication entirely.

### Authorization Header:

```
Authorization: Bearer <token>
```

### Token Requirements:

- Tokens must be valid, non-expired, and issued by the deployment environment.
- Tokens grant access to all `v1` endpoints unless additional role-based policies are configured.
- Requests without a valid token return `401 unauthorized`.

### Local & Development Environments:

For local development or internal automation pipelines, authentication may be disabled.
When disabled:

- Requests do not require an Authorization header
- Behavior of all endpoints remains identical
- Deterministic outputs and schema guarantees remain fully enforced

### Example (authenticated call):

```
POST /api/v1/analysis
Authorization: Bearer eyJhbGciOiJIUzI1NiIsIn...
Content-Type: application/json
```

### Example (unauthenticated local call):

```
POST /api/v1/analysis
Content-Type: application/json
```

### Failure — 401 Unauthorized:

```
{
  "error": "unauthorized",
  "message": "A valid authentication token is required for this endpoint.",
  "details": {}
}
```

---

## 3. Endpoints Overview

The PreMortem AI API exposes a set of structured, schema-validated endpoints that correspond to each stage of the risk-analysis pipeline.  
All endpoints use **JSON request/response bodies**, enforce strict schema validation, and follow deterministic ID and ordering guarantees.

| Endpoint               | Method | Description                                                      |
|------------------------|--------|------------------------------------------------------------------|
| `/analysis`            | POST   | Executes the full pipeline and returns a complete `RiskReport`.  |
| `/analysis/discovery`  | POST   | Extracts canonicalized `Risk` entities from unstructured text.   |
| `/analysis/score`      | POST   | Computes likelihood, impact, and severity scoring for risks.     |
| `/analysis/themes`     | POST   | Generates systemic `Theme` groupings from risks and scores.      |
| `/analysis/mitigations`| POST   | Produces structured mitigation recommendations.                  |
| `/analysis/summary`    | POST   | Generates the executive summary and overall health score.        |
| `/health`              | GET    | Returns service, schema, and model version diagnostics.          |

### Design Principles:

- **Deterministic Output:** Identical inputs across environments produce identical structured outputs.  
- **Schema Enforcement:** All responses conform to the JSON Schemas in `schemas/*.schema.json`.  
- **Composable Stages:** Each endpoint aligns with a pipeline component and can be called independently.  
- **Full-Pipeline Convenience:** `/analysis` executes the entire pipeline and returns a complete `RiskReport`.

---

## 4. POST /analysis

Executes the entire PreMortem AI pipeline and returns a complete `RiskReport`

### Request:

```json
{
  "project_description": "We are integrating a new vendor API but ownership is unclear..."
}
```

### Response — 200 OK:

```json
{
  "risks": [...],
  "scores": [...],
  "themes": [...],
  "mitigations": [...],
  "summary": { ... },
  "metadata": {
    "generated_at": "2025-01-12T18:04:00Z",
    "model_version": "gpt-5.1",
    "schema_version": "1.0.0",
    "pipeline_run_id": "run-000340"
  }
}
```

### Validation Rules:

- `project_description` must be a non-empty string
- All generated artifacts must validate against their respective schemas
- Deterministic ID and ordering guarantees enforced

### Failure — 400 Bad Request:

```json
{
  "error": "invalid_input",
  "message": "project_description must be a non-empty string",
  "details": {}
}
```

---

## 5. POST /analysis/discovery

Extracts, normalizes, and validates Risk entities.

### Request:

```json
{
  "project_description": "Ownership unclear for the data validation subsystem..."
}
```

### Response — 200 OK:

```json
{
  "risks": [
    {
      "risk_id": "risk-00001",
      "title": "Undefined ownership of validation subsystem",
      "description": "The project lacks a clearly assigned owner for validation services.",
      "category": "organizational",
      "source_text": "Ownership unclear..."
    }
  ],
  "metadata": {
    "model_version": "gpt-5.1",
    "schema_version": "1.0.0"
  }
}
```

### Validation Rules:

- Strict JSON extraction
- Category must match allowed taxonomy
- IDs assigned deterministically after normalization

### Failure — 422 Unprocessable Entity:

```json
{
  "error": "schema_violation",
  "message": "One or more extracted risks failed schema validation.",
  "details": { "path": "risks[0].category" }
}
```

---

## 6. Post /analysis/score

Computes likelyhood, impact, and severity for each risk

### Request:

```json
{
  "risks": [
    {
      "risk_id": "risk-00001",
      "title": "Undefined API ownership",
      "description": "No designated owner for API integration workstream.",
      "category": "organizational"
    }
  ]
}
```

### Response — 200 OK:

```json
{
  "scores": [
    {
      "risk_id": "risk-00001",
      "likelihood": 4,
      "impact": 5,
      "severity": 20,
      "rationale": "Ownership gaps significantly increase delivery uncertainty."
    }
  ]
}
```

### Validation Rules:

- Likelyhood/Impact must be integers 1–5
- Severity must be deterministically derived
- `risk_id` must exist in input payload

### Failure — 400 Bad Request:

```json
{
  "error": "invalid_input",
  "message": "Missing or malformed risk entries.",
  "details": {}
}
```

---

## 7. POST /analysis/themes

Clusters risks into systemic **Theme** categories

### Request:

```json
{
  "risks": [...],
  "scores": [...]
}
```

### Response — 200 OK:

```json
{
  "themes": [
    {
      "theme_id": "theme-00001",
      "label": "Execution Readiness Gaps",
      "description": "Patterns involving unclear ownership and planning gaps.",
      "risk_ids": ["risk-00001", "risk-00002"]
    }
  ]
}
```

### Validation Rules:

- Themes must contain ≥1 risk
- No theme may duplicate risk titles
- Membership lists must be stable for deterministic runs

### Failure — 422 Unprocessable Entity:

```json
{
  "error": "llm_malformed_output",
  "message": "Theme generation produced invalid JSON.",
  "details": {}
}
```

---

## 8. POST /analysis/mitigations

Produces structured, actionable mitigation guidance

### Request:

```json
{
  "risks": [...],
  "scores": [...],
  "themes": [...]
}
```

### Response — 200 OK:

```json
{
  "mitigations": [
    {
      "mitigation_id": "mitigation-00007",
      "title": "Assign API integration owner",
      "actions": [
        "Designate a technical DRI.",
        "Publish ownership matrix.",
        "Establish weekly sync checkpoints."
      ],
      "risk_ids": ["risk-00001"],
      "theme_ids": ["theme-00001"]
    }
  ]
}
```

### Validation Rules:

- Actions must be imperative + testable
- No vague recommendations allowed
- Conforms to `mitigation.schema.json`

### Failure — 422 Unprocessable Entity:

```json
{
  "error": "schema_violation",
  "message": "Mitigation output failed validation.",
  "details": {}
}
```

---

## 9. POST /analysis/summary

Generates the executive summary narrative and overall project health score.

### Request:

```json
{
  "risks": [...],
  "scores": [...],
  "themes": [...],
  "mitigations": [...]
}
```

### Response — 200 OK:

```json
{
  "summary": {
    "health_score": 72,
    "top_risks": ["risk-00001"],
    "narrative": "The project faces execution risks due to unclear ownership..."
  }
}
```

### Validation Rules:

- `health_score` must follow deterministic formula
- Narrative must remain within schema length bounds
- Must reference themes, not raw risks

### Failure — 500 Internal Error:

```json
{
  "error": "pipeline_failure",
  "message": "Summary synthesis failed.",
  "details": {}
}
```

---

## 10. GET /health

Returns real-time service diagnostics.

### Response — 200 OK:

```json
{
  "status": "ok",
  "model_version": "gpt-5.1",
  "schema_version": "1.0.0",
  "uptime_seconds": 532842
}
```

---

## 11. Error Model

All endpoints return errors using a unified, machine-consumable structure.  
Errors are **never returned as plain text** and always follow the schema below.

### Error Object (Canonical Structure):

```json
{
  "error": "string_enum",
  "message": "Human-readable explanation of the failure.",
  "details": {}
}
```

### Fields:

| Field      | Type   | Description                                                             |
|------------|--------|-------------------------------------------------------------------------|
| `error`    | string | Stable error code used for programmatic handling.                       |
| `message`  | string | Human-readable explanation intended for operators or developers.        |
| `details`  | object | Optional structured metadata (e.g., schema paths, invalid fields).      |

---

### Common Error Codes:

| Code                   | Meaning                                                                 |
|------------------------|-------------------------------------------------------------------------|
| `invalid_input`        | Request body is missing required fields or contains invalid types.      |
| `schema_violation`     | Output from LLM/pipeline failed JSON Schema validation.                 |
| `llm_malformed_output` | Model returned non-parseable or structurally invalid JSON.              |
| `pipeline_failure`     | A downstream processing step failed unexpectedly.                       |
| `unauthorized`         | Request missing valid authentication token.                             |
| `rate_limited`         | Too many requests within the configured rate window.                    |
| `internal_error`       | Unhandled exception or unexpected server condition.                     |

---

### Example — Invalid Input (400):

```json
{
  "error": "invalid_input",
  "message": "project_description must be a non-empty string.",
  "details": {}
}
```

### Example — Schema Violation (422):

```json
{
  "error": "schema_violation",
  "message": "Extracted risk item did not match risk_item.schema.json.",
  "details": {
    "path": "risks[0].category",
    "expected": ["organizational", "technical", "operational"],
    "received": "org"
  }
}
```

### Example — LLM Malformed Output (422):

```json
{
  "error": "llm_malformed_output",
  "message": "The model returned invalid JSON during theme generation.",
  "details": {
    "raw_output": "<model text here>"
  }
}
```

### Example — Unauthorized (401):

```json
{
  "error": "unauthorized",
  "message": "A valid authentication token is required for this endpoint.",
  "details": {}
}
```

### Determinism & Stability Guarantees:

- Error codes remain stable across all minor versions within the same major API version.
- Additional fields may be added to `details` but will never break existing clients.
- All error responses are guaranteed to be valid JSON.
- The API never returns HTML error payloads or non-JSON responses.
- Pipeline failures always surface as `pipeline_failure` instead of ambiguous 500-series errors.

### Client Handling Guidance

- Use the error code for branching logic and automated recovery.
- Use the message value for UI, logging, or operator-facing diagnostics.
- Inspect details for schema paths, validation failures, or raw model output.
- Treat internal_error as non-retryable unless accompanied by rate-limit headers.

---

## 12. Rate Limiting

Rate limits protect the service from excessive request volume and ensure fair usage across clients.  
If enabled, all rate limits apply **per authenticated token** or **per IP** (for unauthenticated local environments).

### Response Headers:

When rate limiting is active, responses include the following headers:

```text
X-RateLimit-Limit:     <maximum requests allowed per window>
X-RateLimit-Remaining: <requests remaining in the current window>
X-RateLimit-Reset:     <epoch timestamp when the window resets>
```

### Example:

```text
X-RateLimit-Limit:     60
X-RateLimit-Remaining: 54
X-RateLimit-Reset:     1707150203
```

### Behavior

- Requests exceeding the configured window return 429 Too Many Requests.
- Rate-limited responses always include a Retry-After header indicating when the client may retry.
- Rate limits may vary between environments (production vs. internal vs. local).
- Deterministic pipeline behavior remains unaffected by rate limiting.

### Failure — 429 Too Many Requests:

```json
{
  "error": "rate_limited",
  "message": "Too many requests. Please retry after the rate limit resets.",
  "details": {
    "retry_after": 12
  }
}
```

### Client Guidance:

- Always inspect `X-RateLimit-Remaining` before batching or parallelizing requests.
- Use `Retry-After` for automatic backoff.
- Treat 429 as transient — retry after the reset time.
- For heavy workloads, consider using the `/analysis` endpoint rather than multiple staged calls.

---

## 13. Schema Registry

All API responses are validated against the JSON Schemas stored in the `schemas/` directory.  
These schemas define the **authoritative contract** for every entity in the PreMortem AI pipeline and ensure deterministic, machine-validated output across environments.

The registry serves three purposes:

1. **Validation:**  
   Every pipeline stage must emit JSON that conforms to its schema.

2. **Compatibility Guarantees:**  
   Schemas remain backward-compatible within the same major API version.

3. **Client Contract Enforcement:**  
   Programmatic clients can safely rely on field presence, types, and ordering.

---

### Schema Files:

| Schema File                   | Description |
|-------------------------------|-------------|
| `risk_item.schema.json`       | Defines the structure for canonicalized `Risk` entities. |
| `score_item.schema.json`      | Defines likelihood, impact, severity scoring rules. |
| `theme_item.schema.json`      | Defines systemic `Theme` groupings and membership. |
| `mitigation_item.schema.json` | Defines structured mitigation recommendations. |
| `summary.schema.json`         | Defines the executive summary and health scoring shape. |
| `risk_report.schema.json`     | Defines the full output contract for `/analysis`. |

All schemas follow a **strict, non-optional typing model**.  
Fields that are required in the domain model **must** be present in all API responses.

---

### Versioning:

Each schema file includes:

```json
{
  "schema_version": "1.0.0"
}
```

Schema versions follow semantic versioning:

- Minor additions (e.g., new optional fields) do not break compatibility.
- Breaking changes require a new major API version (e.g., `/api/v2`).

### Validation Enforcement:

- The server rejects malformed or incomplete responses from upstream model calls.
- `schema_violation` errors always reference a precise JSON path in `details.path`.
- Entities returned by any `/analysis/*` endpoint are guaranteed to pass schema validation.

### Deterministic Guarantees:

- Property ordering is stable and consistent across environments.
- ID formats (risk-xxxxx, theme-xxxxx, etc.) follow deterministic zero-padded integer sequences.
- All schemas prohibit nullability unless explicitly declared.

### Client Usage:

Clients may:

- Validate responses locally using any JSON Schema validator.
- Generate strongly-typed models (TypeScript, Python, Go, etc.) directly from the registry.
- Detect breaking changes by tracking differences in `schema_version`.

--- 

## 14. Summary

The PreMortem AI API provides a deterministic, schema-bound interface for converting unstructured project descriptions into fully structured risk intelligence.  
Each endpoint corresponds to a discrete pipeline stage, while `/analysis` offers a full end-to-end execution path.

The API guarantees:

- **Strict JSON Schema compliance** for all responses  
- **Deterministic ID formats and field ordering**  
- **Backward-compatible versioning** within the same major version  
- **Consistent, reproducible outputs** across environments  
- **No ambiguous or non-JSON error payloads**

The contract defined in:

- `domain_model.md`  
- `risk_model.md`  
- `schema/*.schema.json`  
- `architecture_overview.md`  
- `data_flow_diagram.md`  

forms the authoritative specification for all clients integrating with the system.

The API is suitable for:

- Automated risk discovery pipelines  
- Enterprise governance/reporting workflows  
- Programmatic ingestion into dashboards or analytics systems  
- Offline or batch execution environments  
- Human-in-the-loop auditing and decision-support tools  

As the system evolves, new capabilities may be added under the existing `/api/v1` namespace, provided they remain **fully backward compatible**.  
Any breaking changes will be introduced under a new major version.

This concludes the API Reference for PreMortem AI.
