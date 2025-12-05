# PreMortem AI 

Automated risk-analysis system using LLM inference, workflow orchestration, and structured data pipelines.

---

## Overview

PreMortem AI is a modular, event-driven automation system that transforms unstructured project descriptions into **structured risk intelligence**.

The platform integrates LLM processing, workflow orchestration, scoring logic, and automated reporting into a **single, enterprise-ready architecture** designed for reliability, transparency, and repeatability.

This repository documents the system’s architecture, schemas, example outputs, and prompt structures.

---

## System Architecture

PreMortem AI operates across five core layers:

---

### **1. Intake & Trigger**

- Google Sheets stores project descriptions and metadata  
- Pipedream monitors updates and triggers the workflow pipeline  
- Input data is validated and normalized before LLM processing  

---

### **2. LLM Inference**

- GPT-5.1 (fallback to GPT-4.1) processes structured prompts  
- Deterministic JSON schemas ensure consistent, machine-readable outputs  
- Multi-pass inference improves identification and scoring accuracy  

---

### **3. Workflow Orchestration**

- Pipedream manages step-by-step logic, retries, and dynamic routing  
- Error-handling rules isolate failed tasks and perform intelligent recovery  
- Modular design enables updates without disrupting other components  

---

### **4. Data Processing & Scoring**

- Outputs are parsed, categorized, and assigned severity scores  
- Cross-team scoring logic ensures alignment and repeatability  
- Data is prepared for reporting and knowledge-base storage  

---

### **5. Reporting & Documentation**

- Automated PDF generation produces standardized, executive-ready briefs  
- Reports and datasets are logged into Notion for versioning and visibility  
- Audit trails provide full traceability across the entire workflow  

---

## Features & Capabilities

- Multi-domain risk identification (technical, operational, product, organizational)  
- Structured LLM inference pipelines  
- Deterministic scoring and probability modeling  
- Automated reporting in PDF / Google Docs formats  
- End-to-end traceability with audit logging  
- Cross-platform orchestration (Google Sheets → Pipedream → LLMs → Docs/Notion)  
- Fully machine-readable outputs suitable for downstream automation  

---

## Example Outputs
```json
{
  "risk_id": "R-014",
  "category": "Technical",
  "description": "Unclear API ownership may delay integration milestones.",
  "probability": "Medium",
  "impact": "High",
  "severity": 4,
  "recommendation": "Assign API ownership and establish cross-team integration checkpoints."
}
```
---

## Tech Stack

### **AI & LLMs**

- GPT-5.1 (primary inference model)
- GPT-4.1 (fallback model)
- GPT-4o (lightweight checks & summarization)
- Deterministic JSON schemas for structured outputs
- Multi-pass inference & scoring logic
- Prompt engineering and tool-use patterns

---

### **Automation Platforms**

- Pipedream (event-driven orchestration)
- Make.com (supplementary workflow automation)
- Zapier (lightweight integrations & triggers)
- Scheduled and conditional workflows
- Error handling, retries, and controlled fallbacks

---

### **APIs & Integrations**

- REST APIs (request/response flows)
- Webhooks (event triggers & callback flows)
- OAuth2 / token-based authentication
- Third-party SaaS integrations
- Cross-platform data passing (Sheets → LLM → Docs → Notion)

---

### **Data & Reporting**

- Google Sheets as structured intake layer
- Data normalization & validation pipelines
- Severity scoring & probability modeling
- Automated PDF and Google Docs generation
- Notion for reporting, audit l

---

## Repository Structure

- `schemas/`
  - `risk_output.schema.json` – JSON schema for individual risk records
  - `scoring.schema.json` – schema for probability, impact, and severity scoring
  - `metadata.schema.json` – schema for run metadata, project info, and audit fields

- `pipedream/`
  - `premortem_main.yml` – primary orchestration workflow (intake → LLM → scoring → reporting)
  - `premortem_retry.yml` – fallback / retry workflow for failed or partial runs
  - `premortem_pdf.yml` – workflow for generating Google Docs / PDF reports
  - `helpers/`
    - `validate-json.js` – helper for schema validation inside Pipedream steps

- `prompts/`
  - `discovery_prompt.md` – prompt for initial risk discovery and expansion
  - `scoring_prompt.md` – prompt for probability, impact, and severity scoring
  - `summary_prompt.md` – prompt for executive summaries and thematic clustering

