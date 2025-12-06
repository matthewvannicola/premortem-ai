# PreMortem AI — Canonical Data Model Layer

The `premortem_ai.models` package defines the **canonical, schema-aligned,
version-governed data models** used across the entire PreMortem AI system.
These models form the public, stable contract between:

- LLM inference modules  
- discovery + scoring engines  
- mitigation generation  
- orchestrator execution  
- REST/CLI API interfaces  
- downstream reporting (PDF, Docs, Notion)  
- SDK consumers and external integrators  

This layer ensures **deterministic, strict, and forward-compatible behavior**
across all pipeline stages.

---

## Design Principles

### **1. CanonicalModel Base Class**
All models inherit from `CanonicalModel`, which enforces:

- **strict schema validation** (`extra="forbid"`)
- **immutability** (`frozen=True`)
- **deterministic serialization** (`model_dump()` output is stable)
- **assignment validation** (no silent type coercion)
- **namespace cleanliness** (no unknown fields accepted)
- **version tagging** (`model_version = "1.0.0"`)

This creates reliability guarantees similar to enterprise platforms like  
OpenAI’s model contracts, Stripe’s API models, or AWS service models.

---

### **2. JSON Schema Alignment**

Each model has a corresponding JSON Schema located in `schema/`:

| Model | Schema |
|-------|--------|
| `RiskItem` | `risk_item.schema.json` |
| `ScoreItem` | `score_item.schema.json` |
| `ThemeItem` | `theme_item.schema.json` |
| `MitigationItem` | `mitigation_item.schema.json` |
| `MitigationAction` | *nested schema inside mitigation* |
| `Summary` | `summary.schema.json` |
| `Metadata` | `metadata.schema.json` |
| `RiskReport` | `risk_report.schema.json` |
| `PipelineRequest` | `pipeline_request.schema.json` |
| `PipelineResponse` | `pipeline_response.schema.json` |

Schemas and models intentionally mirror each other to:

- support automated validation  
- maintain stable public contracts  
- support code generation (future)  
- enable regression detection  

---

### **3. Deterministic Normalization Pipeline**

All free-form text fields (titles, descriptions, narratives, rationales,
recommendations, mitigation steps, etc.) pass through the centralized
`normalize_text()` function before becoming part of any model.

This ensures:

- stable hashing / fingerprints  
- reproducible executions  
- consistent grouping + clustering  
- noise reduction during LLM reasoning  

---

### **4. Cross-Reference Validation**

`RiskReport` performs deep validation to ensure:

- every `ScoreItem.risk_id` references a real `RiskItem`
- every `ThemeItem.risk_ids[*]` is valid
- every `MitigationItem.risk_ids[*]` is valid

This prevents downstream corruption in:

- summaries  
- dashboards  
- PDFs/Docs  
- analytics  

Broken references are rejected at model-construction time.

---

### **5. Immutability and Safety Guarantees**

All canonical models are **frozen**, meaning once constructed:

- fields cannot be mutated  
- references cannot drift  
- hashability becomes stable  
- downstream caches and fingerprints are safe  

This mirrors practices in production-grade ML + risk-analysis systems.

---

## Module Overview

### **RiskItem**
Represents one discovered risk.  
Includes normalization, ID auto-assignment, and structural validation.

### **ScoreItem**
Likelihood × impact scoring.  
Includes severity consistency enforcement.

### **ThemeItem**
Cluster of related risks.  
Enforces grouping logic and uniqueness constraints.

### **MitigationItem + MitigationAction**
Structured, ordered mitigation plans with validation of steps and references.

### **Summary**
Executive human-readable narrative, top risks, and optional recommendations.

### **Metadata**
Execution-context metadata, timestamps, versions, fingerprints.

### **RiskReport**
Top-level aggregation for the entire system.  
Performs cross-reference validation and deterministic serialization.

### **PipelineRequest / PipelineResponse**
Stable public API contracts.  
Normalize inputs and wrap outputs safely.

---

---

## Canonical Model Architecture Diagram

Below is a high-level overview of how canonical models flow through the
PreMortem AI pipeline:

