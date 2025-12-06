# Glossary

This glossary defines the core terminology used throughout the PreMortem AI system.  
All terms are aligned with the canonical definitions in the domain model, JSON Schemas, and pipeline architecture.

---

## A

### **Aggregate Root**
The top-level entity that encapsulates all pipeline outputs for a single analysis.  
In PreMortem AI, the `RiskReport` is the aggregate root.

---

## C

### **Canonical Form**
A normalized, schema-compliant representation of an entity.  
Canonicalization ensures deterministic shapes, stable field ordering, and unambiguous interpretation across environments.

### **Category (Risk Category)**
A taxonomy label describing the type of a risk, such as `organizational`, `technical`, or `operational`.

---

## D

### **Determinism**
A system guarantee that identical inputs produce identical outputs, including ID assignment, ordering, scoring, and narrative structures.

### **Discovery (Risk Discovery)**
The pipeline stage that extracts structured `Risk` entities from unstructured input text.

---

## E

### **Entity**
A named, typed object in the domain model (Risk, Score, Theme, Mitigation, Summary).

### **Executive Summary**
A high-level narrative describing risk posture, top risks, and health score.

---

## F

### **Failure Mode**
A specific way a project can fail, represented as a `Risk` entity.

---

## H

### **Health Score**
A numeric indicator (0–100) summarizing overall project risk.  
Computed deterministically from risk scores, mitigations, and thematic patterns.

---

## I

### **Identifier (ID)**
A deterministic, zero-padded, schema-controlled identifier such as `risk-00001` or `theme-00003`.

### **Input Normalization**
The preprocessing step that cleans, normalizes, and stabilizes raw text before LLM inference.

---

## L

### **Likelihood**
A scoring dimension representing the probability of a risk occurring (1–5).

### **LLM Malformed Output**
A model response that violates JSON shape, structure, or schema rules.

---

## M

### **Mitigation**
A set of actionable steps intended to reduce a risk’s likelihood or impact.

### **Mitigation Generator**
The pipeline component that produces structured mitigation guidance.

---

## N

### **Narrative**
Short, concise, human-readable text explaining risk posture or thematic patterns.

---

## O

### **Ordering Guarantee**
A determinism requirement ensuring arrays (risks, themes, mitigations, etc.) maintain consistent ordering across runs.

---

## P

### **Pipeline Execution**
The end-to-end flow of all analysis components, typically invoked via `/analysis`.

### **Project Description**
The raw, unstructured input text describing a project, problem, or initiative.

---

## R

### **Risk**
A structured entity representing a potential failure mode, including title, description, category, and source text.

### **Risk Discovery Engine**
The component responsible for extracting risks from text.

### **RiskReport**
The aggregate output containing risks, scores, themes, mitigations, summary, and metadata.

---

## S

### **Schema Validation**
The enforcement mechanism ensuring all outputs conform to predefined JSON Schemas.

### **Score (Risk Score)**
A structured entity containing likelihood, impact, severity, and rationale.

### **Scoring Engine**
The component that assigns numerical scores to risks.

### **Severity**
The product of likelihood and impact (1–25), computed deterministically.

### **Summary Synthesizer**
The component that generates the executive narrative and health score.

---

## T

### **Theme**
A systemic pattern derived from one or more risks.

### **Theme Generator**
The pipeline component that clusters risks into themes.

### **Traceability**
The property that each entity (risk, score, theme, mitigation) references its lineage via stable IDs.

---

## V

### **Validation Error**
Any schema violation or malformed model output that prevents downstream processing.

### **Versioned Namespace**
The API path prefix (e.g., `/api/v1`) representing the active contract version.

---

# End of Glossary