- `examples/`
  - `sample_input.json` – example project brief used as intake
  - `sample_output.json` – example structured risk output
  - `sample_report.pdf` – example of the generated executive report

- `docs/`
  - `architecture_overview.md` – high-level system and data-flow explanation
  - `data_flow_diagram.png` – visual representation of the pipeline
  - `risk_model_explained.md` – details on the severity model and scoring logic

- `src/`
  - `utils/`
    - `normalize_text.py` – text cleaning and normalization helpers
    - `validate_schema.py` – local JSON schema validation utilities
  - `scoring/`
    - `severity_engine.py` – core severity and weighting logic

- `README.md` – project overview, architecture, and usage
- `requirements.txt` – Python dependencies for local tools and validation

---

## Configuration

This section defines how PreMortem AI manages environment variables, schema validation, model selection, and pipeline rules.  
All configuration is deterministic, modular, and optimized for enterprise reliability.

---

### **1. Environment Variables**

These variables control inference behavior, output routing, and schema validation.

```env
# OpenAI / Model Controls
OPENAI_API_KEY=your_api_key
MODEL_PRIMARY=gpt-5.1
MODEL_FALLBACK=gpt-4.1
MODEL_SUMMARY=gpt-4o

# Schema Paths
SCHEMA_RISK=./schemas/risk_output.schema.json
SCHEMA_SCORING=./schemas/scoring.schema.json
SCHEMA_METADATA=./schemas/metadata.schema.json

# Output Controls
DOCS_OUTPUT_FOLDER_ID=your_google_docs_folder
NOTION_API_KEY=your_notion_key
NOTION_DATABASE_ID=your_notion_db

# Execution
MAX_RETRIES=3
STRICT_VALIDATION=true
```

---

### **2. JSON Schema Validation**

Every LLM output is checked against strict JSON schemas before it enters the rest of the pipeline.  
This ensures the system always produces clean, structured, machine-readable data.

**How validation works:**

1. The LLM generates a JSON object  
2. The output is checked against the schema (risk, scoring, metadata)  
3. If the structure is invalid, missing fields, or contains unexpected values:  
   - A retry is triggered  
   - A fallback model (GPT-4.1) regenerates the output  
4. All validation results are logged to the audit trail for transparency

This guarantees deterministic outputs and prevents malformed responses from breaking the workflow.

---

### **3. Multi-Pass Inference Configuration**

PreMortem AI uses a multi-pass inference pipeline to improve accuracy, enforce structure, and reduce hallucinations.  
Each stage focuses on a different part of the analysis, allowing the system to produce highly reliable outputs.

---

#### **Pass 1 — Discovery Layer**

- GPT-5.1 identifies raw risks based on the project description  
- Focuses on breadth, context, and uncovering hidden dependencies  
- Produces a structured but unscored list of risks  

---

#### **Pass 2 — Scoring Layer**

- GPT-4.1 evaluates probability, impact, and severity  
- Uses deterministic scoring rules defined in the scoring schema  
- Ensures consistent and repeatable results across runs  

---

#### **Pass 3 — Summary Layer**

- GPT-4o generates leadership-ready summaries and top-risk highlights  
- Clusters risks into themes (technical, organizational, product, etc.)  
- Creates a clean, executive-friendly overview of the findings  

Each pass is validated independently and logged in the audit trail to ensure full transparency.

---

### **4. Pipeline Execution Rules**

These rules define how the system behaves during inference, validation, error recovery, and reporting.  
They ensure reliability, stability, and deterministic outcomes across executions.

---

#### **Rule 1 — Conditional Model Fallback**

Fallback is triggered when:
- JSON output is malformed  
- Required fields are missing  
- Schema validation fails  
- The LLM response is incomplete or truncated  

Fallback behavior:
- Switch to GPT-4.1  
- Use strict deterministic settings (`temperature = 0`)  
- Retry up to `MAX_RETRIES`  

This prevents single-pass failures from stopping the workflow.

---

#### **Rule 2 — Controlled Retries**

If an LLM output fails validation:
1. Attempt regeneration with correction hints  
2. Retry with fallback model  
3. Regenerate only missing or invalid fields  
4. If still invalid → log an error and insert a placeholder risk  

This ensures the pipeline always completes gracefully.

---

#### **Rule 3 — Output Normalization**

