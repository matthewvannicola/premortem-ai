"""
LLM Integration Layer for PreMortem AI
--------------------------------------

This package centralizes all logic related to interacting with large language
models. It provides a clean, governed, and stable API surface so that upstream
systems (orchestrators, services, pipelines) NEVER need to import OpenAI client
objects directly or manage model selection manually.

This layer ensures:
    • Consistent, enterprise-safe model invocation
    • Deterministic model routing & validation
    • Clear separation between governance and execution
    • JSON-mode enforcement (via LLMClient)
    • Full observability (metrics + tracing)
    • Future extensibility for multi-model pipelines

Modules:
    openai_client:
        Thin, governed wrapper around the OpenAI Responses API.
        Provides retry logic, JSON-mode, telemetry, and strict errors.

    model_router:
        Centralized model governance.
        Handles overrides, defaults, validation, and specialized routing
        (e.g., reasoning vs. summarization model selection).

    prompt_router (optional future module):
        If added, would handle selection of prompt templates by task
        (discovery, scoring, themes, mitigation, summaries, etc.).

    parsers (optional future module):
        If added, provides structured response interpreters for converting
        raw JSON LLM output into the project's Pydantic schema models.

Public API:
    from premortem_ai.llm import (
        get_llm_client,
        resolve_model_version,
        validate_model,
        get_reasoning_model,
        get_summarization_model,
    )

Downstream code should treat this as the single authoritative entry point for
all LLM interactions.
"""

from .openai_client import LLMClient, get_llm_client
from .model_router import (
    resolve_model_version,
    validate_model,
    get_reasoning_model,
    get_summarization_model,
)

__all__ = [
    # Client
    "LLMClient",
    "get_llm_client",

    # Routing / Governance
    "resolve_model_version",
    "validate_model",
    "get_reasoning_model",
    "get_summarization_model",
]
