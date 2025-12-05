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

## Example Outputs *(Optional — add later)*
*(Add JSON examples, report snippets, or scoring tables here.)*

---

## Prompt & Schema Definitions *(Optional — add later)*
*(Insert deterministic JSON schemas and prompt templates here.)*

---

## Full Technical Stack

### **AI & LLMs**
- GPT-5.1 (enterprise LLM integrations)  
- GPT-4.1  
- GPT-4o  
- LLM decision-logic design  
- Function calling / tool use  
- Retrieval-augmented workflows (RAG-style patterns)  
- Structured output generation  
- JSON schema design  
- Prompt engineering  

### **Automation Platforms**
- Pipedream  
- Make.com  
- Zapier  
- Event-driven automation  
- Scheduled & cron-based workflows  
- Webhook integrations  
- Multi-step workflow orchestration  
- Cross-platform pipeline coordination  

### **APIs & Integrations**
- REST API design & integration  
- Webhooks (event-driven callbacks)  
- JSON / structured data transformation  
- OAuth 2.0 & token-based authentication  
- Third-party SaaS integrations  
- API error-handling & retry logic  
- Secure credential management  

### **Data & Reporting**
- Automated Google Sheets pipelines (ETL-style transformations)  
- Data normalization, schema validation & error handling  
- Structured report outputs (JSON → PDFs / Google Docs)  
- Scheduled reporting workflows with audit-friendly logs  
- Multi-source data aggregation for automated insights  

### **Systems & Architecture**
- End-to-end automation architecture (cross-platform, multi-service systems)  
- Pipeline orchestration with dependency management, failover logic & idempotent execution  
- System mapping & integration strategy (data contracts, API governance, event models)  
- Scalability engineering for high-volume workflows (rate limits, concurrency, backoff logic)  
- Architecture documentation & implementation roadmaps  
- Operational reliability for automations (monitoring, alerting, version-controlled releases)  

---

## License
This repository is provided for demonstration and educational purposes.

---

## Contact
For engineering discussions or collaboration opportunities:

**Matthew Vannicola**  
AI Automation Engineer — LLM Systems & Workflow Orchestration  
📧 matthew.vannicolajr@gmail.com  
🌐 Portfolio: https://sites.google.com/view/matthew-vannicola-ai

---
