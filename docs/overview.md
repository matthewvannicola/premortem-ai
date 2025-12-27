# PreMortem AI — System Overview

PreMortem AI is an automated, domain-driven risk analysis engine that
transforms unstructured project descriptions into fully structured,
auditable, and actionable risk intelligence.  

The system integrates deterministic processing, schema enforcement, and
structured LLM inference to deliver consistent, explainable results that
support engineering teams, leadership stakeholders, and governance
frameworks.

---

## Why PreMortem AI Exists

Most projects begin with undocumented assumptions, ambiguous
requirements, and no standardized approach to identifying early-stage
risks. As a result:

- Silent risks emerge late  
- Teams waste effort debating severity instead of addressing root causes  
- Leadership lacks visibility into systemic concerns  
- Quality and delivery timelines degrade  

PreMortem AI addresses this gap by providing:

1. **Automated risk discovery**  
2. **Hybrid scoring (deterministic + LLM)**  
3. **Thematic clustering of systemic patterns**  
4. **Concrete mitigation recommendations**  
5. **Executive-ready summaries and structured reports**  

---

## High-Level Pipeline

PreMortem AI processes data through a sequence of structured, modular
domains:
```
Discovery → Scoring → Themes → Mitigation → Summary → Final Report
```


Each domain enforces:

- strict schema contracts  
- cleanly defined inputs/outputs  
- deterministic fallback logic  
- JSON-only LLM responses  
- audit-friendly transformations  

This architecture ensures the system behaves predictably, regardless of
model choice or input variability.

---

## Capabilities at a Glance

### **Discovery**
Extracts raw risk signals from natural-language project descriptions.

### **Scoring**
Combines deterministic heuristics with LLM reasoning to produce stable,
explainable likelihood, impact, and severity values.

### **Themes**
Clusters risks into meaningful problem categories, revealing systemic
patterns across a project or organization.

### **Mitigation**
Generates actionable, context-aware mitigation steps aligned with risk
severity and thematic insights.

### **Summary**
Produces an executive-level synthesis designed for engineering managers,
product leads, and delivery governance.

### **Final Report**
Structured, schema-compliant JSON output ready for downstream analytics,
dashboards, automation, or archival.

---

## Design Principles

### **1. Deterministic Foundations**
Core transformations—normalization, schema validation, ID generation,
aggregation—must always yield consistent results.

### **2. Structured LLM Interaction**
All model calls require:
- strict JSON schemas  
- domain-specific prompts  
- validation before advancing stages  

LLMs never produce free-form responses inside the pipeline.

### **3. Domain Isolation**
Each domain is self-contained, testable, and independently improvable.

### **4. Auditability & Trust**
Every output artifact is:
- schema compliant  
- reproducible  
- explainable  
- traceable across stages  

### **5. Modularity & Extensibility**
New models, additional domains, or custom risk frameworks can be added
without altering the core architecture.

---

## When to Use PreMortem AI

- Early-stage engineering planning  
- Risk discovery for product roadmaps  
- Technical due diligence  
- Architecture or implementation reviews  
- Delivery governance and oversight  
- AI-driven PMO workflows  
- Automated risk reporting systems  

---

## Output Formats

PreMortem AI produces multiple structured outputs:

- `risk_items`  
- `risk_scores`  
- `themes`  
- `mitigations`  
- `summary`  
- `risk_report` (final aggregated artifact)  

All outputs conform to versioned JSON schemas in `/schemas`.

---

## System Guarantees

PreMortem AI guarantees:

- Validated inputs/outputs at every step  
- No stage progress without schema compliance  
- Normalized text everywhere  
- Predictable scoring  
- Reproducible risk reports  
- Full traceability of reasoning  
- Enterprise alignment with AI governance best practices  

---

## Next Steps

For deeper insight into the system, see:

- [`architecture_overview.md`](architecture_overview.md)  
- [`data_flow_diagram.md`](data_flow_diagram.md)  
- [`risk_model_explained.md`](risk_model_explained.md)  
- [`api_reference.md`](api_reference.md)  

---

**PreMortem AI combines structured engineering rigor with modern LLM
capabilities to elevate how organizations identify and respond to risk.**