Before scoring or reporting:
- Normalize enums (“High”, not “high”)  
- Trim whitespace and fix formatting  
- Merge duplicate risks  
- Clamp severity values to the allowed range (1–5)  
- Standardize keys and value types  

Normalization enforces consistency across all outputs.

---

#### **Rule 4 — Reporting Conditions**

The reporting workflow (PDF/Docs generation) only runs when:
- All risk objects pass validation  
- Metadata is complete  
- Scoring is finalized  

If any condition fails:
- Workflow transfers to `premortem_retry.yml`  
- Notion logs the error record  
- Google Sheets is updated with a failure status  

This ensures only clean, validated runs produce final reports.

---

### **5. Audit Trail Configuration**

PreMortem AI maintains a full audit trail for every execution.  
This enables transparency, debugging, compliance, and reproducibility.

Each run logs the following data:

- **Raw project input** (as provided in Google Sheets)  
- **All LLM messages** used across each inference pass  
- **Validation results** for risk, scoring, and metadata schemas  
- **Retry attempts** and fallback model usage  
- **Normalized final JSON output**  
- **Links to generated PDF/Docs reports**  
- **Execution timestamp and run ID**  

The audit log is stored in Notion and optionally mirrored to Google Sheets for operational visibility.

This ensures every run is fully traceable from input to final report.

---

### **6. Customization**

PreMortem AI is designed to be fully configurable so teams can adapt the system to their workflow, modeling needs, and reporting formats.

Key customization points include:

- **Model Selection**  
  Swap primary or fallback LLMs, adjust temperatures, or change which model handles each inference pass.

- **Scoring Logic**  
  Modify probability/impact enums, severity weighting, or thresholds to match organizational risk models.

- **Pipeline Flags**  
  Control validation strictness, retry limits, fallback behavior, and output normalization rules.

- **Report Templates**  
  Replace or update the Google Docs template to match internal branding, formats, or executive reporting standards.

- **Metadata Extensions**  
  Add fields for department, budget, project owner, review status, RACI roles, or any additional enterprise metadata.

All configuration is modular, enabling easy extension without rewriting core pipeline logic.

---

## Impact & Use Cases
PreMortem AI delivers measurable value across product, engineering, and operations teams by transforming unstructured project descriptions into actionable, structured risk intelligence.

---

### **1. Faster, Higher-Quality Risk Discovery**

Traditional pre-mortem sessions require multi-hour meetings and still miss critical risks.  
PreMortem AI identifies 50–200 risks in seconds, dramatically increasing coverage and reducing blind spots.

**Value:**

- Accelerates planning cycles  
- Improves forecast accuracy  
- Reduces late-stage project failures  

---

### **2. Standardized Scoring & Decision Making**

Different teams score risks differently, leading to inconsistent prioritization.  
PreMortem AI enforces deterministic probability, impact, and severity scoring for every project.

**Value:**

- Creates a shared language around risk  
- Enables cross-team comparability  
- Supports leadership decision-making  

---

### **3. Automated Executive Reporting**

Instead of manually compiling notes, summaries, and risk tables, the system generates polished PDF or Google Docs reports with one click.

**Value:**

- Saves hours of manual report-building  
- Ensures consistent formatting and quality  
- Supports recurring project reviews at scale  

---

### **4. Auditability & Compliance**

All inputs, LLM messages, scoring logic, retries, and outputs are fully logged.

**Value:**

- Enables transparent, defensible decision-making  
- Supports compliance and governance standards  
- Provides complete traceability for audits  

---

### **5. Enterprise Workflow Integration**

PreMortem AI plugs into tools teams already use — Google Sheets, Pipedream, Notion, and internal APIs.

**Value:**

- Zero learning curve  
- Compatible with any project workflow  
- Easily extended to Jira, Asana, ServiceNow, or internal systems  

---

### **6. Ideal For**

- Product Managers  
- Engineering Leads  
- Program / Project Managers  
- Risk & Compliance Teams  
- AI-driven PMOs  
- Early-stage startups and enterprise organizations  

---

PreMortem AI bridges the gap between **project planning** and **risk management**, delivering structured intelligence that teams can trust.

---

## Architecture Overview & Diagram (Text Version)

The PreMortem AI pipeline is designed as a modular, event-driven architecture.  
Each component is isolated, deterministic, and optimized for transparency and reliability.

