# Pipedream Workflows — PreMortem AI Pipeline

This directory contains all workflow components, logic blocks, and orchestration assets required to run the PreMortem AI pipeline inside **Pipedream**.  
Each component is isolated, versioned, and built to support deterministic execution, structured JSON handling, and seamless integration with LLM inference steps.

The Pipedream layer acts as the **operational backbone** of the pipeline—managing triggers, execution order, retries, validation, and report generation.

---

## 1. Architecture Overview

The Pipedream implementation is organized around two core elements:

### **A. Component Modules (`/components`)**
Each pipeline stage (Discovery, Scoring, Themes, Mitigation, Summary, Final Report) is implemented as a standalone, reusable Pipedream component.

Every component folder contains:
- `component.yaml` — metadata, props, inputs/outputs, versioning
- `index.js` — execution logic for that pipeline stage

### **B. Workflow Definitions (`/workflows`)**
Full workflow YAML files define the actual execution graph and orchestrate how components interact.

This separation mirrors enterprise architecture standards:
- **Components** = atomic, testable units  
- **Workflows** = orchestrated business logic  

---

## 2. Component Directory Structure

```
components/
discovery/
component.yaml
index.js
final_report/
component.yaml
index.js
mitigation/
component.yaml
index.js
scoring/
component.yaml
index.js
summary/
component.yaml
index.js
themes/
component.yaml
index.js
```


### Component Responsibilities

| Component        | Purpose |
|------------------|---------|
| **discovery**    | Extracts raw risks from project description using structured LLM calls. |
| **scoring**      | Applies probability, impact, and severity scoring rules. |
| **themes**       | Clusters risks into higher-order patterns. |
| **mitigation**   | Generates targeted mitigation actions for each risk/theme. |
| **summary**      | Produces executive-level summaries, health scores, and thematic insights. |
| **final_report** | Builds and exports the Google Doc / PDF report. |

Each component enforces:
- Schema validation  
- Deterministic JSON formatting  
- Retry logic and error handling  
- Model configuration (GPT-4.1 / GPT-5.1)  

---

## 3. Workflow Definitions (`/workflows`)

All workflow YAML files live in the `workflows/` directory.

These orchestrate:
- Input ingestion  
- Execution order  
- Error routing  
- Retry policies  
- Final report generation  
- Persistence and logging  

Typical workflows:

- **main_workflow.yml**  
  End-to-end pipeline execution.

- **retry_workflow.yml**  
  Handles fallback logic when a component fails schema validation.

- **report_workflow.yml**  
  Generates Google Docs / PDF outputs.

---

## 4. Deployment Instructions

### **Step 1 — Import Components**
1. Go to **Pipedream → Components**
2. Click **Import Component**
3. Import each folder under `/components`
4. Publish each component version

### **Step 2 — Import Workflows**
1. Go to **Workflows**
2. Import each YAML file from `/workflows`
3. Connect required integrations:
   - OpenAI API
   - Google Docs API
   - Google Drive
   - Notion (optional)
   - Sheets (optional)

### **Step 3 — Set Environment Variables**
In each workflow:
- `OPENAI_API_KEY`
- `MODEL_PRIMARY` (e.g., `gpt-5.1`)
- `MODEL_FALLBACK`
- `REPORT_FOLDER_ID`
- `STRICT_VALIDATION`
- `MAX_RETRIES`

---

## 5. Execution Flow (High-Level)
```
Discovery → Scoring → Themes → Mitigation → Summary → Final Report
```


Pipedream workflows manage:
- Ordered execution  
- Schema validation after every step  
- Failure isolation and retry  
- Fallback model logic  
- Artifact routing into Google Docs  

---

## 6. Error Handling & Retry Logic

Pipedream workflows implement three layers of protection:

### **1. Component-Level Validation**
Each component validates its JSON output against strict schemas.

### **2. Step-Level Retry**
If validation fails:
- Component is re-executed
- Hints are added to the LLM prompt

### **3. Workflow-Level Fallback**
If failure persists:
- A fallback workflow handles regeneration
- Output is flagged for review
- The run is still completed gracefully

---

## 7. Maintaining and Extending Components

You can safely extend or modify pipeline functionality by updating:
- Component logic in `index.js`
- Component metadata in `component.yaml`
- Workflow order or branching in `/workflows`
- Schemas (outside this folder)

This modular design ensures:
- Low coupling  
- High maintainability  
- Easy experimentation  
- Enterprise-grade governance  

---

## 8. Best Practices

- Keep all component outputs strictly JSON-validated  
- Use model temperature = 0 for deterministic behavior  
- Increment version numbers in `component.yaml` when publishing changes  
- Log errors inside each component for auditing  
- Maintain human-readable prompts inside `/docs` or `/prompts`  

---

## 9. Related Documentation

Main architecture README:  
*(Generated last, after repository is complete)*

Deep-dive component docs:  
`/docs/components/`

Pipeline schemas:  
`/schemas/`

Prompts (LLM instructions):  
`/prompts/`

---

## Maintainer
This workflow infrastructure is maintained by **Matthew Vannicola**.
