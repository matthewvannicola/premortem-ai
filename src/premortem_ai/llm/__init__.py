"""
LLM Integration Layer for PreMortem AI.

This package contains all logic related to interacting with large language models,
including:

    - openai_client     → governed wrapper around OpenAI API calls
    - model_router      → deterministic model selection & override handling
    - prompt_router     → (optional) routing of prompt templates by task
    - parsers           → structured response interpreters for discovery / scoring

The goal of this layer is to isolate all LLM dependencies behind a stable internal API.

External modules (orchestrator, services, pipelines) should always import LLM
functionality from here rather than interacting with the OpenAI client directly.

Example usage:

    from premortem_ai.llm import get_llm_client, resolve_model_version

"""

from .openai_client import LLMClient, get_llm_client
from .model_router import resolve_model_version, validate_model, get_reasoning_model

__all__ = [
    "LLMClient",
    "get_llm_client",
    "resolve_model_version",
    "validate_model",
    "get_reasoning_model",
]
