# SYSTEM_CANON.md

## Purpose

This document defines the **non-negotiable architectural rules and mental models** for the PreMortem AI system.

It exists to ensure the system remains:

* Deterministic where possible
* Observable and debuggable
* Safe around AI components
* Easy for engineers to reason about
* Production-ready rather than prototype-driven

If a design decision conflicts with this document, **the system canon wins**.

---

## System Overview Diagram

                +------------+
                |   Client   |
                +------------+
                       |
                       v
                +------------+
                |    API     |
                +------------+
                       |
                       v
                +------------+
                |  Schemas   |
                +------------+
                       |
                       v
                +------------+
                |  Services  |
                +------------+
                       |
                       v
                +------------+
                |    Core    |
                +------------+
                       |
                       v
                +------------+
                | External   |
                +------------+

---

# 1. System Philosophy

PreMortem AI is **not an AI demo**.

It is a **risk and operations intelligence system that uses AI as a component**, not as the source of truth.

Core principles:

1. **Determinism over magic**
2. **Contracts over assumptions**
3. **Pipelines over monolith logic**
4. **Guardrails around AI**
5. **Observability everywhere**

AI may assist in discovery, but **final outputs must pass deterministic validation**.

## Request Lifecycle

Client Request
↓
FastAPI Route
↓
Schema Validation
↓
Service Orchestration
↓
Pipeline Execution
↓
Core Logic Evaluation
↓
Response Serialization
↓
JSON Response

---

# 2. Layered Architecture (Mandatory)

Every request through the system must map to this structure:

Client
↓
API Layer
↓
Validation Layer
↓
Core Logic
↓
Services
↓
External Systems
↓
Response

## Folder Mapping

api/
HTTP routes only

schemas/
Pydantic request/response contracts

core/
Deterministic logic and rules

services/
Workflows and orchestration

clients/
External system wrappers (LLMs, APIs)

utils/
Small helpers with no business logic

## LLM Interaction Rules

LLMs may only be called from the services layer.

LLM responses must:

1. Use structured output
2. Pass schema validation
3. Be logged
4. Never directly influence final decisions

---

# 3. AI Safety Model

LLMs are **non-deterministic generators**.

Therefore they must never:

* Directly control system decisions
* Write to the database without validation
* Bypass schema validation

LLM outputs must always pass through:

LLM Output
↓
Schema Validation
↓
Deterministic Filtering
↓
Core Logic Evaluation

If validation fails, the output is rejected.

## Idempotency

Pipeline stages must be safe to retry.

Running the same stage twice must not produce different system state.

---

# 4. Deterministic Core

The **core/** directory contains pure logic.

Rules:

* No HTTP
* No database access
* No LLM calls
* No external API calls

Core functions must be:

* Pure
* Deterministic
* Unit testable

Example responsibilities:

* risk scoring
* signal normalization
* classification rules

## Traceability

Every risk output must be traceable back to:

document_id
signals
evidence spans
pipeline stage outputs
model responses

---

# 5. Services Layer

The **services/** layer handles workflows.

Services may:

* Call LLMs
* Retry failures
* Orchestrate pipelines
* Coordinate multiple steps

Services must **never contain core business rules**.

They only coordinate execution.

## Data Model Philosophy

System objects must be explicit.

Examples:

Document
Signal
Risk
Evidence
Report

Implicit structures are forbidden.

---

# 6. Pipeline Mental Model

PreMortem operates as a **multi-stage pipeline**.

Example:

Input
↓
Discovery
↓
Signal Extraction
↓
Classification
↓
Validation
↓
Risk Evaluation
↓
Report Generation

Each stage must:

* Accept structured input
* Produce structured output
* Be independently testable

---

# 7. Contracts (Schemas)

All system boundaries must use explicit schemas.

Examples:

* API request models
* API response models
* LLM structured outputs
* Internal pipeline objects

Benefits:

* type safety
* validation
* easier debugging

---

# 8. Observability Requirements

Production systems must be explainable.

PreMortem must support:

* structured logs
* trace IDs
* stage-level logging
* error classification

Logs should answer:

* what happened
* where it happened
* why it failed

---

# 9. Error Handling

Errors must be categorized:

Validation Errors
Invalid inputs or schema failures

LLM Errors
Malformed or rejected model output

Service Errors
External API failures

System Errors
Unexpected internal failures

Every error must produce:

* a clear log
* a meaningful API response

---

# 10. Testing Strategy

Testing priority:

1. Core logic (highest priority)
2. Pipeline stages
3. API routes
4. Integration flows

LLM calls should be mocked during tests.

---

# 11. System Evolution Rules

When adding features:

Do NOT:

* bypass schemas
* put logic in routes
* mix deterministic rules into services

Always ask:

"Which layer owns this responsibility?"

---

# 12. Definition of Production-Ready

A feature is production-ready when:

* Inputs are validated
* Outputs are structured
* Core logic is deterministic
* Logs exist for each stage
* Failures are handled
* Tests exist

---

# 13. Long-Term System Direction

PreMortem will evolve toward:

* AI-assisted operational intelligence
* deterministic risk evaluation
* enterprise-grade observability
* audit-ready decision pipelines

The system must remain **explainable, auditable, and reliable** even as AI capabilities increase.
