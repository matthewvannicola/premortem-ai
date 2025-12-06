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

## 2. High-Level Architecture

The system is organized into distinct layers with clear responsibility boundaries:

**LLM Integration Layer**
Abstracts model selection, routing, and structured inference through a controlled OpenAI client.

**Domain Engines**
Modular engines responsible for discovery, scoring, mitigation, and summary generation. Each engine is independently testable and uses domain-specific prompts and validators.

**Pipeline Orchestration Layer**
Modular engines responsible for discovery, scoring, mitigation, and summary generation. Each engine is independently testable and uses domain-specific prompts and validators.

**Core Utilities**
Shared foundational components including logging, file I/O, ID generation, schema validation, text normalization, and timing instrumentation.

**API and CLI Interfaces**
Expose the pipeline to external consumers through a FastAPI service and a command-line interface.

**Configuration Layer**
Centralizes runtime configuration, model selection defaults, pipeline options, and environment-driven overrides.

The architecture is intentionally model-agnostic and can operate with any LLM that adheres to the required response schemas.

---

## 3. Repository Structure

```
premortem_ai/
│
├── analysis_service/          # High-level analysis functions consumed by API/CLI
│
├── api/                       # Public interfaces
│   ├── cli.py                 # CLI entrypoint
│   ├── fastapi_app.py         # REST API service
│   └── __init__.py
│
├── config/                    # System configuration and pipeline settings
│   ├── settings.py
│   ├── pipeline_configs.py
│   └── __init__.py
│
├── core/                      # Shared foundational components
│   ├── file_io.py
│   ├── id_generation.py
│   ├── logger.py
│   ├── model_selector.py
│   ├── normalize_text.py
│   ├── schema_validation.py
│   ├── timer.py
│   └── __init__.py
│
├── domains/                   # Primary business logic organized by domain
│   ├── discovery/             # Risk extraction
│   ├── scoring/               # Probability and impact scoring
│   ├── mitigation/            # Mitigation generation
│   ├── summary/               # Executive summaries
│   └── share/                 # Cross-domain validators, shared checks, and models
│
├── exceptions/                # Canonical exception hierarchy
│
├── llm/                       # LLM routing and client wrappers
│
├── models/                    # Pydantic V2 schema definitions
│   ├── RiskItem.py
│   ├── ScoreItem.py
│   ├── ThemeItem.py
│   ├── MitigationItem.py
│   ├── Summary.py
│   ├── PipelineRequest.py
│   └── PipelineResponse.py
│
├── observability/             # Metrics, tracing hooks
│
├── pipelines/                 # Execution graph and orchestrator
│   ├── context_manager.py
│   ├── execution_graph.py
│   ├── orchestrator.py
│   └── __init__.py
│
├── tests/                     # Unit tests
│
└── utils/                     # Optional helpers
```

---

## 4. Processing Flow

The PreMortem analysis executes in four controlled stages:

### 4.1 Discovery:

- Extracts atomic risks from project input.
- Normalizes language and produces structured `RiskItem` objects.
- Performs validation against discovery schemas.

### 4.2 Scoring:

- Assigns probability and impact using a ruleset and LLM-assisted inference.
- Produces `ScoreItem` instances linked to each risk by unique ID.

### 4.3 Mitigation:

- Generates mitigation steps using deterministic templates and structured LLM calls.
- Produces `MitigationItem` objects.

### 4.4 Summary:

- Produces an executive-style summary with narrative framing and risk groupings.
- Utilizes shared domain validators to ensure alignment with scored risks and mitigations.

Every output passes through the schema validation layer before continuing.

---

## 5. Pipeline Orchestration

The pipeline is coordinated through:

**execution_graph.py**
Defines the ordered sequence of domain operations.

**context_manager.py**
Maintains shared state and intermediate results across stages.

**orchestrator.py**
Runs the full graph, enforces error boundaries, logs execution durations, and emits a machine-readable `PipelineResponse`.

This structure allows:

- Strict reproducibility
- Swap-in domain modules
- Parallelizable future extensions
- Modular testing of each domain

---

## 6. LLM Integration Layer

The system does not call LLMs directly. All inference routes through:

- `LLMClient` (OpenAI API wrapper)
- `model_router` (deterministic model selection)
- Structured prompt templates per domain
- Strict Pydantic V2 schema parsing and error recovery

This ensures:

- Version-controlled LLM behavior
- Auditability
- Deterministic field-level validation
- Production readiness for enterprise use cases

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

## 13. Liscense

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