Below is a text-based representation of the system diagram.

---

### 1. Intake Layer

**Google Sheets → Pipedream Trigger**

- Project descriptions and metadata are entered into Google Sheets.
- A Pipedream trigger watches for changes and starts the workflow.
- Basic validation and normalization are applied to the input.

```
Google Sheets
    ↓
Pipedream Trigger
    ↓
Input Validation
```

---

### 2. LLM Processing Layer

**Multi-pass inference using GPT-5.1, GPT-4.1, and GPT-4o**

- Pass 1 — Discovery (GPT-5.1): identifies raw risk candidates.
- Pass 2 — Scoring (GPT-4.1): assigns probability, impact, and severity.
- Pass 3 — Summary (GPT-4o): produces executive summaries and thematic clusters.

```
Discovery (GPT-5.1)
    ↓
Scoring (GPT-4.1)
    ↓
Summary (GPT-4o)
```

---

### 3. Orchestration Layer

**Pipedream Workflow**

- Controls pipeline execution order.
- Applies JSON schema validation after each LLM pass.
- Handles retries and fallback model behavior.
- Normalizes outputs before scoring and reporting.

```
LLM Output
    ↓
Schema Validation
    ↓
Retry / Fallback Logic
    ↓
Normalization
```

---

### 4. Data Processing Layer

- Cleans and standardizes JSON fields.
- Merges duplicates and enforces enum/value constraints.
- Produces a final validated dataset ready for reporting.

```
Raw JSON
    ↓
Validation & Normalization
    ↓
Final Clean Dataset
```

---

### 5. Reporting Layer

**Google Docs → PDF**

- Fills a Google Docs template with risk tables and summaries.
- Exports a final PDF suitable for stakeholders.
- Saves the formatted report to an output folder.

```
Validated Dataset
    ↓
Google Docs Template
    ↓
PDF Export
```

---

### 6. Audit Logging Layer

**Notion + Google Sheets (optional)**

- Logs raw inputs, LLM messages, schema validation status, and retries.
- Captures run metadata such as timestamps, run IDs, and model usage.
- Stores links to generated documents and final outputs.

```
Execution Data
    ↓
Notion Audit Log
```

---

### 7. End-to-End Flow Summary

```
Google Sheets
    ↓
Pipedream Trigger
    ↓
Multi-pass LLM (GPT-5.1 → GPT-4.1 → GPT-4o)
    ↓
Validation & Normalization
    ↓
Final Dataset
    ↓
Google Docs → PDF
    ↓
Notion Audit Trail
```

---

## Roadmap

The following roadmap outlines planned enhancements and long-term improvements for PreMortem AI. These initiatives focus on scalability, automation depth, enterprise compatibility, and richer analytics.

---

### **1. Enhanced Integrations**

- Jira, Asana, and ClickUp API connectors for automated project ingestion  
- Slack and Teams notifications for report delivery  
- ServiceNow integration for risk escalation workflows  

---

### **2. Multi-Project Batch Processing**

- Support for batch ingestion of 10–100 projects at once  
- Parallel processing with shared context models  
- Consolidated executive reports for program-level risk visibility  

---

### **3. Advanced Analytics & Dashboards**

- Risk trend analytics over time  
- Aggregated severity scoring across teams  
- Visualization dashboards powered by Looker / Data Studio / Supabase  
- Heatmaps for probability × impact patterns  

---

### **4. Custom Severity Models**

- Organization-specific scoring weights  
- Multi-factor scoring (technical complexity, dependency load, budget risk)  
- Dynamic severity adjustment based on historical outcomes  

---

### **5. Expanded Reporting Capabilities**

- Multi-section PDF reports with appendices  
- Optional CSV exports for BI pipelines  
- Richer Google Docs templates with branded components  
- Stakeholder-specific report variants (PMs, engineering leads, executives)  

---

### **6. Enterprise Workflow Extensions**

- SOC2-friendly audit pipeline with stricter logging  
- Role-based access controls for report visibility  
- Internal API endpoints for triggering runs programmatically  
- Scheduled weekly or monthly automated summary reports  

---

### **7. Multi-Language Support**

- English + Spanish + German report outputs  
- Localization for risk categories and scoring definitions  
- Model-based translation consistency checks  

---

### **8. On-Prem / VPC Deployment Option**