```
PipelineRequest ──▶ Discovery Engine ──────▶ RiskItem[]
                      │
                      ▼
                 Scoring Engine ───────────▶ ScoreItem[]
                      │
                      ▼
                 Theme Clusterer ─────────▶ ThemeItem[]
                      │
                      ▼
             Mitigation Generator ─────────▶ MitigationItem[]
                      │
                      ▼
                    Summarizer ───────────▶ Summary
                      │
                      ▼
                Metadata Collector ───────▶ Metadata
                      │
                      ▼
               RiskReport Assembler ──────▶ RiskReport
                      │
                      ▼
               API / SDK Wrapper ─────────▶ PipelineResponse
```


This diagram reflects the **canonical, validated, and deterministic flow**
guaranteed by the model layer.

---

## Example Usage

### Creating a RiskItem:

```python
from premortem_ai.models import RiskItem

risk = RiskItem(
    risk_id="risk-00001",
    title="API ownership unclear",
    description="No defined maintainer or escalation path.",
    category="Delivery"
)
```

### Building a full RiskReport:

```python
from premortem_ai.models import (
    RiskItem, ScoreItem, ThemeItem,
    MitigationItem, Summary, Metadata, RiskReport
)

report = RiskReport(
    risks=[...],
    scores=[...],
    themes=[...],
    mitigations=[...],
    summary=summary_obj,
    metadata=metadata_obj,
)
```

### Serializing deterministically:

```python
payload = report.model_dump()
```

This output is guaranteed stable across runs and compatible with the JSON Schema.

---

## Versioned Public API Surface

All models exposed via:

```python
from premortem_ai.models import *
```

are considered part of the public, governed, versionable interface of the PreMortem AI system.

Breaking changes require a semver bump and migration notes.

---

---

## Forward & Backward Compatibility Guarantees

The canonical model layer is designed with long-term stability in mind.

### **Backward Compatibility**
Older serialized reports remain readable because:

- all new fields must be optional or additive  
- `CanonicalModel` forbids breaking-field removals  
- deterministic parsing ensures no implicit data shifts  

### **Forward Compatibility**
Future versions of the pipeline can safely read older model versions due to:

- strict JSON Schema alignment  
- version-tagged canonical models  
- clearly governed public API boundaries  

These guarantees make canonical models suitable for:

- historical risk trend analysis  
- audit logs  
- regulatory/compliance reporting  
- reproducible research workflows  

---

## Model Validation & Invariant Tests

The integrity and stability of the canonical model layer is verified through
a suite of automated tests located in:

```
test/models/
```


These tests enforce:

- schema alignment  
- deterministic serialization  
- cross-reference integrity (e.g., ScoreItem → RiskItem)  
- normalization consistency  
- immutability behavior  
- regression protection for public API changes  

Before modifying or introducing new models, developers should run:

```bash
pytest tests/models -q
```

---

## Why Canonical Models Instead of Free-Form Dictionaries?

PreMortem AI enforces strict canonical models rather than unstructured
Python dictionaries. This provides several critical advantages:

### **1. Deterministic Behavior**
All models normalize text, validate constraints, and serialize identically
across environments → essential for reproducibility.

### **2. Safety & Governance**
Invalid fields, unexpected shapes, or corrupted references are rejected
early via strict validation (`extra="forbid"`).

### **3. Stability for Integrators**
External consumers rely on stable, versioned contracts — identical to how
platforms like OpenAI, AWS, and Stripe structure their API models.

### **4. Cross-Module Guarantees**
Strong typing prevents:

- broken risk references  
- missing or malformed summaries  
- invalid scoring formulas  
- misaligned mitigations  

### **5. Future-Proofing**
Canonical models allow:

- schema-driven code generation  
- UI form generation  
- validation in any language  
- long-term auditability  

This approach turns the model layer into a *governed infrastructure tier*,
not just a serialization convenience.

---

## Extending the Model Layer

To add a new canonical model:
1. Create a JSON Schema in `schema/`
2. Create a corresponding Python model inheriting from `CanonicalModel`
3. Ensure deterministic behavior (text normalization, validators)
4. Add the model to `__init__.py`
5. Add tests ensuring:
   - schema alignment
   - serialization format
   - invariants
  
---

## Summary

This package is the backbone of the PreMortem AI system.
It provides:

- strict data integrity
- reliable cross-module communication
- deterministic replays + reproducibility
- safe API boundaries
- schema versioning
- testable, governed domain contracts

Treat this folder as a core infrastructure module — stable, reliable, high-assurance, and foundational.
