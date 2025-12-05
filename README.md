# PreMortem AI  
Automated risk-analysis system using LLM inference, workflow orchestration, and structured data pipelines.

---

##  Overview  
PreMortem AI is a modular, event-driven automation system that transforms project descriptions into structured risk intelligence.  
The system integrates LLM processing, workflow orchestration, scoring logic, and automated reporting into one cohesive, enterprise-ready architecture.

This repository documents the system's architecture, schemas, example outputs, and prompt structures.

---

##  Key Features
- Deterministic risk generation using structured LLM prompts  
- Multi-pass inference for high-severity risk detection  
- End-to-end orchestration with retries, recovery, and logging  
- Automated PDF/Docs report assembly  
- Cross-team scoring standardization  
- Full audit trails and model-version lineage  

---

##  System Architecture  

PreMortem AI operates across five core layers:

---

### 1. **Intake & Trigger**
- Google Sheets stores project metadata and descriptions  
- Pipedream monitors updates and triggers the workflow pipeline  
- Input data is validated and normalized before LLM processing  

---

### 2. **LLM Inference**
- GPT-5.1 (fallback to GPT-4.1) processes structured prompts  
- Deterministic JSON schemas ensure consistent, machine-readable outputs  
- Multi-pass inference improves identification and scoring accuracy  

---

### 3. **Workflow Orchestration**
- Pipedream manages step-by-step logic, retries, and dynamic routing  
- Error-handling rules isolate failed tasks and perform intelligent recovery  
- Modular design allows updates without disrupting other components  

---

### 4. **Data Processing & Scoring**
- Outputs are parsed, categorized, and assigned severity  
- Cross-team scoring logic ensures alignment and repeatability  
- Data is prepared for reporting and knowledge-base storage  

---

### 5. **Reporting & Documentation**
- Automated PDF generation produces standardized executive-ready briefs  
- Reports and datasets are logged into Notion for versioning and visibility  
- Audit trails provide full traceability across the entire workflow
