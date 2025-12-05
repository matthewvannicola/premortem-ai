# Architecture Overview — PreMortem AI

PreMortem AI is a domain-driven, modular risk-analysis engine built around
deterministic processing, structured LLM inference, and strict schema
validation. The architecture is intentionally layered to ensure
predictability, auditability, and extensibility across the entire system.

The pipeline transforms an unstructured project description into a fully
structured, schema-compliant risk report through a sequence of isolated
domains (Discovery → Scoring → Themes → Mitigation → Summary).

---

# 1. Architectural Goals

### **Determinism**
Core behavior (normalization, ID generation, scoring anchors, schema
enforcement) must be fully reproducible across runs.

### **Structured LLM Interaction**
LLM calls must:
- use strict JSON schemas  
- be wrapped in deterministic validation  
- avoid free-form text leakage between pipeline stages  

### **Domain Isolation**
Each functional domain is self-contained, independently testable, and
encapsulates its own logic and prompts.

### **Auditability & Explainability**
Every output artifact is validated, versioned, and traceable.

### **Extensibility**
New models, risk rules, domains, or reporting layers can be added without
breaking the surrounding system.

---

# 2. High-Level Architecture

The architecture is composed of **five layers**:

```
┌──────────────────────────────────────────────┐
│                Reporting Layer               │
│            → Final Report (validated)        │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│           Pipeline Orchestration             │
│        → execution graph, failure logic      │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│             LLM Integration Layer            │
│         → structured JSON inference          │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│              Domain Logic Layer              │
│   → discovery, scoring, themes, mitigation,  │
│                    summary                   │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│                   Core Layer                 │
│   → normalization, schema validation, IDs    │
└──────────────────────────────────────────────┘
```


---

# 3. Core Layer

The Core Layer provides deterministic utilities and guarantees relied on
by every domain.

### **Normalization**
All free-form text is passed through:
- Unicode normalization (NFKC)  
- whitespace collapsing  
- invisible character removal  
- lowercasing  

Ensures stable comparisons, hashing, and scoring.

### **Schema Validation**
Every domain input and output must satisfy the JSON schemas in `/schemas`.

### **ID Generation**
Risk and theme identifiers follow a stable prefix-based pattern:
`risk-xxxxxx`, `theme-xxxxxx`.

### **Model Selection**
Centralized logic chooses which LLM model to use based on:
- latency  
- cost  
- availability  
- configured preferences  

### **Execution Graph**
Defines the ordered sequence of pipeline stages and guards transitions
between them.

---

# 4. Domain Logic Layer

Each domain encapsulates its own logic, prompts, error handling, and
schema contracts. Domains never reference each other's internal
implementation.

---

## **4.1 Discovery Domain**

Extracts raw risk candidates via structured LLM prompting.

**Inputs:** project description  
**Outputs:** list of `RiskItem` objects  

### Responsibilities
- perform text segmentation  
- detect risk-like statements  
- normalize extracted items  
- assign stable risk IDs  

---

## **4.2 Scoring Domain**

Implements the hybrid scoring model:
- deterministic rule-based heuristics  
- LLM-assisted contextual scoring  
- weighted aggregation  

**Outputs:** list of `RiskScore` objects  

### Responsibilities
- compute rule-based likelihood & impact  
- request LLM-scored likelihood & impact  
- aggregate and normalize final score  
- enforce scoring schema  

---

## **4.3 Themes Domain**

Clusters risks into higher-order categories.

**Outputs:** list of `Theme` objects  

### Responsibilities
- analyze risk descriptions + severity  
- generate theme names and rationale  
- assign grouped `risk_ids`  
- normalize and validate theme objects  

---

## **4.4 Mitigation Domain**

Produces actionable mitigation steps for each risk.

**Outputs:** list of `Mitigation` objects  

### Responsibilities
- analyze risk + severity + theme context  
- request structured JSON mitigation suggestions  
- normalize actionable steps  
- enforce schema constraints  

---

## **4.5 Summary Domain**

Synthesizes the entire pipeline’s results into an executive-grade summary.

**Outputs:** `Summary` object  

### Responsibilities
- highlight top risks  
- summarize systemic patterns  
- consolidate mitigation strategy  
- produce leadership-level narrative  

---

# 5. LLM Integration Layer

This layer contains:

- structured prompts  
- deterministic JSON parsing  
- failure recovery (retry, fallback model, etc.)  
- validation-before-propagation guarantees  

LLMs **never** return free-form text into pipeline logic.

All calls follow:

```
prompt_template.format(...)
↓
strict JSON output required
↓
json.loads(...)
↓
validate against schema
↓
domain receives normalized object
```


---

# 6. Pipeline Orchestration Layer

The orchestrator governs the entire lifecycle of a risk analysis run.

### Responsibilities
- invoke domains in correct order  
- assemble unified pipeline payload  
- catch and classify domain-level failures  
- enforce schema contracts at boundaries  
- stop execution if validation fails  
- prepare final `RiskReport`  

The orchestrator is deterministic and stateless.

---

# 7. Reporting Layer

Produces the final schema-aligned output:

```
RiskReport:
  risks:        [...]  # extracted & normalized risk items
  scores:       [...]  # severity, likelihood, impact, aggregates
  themes:       [...]  # clustered thematic groups
  mitigations:  [...]  # actionable steps for each risk/theme
  summary:      {...}  # executive-level synthesis
  metadata:     {...}  # versioning, timestamps, model info
```


This artifact is suitable for:
- dashboards  
- periodic reporting  
- automated governance workflows  
- document generation  
- long-term archival  

---

# 8. Architectural Guarantees

### ✔ Schema compliance at every boundary  
### ✔ Fully deterministic non-LLM logic  
### ✔ Strict JSON responses from LLMs  
### ✔ Clear domain separation  
### ✔ Auditable transformation chain  
### ✔ Reproducible results regardless of model choice  

---

# 9. Future Extensions (Design-Ready)

The architecture supports:

- additional risk taxonomies  
- sector-specific scoring rules  
- expanded mitigation libraries  
- custom reporting templates  
- multi-model ensembles  
- fine-tuned domain-specific LLMs  

The modularity ensures no rewrites are required for system growth.

---

**PreMortem AI’s architecture combines engineering rigor with modern
language models to deliver accurate, consistent, and enterprise-ready
risk intelligence.**