- Self-hosted inference endpoint for regulated environments  
- Private network execution with secrets isolation  
- Enterprise security posture alignment  

---

### **9. Model Optimization & Alternative LLMs**

- Fine-tuned mini-model for scoring layer  
- Mixed-model inference routing based on complexity  
- Optional Anthropic or Azure OpenAI compatibility modes  

---

### **10. Collaboration & Feedback Loop**

- Reviewer comments directly inside the report  
- Feedback ingestion to refine future scoring  
- Team-based consensus scoring panels  
- Continuous learning mechanisms for risk weighting  

---

PreMortem AI is designed for long-term evolution, supporting increasingly complex workflows, larger datasets, and deeper enterprise integrations as the system matures.

---

## Installation & Setup

PreMortem AI runs primarily inside Pipedream with supporting configuration stored in this repository.  
Follow the steps below to install, configure, and run the system end-to-end.

---

### 1. Clone the Repository

Clone the project to access schemas, prompts, helper scripts, and workflow files.

    git clone https://github.com/<your-username>/premortem-ai.git
    cd premortem-ai

---

### 2. Set Up Environment Variables

Create a `.env` file or set environment variables inside Pipedream.

Required values:

    OPENAI_API_KEY=your_api_key
    MODEL_PRIMARY=gpt-5.1
    MODEL_FALLBACK=gpt-4.1
    MODEL_SUMMARY=gpt-4o

    SCHEMA_RISK=./schemas/risk_output.schema.json
    SCHEMA_SCORING=./schemas/scoring.schema.json
    SCHEMA_METADATA=./schemas/metadata.schema.json

    DOCS_OUTPUT_FOLDER_ID=your_google_docs_folder
    NOTION_API_KEY=your_notion_key
    NOTION_DATABASE_ID=your_notion_db

    MAX_RETRIES=3
    STRICT_VALIDATION=true

---

### 3. Import the Pipedream Workflows

In the `/pipedream` directory you will find:

- premortem_main.yml  
- premortem_retry.yml  
- premortem_pdf.yml  

Import each one:

1. Go to Pipedream → Workflows  
2. Click **Import Workflow**  
3. Upload the corresponding `.yml` file  
4. Connect Google, OpenAI, and Notion accounts when prompted  

---

### 4. Connect Google Sheets (Intake Layer)

1. Duplicate your template sheet (provided in `/integrations/google-sheets/` or create your own).  
2. Add project descriptions in the first column.  
3. Pipedream will ingest new or updated rows automatically.  

Your sheet acts as the **trigger/input source**.

---

### 5. Connect Google Docs (Reporting Layer)

Inside Pipedream:

1. Add the Google Docs integration  
2. Set the folder ID where reports should be created  
3. Ensure your account has editor access to the folder  

The reporting workflow will fill in a template and export PDFs.

---

### 6. Optional: Install Local Tools

If you want to locally validate schemas or test helper scripts:

    pip install -r requirements.txt

Local tools let you test normalization and schema validation offline.

---

### 7. Run the System

There are two ways to run PreMortem AI:

**Option A — Google Sheets Trigger**  
Update or add a row; the workflow fires automatically.

**Option B — Manual Run**  
Inside Pipedream → open the workflow → click **Run Now**.

During execution, the system will:

1. Ingest your project  
2. Run multi-pass inference  
3. Validate all outputs  
4. Apply scoring and normalization  
5. Generate a Google Doc  
6. Export a PDF  
7. Log metadata in Notion  

---

### 8. Confirm Output

When the workflow completes, you will see:

- A completed Google Doc  
- A PDF export  
- A normalized JSON output (in logs)  
- A Notion entry containing:  
  - run_id  
  - timestamps  
  - retry counts  
  - links to generated reports  
  - cleaned final dataset

---

## Schemas

PreMortem AI uses strict JSON schemas to enforce structure, consistency, and deterministic outputs across all LLM stages.  
These schemas ensure that every inference pass produces machine-readable data suitable for scoring, reporting, and audit logging.

The system defines three core schemas:

---

### **1. Risk Output Schema**

Path: `/schemas/risk_output.schema.json`

Defines the structure of a single risk object, including:

- risk_id  
- category  
- description  
- probability  
- impact  
- severity  
- recommendation  

This schema ensures every risk follows the same format and value constraints.

---

### **2. Scoring Schema**

