# Data Flow Diagram (Text-Based)

This document provides a text-based diagram showing how information flows through the PreMortem AI system from intake → inference → scoring → reporting → audit logging.

It is meant to visually complement the architecture overview.

---

## End-to-End Data Flow (Text Version)

```
Google Sheets (Project Input)
↓
Pipedream Workflow
    • Normalize input
↓
LLM – Discovery Pass
    • Extract raw risks
    • Schema validation (risk_output.schema.json)
↓
LLM – Scoring Pass
    • Apply severity model
    • Normalize + deduplicate + clamp enums
↓
LLM – Summary Pass
    • Generate executive summary
    • Assemble final structured dataset
↓
Reporting Engine
    • Google Doc generation
    • PDF export
    • JSON dataset
↓
Notion Audit Log
    • run_id
    • timestamps
    • retry_count
    • cleaned final dataset
```

---

## Workflow Notes

- **Every inference pass** produces JSON validated against strict schemas.  
- **Normalization** ensures consistent formatting and allowed values.  
- **Retries & fallback logic** ensure robustness when LLM output is malformed.  
- **The reporting engine** consolidates LLM outputs into executive-facing artifacts.  
- **The audit log** ensures traceability, versioning, and compliance.

---

# End of Document
