"""
Core utilities and shared system primitives for the PreMortem AI pipeline.

This module exposes foundational functions used across all pipeline domains,
including text normalization, schema enforcement, internal ID generation,
and dynamic model selection.

Design Principles:
- Zero business logic lives here.
- Everything in this module must be reusable across multiple domains.
- Functions must be deterministic and side-effect free where possible.
"""

from .normalize_text import normalize_text
from .schema_validation import validate_schema
from .id_generation import generate_risk_id, generate_theme_id
from .model_selector import select_model

__all__ = [
    "normalize_text",
    "validate_schema",
    "generate_risk_id",
    "generate_theme_id",
    "select_model",
]