Path: `/schemas/scoring.schema.json`

Defines the allowed values and constraints for:

- probability (Low, Medium, High)  
- impact (Low, Medium, High)  
- severity (1–5 numeric range)  

This schema guarantees consistent scoring across all runs.

---

### **3. Metadata Schema**

Path: `/schemas/metadata.schema.json`

Defines the structure of execution-level metadata, such as:

- run_id  
- timestamp  
- model_used  
- pipeline_version  
- source sheet / row index  

This schema ensures complete traceability for every workflow run.

---

### Schema Governance

All schemas must pass validation before data moves to the next stage of the pipeline.  
If validation fails:

1. The system retries  
2. Attempts correction  
3. Falls back to an alternative model if necessary  
4. Logs the failure into the audit trail  

This prevents malformed outputs and guarantees deterministic behavior end-to-end.

---

## Example Prompts

PreMortem AI uses structured, deterministic prompts across three inference passes.  
Each prompt is designed to enforce schema compliance, reduce ambiguity, and improve output reliability.

---

### **1. Discovery Prompt (GPT-5.1)**

*Identifies raw risk candidates from the project description.*

Purpose: Generate a broad, structured list of potential risks before scoring.

Prompt:

    You are an AI risk analysis engine. Analyze the project description below and
    identify all potential risks across technical, operational, organizational,
    product, compliance, and dependency domains.

    Your goal is to produce a *diverse and comprehensive* set of risks before scoring.
    Do not assign probability, impact, or severity values yet.

    Output must be strictly formatted as a JSON array of objects, each containing:
      - "risk_id": string (leave blank, pipeline will populate)
      - "category": string
      - "description": string

    Project Description:
    {{project_description}}

    Return ONLY valid JSON. No explanation, no commentary.

---

### **2. Scoring Prompt (GPT-4.1)**

*Applies probability, impact, and severity values using deterministic rules.*

Purpose: Enforce consistent, rule-based scoring.

Prompt:

    You are an AI scoring engine. Using the deterministic scoring rules below,
    evaluate each risk provided in the input list.

    Allowed values:
      - probability: Low, Medium, High
      - impact: Low, Medium, High
      - severity: integer from 1 to 5

    Severity Definition:
      1 = Minimal effect
      2 = Low impact on deliverables
      3 = Moderate risk requiring monitoring
      4 = High risk likely to affect timelines
      5 = Critical risk requiring immediate mitigation

    For each risk, output a JSON object containing:
      - "risk_id": string (pipeline populates)
      - "category": string
      - "description": string
      - "probability": string
      - "impact": string
      - "severity": integer
      - "recommendation": string

    Risks to score:
    {{risk_list}}

    Return ONLY valid JSON. No explanations.

---

### **3. Summary Prompt (GPT-4o)**

*Generates an executive-ready narrative summarizing major risks.*

Purpose: Produce leadership-focused takeaways.

Prompt:

    You are an executive summarization engine. Based on the list of scored risks
    provided below, generate:

      - A concise executive summary (3–5 sentences)
      - The top 5 highest-severity risks with 1-sentence explanations
      - Thematic clusters (technical, organizational, product, etc.)
      - High-level mitigation considerations

    Keep the tone concise, neutral, and business-oriented.

    Scored Risks:
    {{scored_risks}}

    Output must be a JSON object with the following fields:
      - "executive_summary": string
      - "top_risks": array of strings
      - "themes": array of strings
      - "mitigation_notes": array of strings

    Do NOT include disclaimers or commentary. Return only JSON.

---

## Contact / About the Author

PreMortem AI was built by **Matthew Vannicola**, an AI Automation Engineer specializing in:

- LLM orchestration and multi-stage pipelines  
- Deterministic prompt engineering  
- Workflow automation (Pipedream, Make, Zapier)  
- Structured data systems and schema-driven validation  
- Enterprise reporting and operational AI tooling  

If you’d like to connect, collaborate, or discuss automation systems:

- **GitHub:** https://github.com/matthewvannicola 
- **LinkedIn:** https://www.linkedin.com/in/matthew-vannicola  
- **Portfolio:** https://sites.google.com/view/matthew-vannicola-ai/  
- **Email:** <matthew.vannicolajr@gmail.com>  

Feel free to reach out for project collaborations, architecture questions, workflow design, or AI-powered automation opportunities.
