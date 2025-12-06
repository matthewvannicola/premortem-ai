# PreMortem AI

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Automated risk discovery, scoring, mitigation planning, and executive summarization for complex projects.
This system provides a deterministic, domain-driven architecture for generating structured pre-mortem analyses using LLMs behind a governed API.

---

## 1. Overview

PreMortem AI is an end-to-end automated pre-mortem engine that identifies potential project failures before execution. The system ingests a project description and produces a complete risk package:

- Structured risk items
- Probability and impact scoring
- Risk themes
- Mitigation strategies
- Executive summaries
- Machine-readable pipeline response output

The design follows a domain-driven, layered architecture to ensure extensibility, traceability, and deterministic behavior across LLM runs.

---

## 2. High-Level Architecture

The system is built on a domain-driven, layered architecture designed for determinism, extensibility, and strict schema guarantees.

**LLM Integration Layer**  
Handles model routing, structured inference, versioning, and strict schema-validated responses.

**Domain Engines**  
Self-contained engines for discovery, scoring, mitigation, and summary. Each domain includes its own prompts, validators, and error boundaries.

**Pipeline Orchestration Layer**  
Defines the execution graph, runs each domain in sequence, manages shared context, enforces reproducibility, and produces the final `PipelineResponse`.

**Core Utilities**  
Cross-cutting support modules: logging, ID generation, schema validation, text normalization, file I/O, and timing.

**API + CLI Layer**  
Public interfaces exposing the pipeline to external systems with clean, stable contracts.

**Configuration Layer**  
Centralized model defaults, environment overrides, and pipeline feature flags.

This architecture cleanly separates concerns and supports rapid extension without breaking existing surfaces.

---

## 3. Repository Structure

```
premortem_ai/
│
├── analysis_service/                  # High-level analysis entrypoints consumed by API/CLI
│   ├── __init__.py
│   └── service.py
│
├── api/                               # Public interfaces to the pipeline
│   ├── cli.py                         # CLI entrypoint
│   ├── fastapi_app.py                 # FastAPI application
│   ├── model_router.py                # API-level model routing
│   └── __init__.py
│
├── config/                            # Centralized configuration
│   ├── settings.py                    # Environment and global settings
│   ├── pipeline_configs.py            # Pipeline-level runtime configuration
│   └── __init__.py
│
├── core/                              # Foundational utilities reused across domains
│   ├── file_io.py
│   ├── id_generation.py
│   ├── logger.py
│   ├── model_selector.py
│   ├── normalize_text.py
│   ├── schema_validation.py
│   ├── timer.py
│   └── __init__.py
│
├── domains/                           # Business logic for each stage of the pipeline
│   ├── discovery/
│   │   ├── discovery_engine.py
│   │   ├── prompts.py
│   │   ├── validators.py
│   │   └── __init__.py
│   │
│   ├── scoring/
│   │   ├── scoring_engine.py
│   │   ├── prompts.py
│   │   ├── validators.py
│   │   └── __init__.py
│   │
│   ├── mitigation/
│   │   ├── mitigation_engine.py
│   │   ├── prompts.py
│   │   ├── validators.py
│   │   └── __init__.py
│   │
│   ├── summary/
│   │   ├── summary_engine.py
│   │   ├── prompts.py
│   │   ├── validators.py
│   │   └── __init__.py
│   │
│   └── share/                         # Shared cross-domain logic
│       ├── models.py                  # Shared domain-level helper models
│       ├── validators.py              # Cross-domain validation rules
│       └── __init__.py
│
├── exceptions/                        # Canonical exception hierarchy
│   ├── errors.py
│   ├── validation_errors.py
│   └── __init__.py
│
├── llm/                               # Model routing and inference
│   ├── openai_client.py               # Wrapper around OpenAI client
│   ├── model_router.py                # Deterministic model selection for inference
│   ├── prompts/                       # Optional shared prompt templates
│   │   ├── base_templates.py
│   │   └── __init__.py
│   └── __init__.py
│
├── models/                            # Pydantic v2 schemas for structured data
│   ├── RiskItem.py
│   ├── ScoreItem.py
│   ├── ThemeItem.py
│   ├── MitigationItem.py
│   ├── Summary.py
│   ├── PipelineRequest.py
│   ├── PipelineResponse.py
│   └── __init__.py
│
├── observability/                     # Monitoring, metrics, and tracing
│   ├── metrics.py
│   ├── tracing.py
│   └── __init__.py
│
├── pipelines/                         # Execution graph and orchestrator
│   ├── context_manager.py
│   ├── execution_graph.py
│   ├── orchestrator.py
│   └── __init__.py
│
├── tests/                             # Unit + integration tests
│   ├── test_models.py
│   ├── test_pipelines.py
│   ├── test_orchestrator.py
│   └── __init__.py
│
└── utils/                             # Optional general-purpose helpers
    ├── text_utils.py
    ├── json_utils.py
    └── __init__.py
```

