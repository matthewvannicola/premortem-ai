# PreMortem AI — Prompt Library

This folder contains the full prompt suite used by **PreMortem AI**, a multi-stage automated risk analysis and reporting system.  
Each prompt represents one deterministic step in the inference pipeline, transforming raw project descriptions into a structured, executive-ready risk report.

All prompts follow these design principles:

- **Strict output schemas** (JSON-only where required)
- **Deterministic formatting** for automation pipelines
- **Separation of concerns** (each prompt performs one task only)
- **LLM-safe constraints** to prevent drift or hallucination
- **Executive-grade writing standards**

The pipeline is designed to run sequentially:

Discovery → Scoring → Themes → Mitigation → Summary → Final Report

---

# Prompt Index

Below is a complete description of each prompt, its purpose, input/output format, and role within the overall system.

---

## 1. `premortem_discovery.md`
**Purpose:**  
Identify and describe all plausible project risks based on a free-form project description.

**Input:**  
- `{{project_description}}`

**Output:**  
- A **JSON array** of raw risks (id, title, description, category, probability, impact, llm_score)

**Role:**  
This is the *first step* of the pipeline.  
It expands the project description into a structured list of potential risks.

---

## 2. `risk_scoring_prompt.md`
**Purpose:**  
Generate consistent, deterministic severity scoring across all discovered risks.

**Input:**  
- `{{risk_list}}` (from discovery step)

**Output:**  
- A **JSON array** with populated scoring fields:
  - `probability`  
  - `impact`  
  - `llm_score`  
  - `human_score` (null)  
  - `model_reasoning`  

**Role:**  
Transforms qualitative risks into **quantifiable data**.  
Used for ranking, prioritization, and report generation.

---

## 3. `risk_theme_prompt.md`
**Purpose:**  
Cluster risks into **non-overlapping thematic groups** (e.g., Technical Debt, Workflow Gaps, Product Risks).

**Input:**  
- `{{risk_list}}` (scored risks)

**Output:**  
- A **JSON array** of theme objects:
  - `theme`  
  - `description`  
  - `risks` (risk_id + reason)

**Role:**  
Provides higher-level structure and pattern recognition for executive reporting.  
Used by the Final Report prompt.

---

## 4. `mitigation_prompt.md`
**Purpose:**  
Generate targeted, practical mitigation strategies for each risk.

**Input:**  
- `{{scored_risk_list}}`

**Output:**  
- A **JSON array** identical to the input but with a populated `mitigation` field.

**Role:**  
Adds strategic recommendations to each risk, used in the Summary and Final Report.

---

## 5. `summary_prompt.md`
**Purpose:**  
Produce a polished **executive summary** of the overall risk posture, themes, and mitigation readiness.

**Input:**  
- `{{final_risk_list}}` (risks with scores, themes, and mitigations)

**Output:**  
- **Narrative prose only**  
- No JSON, no bullets, no markdown  

**Role:**  
This is used as the opening narrative of the Final Report.  
Summarizes risk posture for leadership.

---

## 6. `final_report_prompt.md`
**Purpose:**  
Assemble all outputs into a clean, structured, executive-ready risk report.

**Input:**  
- `{{report_inputs}}` (includes discovery results, scores, themes, mitigations, and summary)

**Output:**  
- A fully formatted **Markdown report**, following a mandatory structure:
  1. Executive Summary  
  2. Risk Landscape Overview  
  3. Thematic Risk Groups  
  4. Detailed Risk Breakdown  
  5. Recommended Focus Areas  

**Role:**  
Final deliverable.  
Suitable for leadership, clients, internal communication, and compliance documentation.

---

# Prompt Pipeline Overview

```mermaid
graph TD
    A[Project Description] --> B[Discovery Prompt]
    B --> C[Scoring Prompt]
    C --> D[Theme Prompt]
    C --> E[Mitigation Prompt]
    D --> F[Final Report]
    E --> F[Final Report]
    C --> G[Summary Prompt]
    G --> F[Final Report]