## 4. Processing Flow

The PreMortem pipeline executes in four deterministic stages.  
Each stage is handled by its own domain engine, enforces strict schema validation,
and writes structured results to the shared pipeline context.

### 4.1 Discovery:

- Extracts atomic risks from the project description using domain prompts and structured inference.
- Normalizes all text fields and assigns unique, stable risk IDs.
- Produces a list of `RiskItem` objects.
- Applies domain-level and shared validators to guarantee completeness and structural integrity.

### 4.2 Scoring:

- Evaluates each discovered risk and assigns probability and impact values.
- Combines rule-based logic with LLM-assisted scoring under strict schema constraints.
- Produces `ScoreItem` objects keyed by the originating risk ID.
- Enforces bounded numeric ranges and probabilistic coherence across all scores.

### 4.3 Mitigation:

- Generates targeted mitigation strategies for each risk.
- Uses deterministic templates and structured LLM calls to ensure consistency and reproducibility.
- Produces `MitigationItem` objects, each referencing an existing risk ID.
- Validates content quality, duplication, and alignment with the underlying risk.

### 4.4 Summary:

- Synthesizes a leadership-ready executive summary of the overall risk landscape.
- Groups risks into themes, highlights critical patterns, and frames recommended actions.
- Produces a structured `Summary` object tied to all upstream artifacts.
- Ensures semantic alignment with discovered risks, scored values, and mitigation outputs.

All stage outputs must successfully parse into their Pydantic V2 schemas.  
If any step fails validation, the orchestrator stops execution and returns a structured error.

---

## 5. Pipeline Orchestration

The orchestration layer coordinates all domain engines into a deterministic,
fully auditable execution sequence. It ensures that each stage operates on
validated inputs, produces validated outputs, and writes results into the
shared pipeline context.

### 5.1 execution_graph.py:

Defines the ordered workflow of the pipeline:

    Discovery → Scoring → Mitigation → Summary

The execution graph specifies:

- The exact sequence of domain engines
- Input/output dependencies for each stage
- Enforcement of schema boundaries between stages
- Strict progression rules (no stage may execute without validated upstream data)

This module acts as the canonical blueprint for the entire system.

### 5.2 context_manager.py:

Maintains all intermediate state across the pipeline lifecycle.

Responsibilities include:

- Storing validated outputs from each domain
- Exposing typed getters/setters for structured access
- Ensuring immutability of finalized stage outputs
- Providing a controlled interface for cross-domain data consumption
- Supporting future parallel execution or caching strategies

The context manager is the single source of truth for pipeline state.

### 5.3 orchestrator.py:

Executes the pipeline by walking the execution graph and coordinating each domain engine.

Core responsibilities:

- Initialize context and runtime configuration
- Execute each stage in sequence with strict error boundaries
- Enforce schema validation before and after each domain engine runs
- Capture timings, logs, and metadata for observability
- Halt immediately on validation failures and surface structured errors
- Produce the final `PipelineResponse` with all validated artifacts

The orchestrator ensures reproducibility, determinism, and traceability of every run.

### 5.4 Guarantees Provided by the Orchestration Layer:

- Deterministic order of execution
- No cross-stage mutation after a stage is finalized
- Full audit trail of inputs, outputs, timings, and model versions
- Clear separation of concerns between domain logic and pipeline control flow
- Predictable failure behavior with typed, structured error responses

This orchestration design enables enterprise reliability while preserving modularity,
making each domain engine independently testable and easily replaceable.

---

## 6. LLM Integration Layer

All LLM interaction is routed through a controlled inference layer that enforces
deterministic behavior, strict schema validation, and version-governed model usage.
No domain engine interacts with an LLM directly.

### 6.1 openai_client.py:

Provides the unified interface for all inference operations.

Responsibilities:

- Perform all outbound LLM calls through a single governed client
- Attach model version, temperature, and system prompts deterministically
- Apply request-level timeouts, retries, and error normalization
- Record raw input/output payloads for observability
- Never return unvalidated model output to upstream components

This guarantees that all inference behavior is consistent, auditable, and centrally controlled.

### 6.2 model_router.py:

Determines which model should be used for each operation.

Responsibilities:

- Map each domain engine to its designated model tier
- Enforce stable model versions via configuration (e.g., `gpt-5.1`, `gpt-4o-mini`)
- Support pluggable future providers without changing domain logic
- Ensure deterministic selection based on pipeline settings and environment overrides

Domain engines do not choose their models—routing is fully centralized.

### 6.3 Structured Prompt Templates:

Each domain uses tightly scoped prompt templates that define:

- Required output schema
- Canonical vocabulary and formatting rules
- Deterministic phrasing to minimize inference variance
- Clear examples of valid and invalid responses
- Instructions forbidding creative formatting, unrequested narratives, or deviations

Prompts are intentionally rigid to maintain reproducibility across runs.

### 6.4 Structured Response Enforcement:

Every LLM response must successfully parse into a Pydantic V2 schema
before the pipeline is allowed to progress.

Process:

1. LLM returns raw text.
2. The client attempts to parse the response into the domain’s schema (e.g., `RiskItem`, `ScoreItem`, `MitigationItem`, `Summary`).
3. If parsing fails:
   - The pipeline halts immediately.
   - A structured `ValidationError` is raised.
   - The orchestrator returns a typed error response containing:
     - offending payload
     - model version
     - domain step
     - parsing details

No partially valid or malformed outputs are ever accepted.

### 6.5 Enforcement Guarantees:

The integration layer ensures:

- All inference outputs are strongly typed
- No downstream stage receives unstructured or ambiguous data
- Full reproducibility of model behavior based on controlled prompts and parameters
- Clear audit trails for debugging and compliance
- Zero tolerance for schema drift or format deviations

This transforms LLM inference from an unbounded text-generation process
into a **strictly governed, contract-enforced data transformation step**.

### 6.6 Provider-Agnostic Architecture:

By isolating inference behind this layer, the system can adopt additional
providers (e.g., Anthropic, Azure OpenAI, local models) by implementing:

- A new client wrapper
- A routing strategy
- Schema validation bindings

No domain engine or pipeline component requires modification.

---

## 7. API Usage

Start the FastAPI server:

```
uvicorn premortem_ai.api.fastapi_app:app --reload
```

Submit a request:

```
POST /analyze
{
  "project_description": "..."
}
```

The response conforms to `PipelineResponse`.

---

## 8. CLI Usage

Run a premortem from the command line:

```
premortem analyze "Your project description here"
```

Output is written to the console and optionally saved as JSON.

---

## 9. Configuration

All configuration is centralized in `config/settings.py`.
The configuration layer supports:

- Environment variable overrides
- Model version selection
- Pipeline feature toggles
- Logging verbosity
- Output paths

Pipeline-specific options are defined in `pipeline_configs.py`.

## 10. Why This System Exceeds Existing Pre-Mortem Tools

This implementation distinguishes itself through several core capabilities:

**1. Strong Schema Guarantees**
All LLM output must conform to strict Pydantic schemas, eliminating malformed responses.

**2. Modular Domain Architecture**
Discovery, scoring, mitigation, and summary are independently replaceable modules.

**3. Deterministic Pipeline Execution**
Execution graphs enforce a controlled order of operations with predictable state transitions.

**4. Enterprise-Ready Observability**
Integrated logging, metrics hooks, and timing instrumentation support production environments.

**5. Separation of Concerns**
The API, CLI, pipeline orchestrator, domain logic, and LLM client are fully decoupled.

**6. Extensibility**
New engines, scoring models, or LLM backends can be added with minimal code changes.

The pipeline is fully auditable: every stage logs inputs, outputs, timings, model versions, and validation boundaries to support enterprise governance.

---

## 11. Extending the System

To add a new domain:

1. Create a folder under `domains/`
2. Implement prompt templates and a domain engine
3. Define any domain-specific schemas
4. Register the new step in the execution graph
5. Add validation rules in `domains/share` if needed

To incorporate a new LLM provider, implement:

- A client wrapper
- A routing strategy
- Structured response validation logic

---

## 12. Testing

Tests are located under `tests/` and should cover:

- Domain-level engines
- Pipeline orchestration
- Schema validation
- LLM mock output parsing

---

## 13. License

This project is licensed under the [MIT License](./LICENSE). See the LICENSE file for details.

---

If you’d like to connect, collaborate, or discuss automation systems:

- **GitHub:** https://github.com/matthewvannicola 
- **LinkedIn:** https://www.linkedin.com/in/matthew-vannicola  
- **Portfolio:** https://sites.google.com/view/matthew-vannicola-ai/  
- **Email:** <matthew.vannicolajr@gmail.com>  

Feel free to reach out for project collaborations, architecture questions, workflow design, or AI-powered automation opportunities.

---

## Contributions

Contributions, suggestions, or improvements are welcome.
Feel free to open an issue or submit a pull request.
