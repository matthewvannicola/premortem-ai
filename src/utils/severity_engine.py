"""
Severity scoring utilities for PreMortem AI.

This module provides a deterministic scoring engine that blends:
- LLM-generated severity values
- rule-based normalization
- optional weighting
- optional human override signals

The goal is to produce consistent, comparable severity ratings across:
- multiple LLM passes
- multiple assessors
- multiple project snapshots

This engine is intentionally lightweight, dependency-free, and fully deterministic.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union


class SeverityEngine:
    """
    A deterministic scoring engine used to compute normalized severity ratings
    for individual risk items.

    Supports:
    - integer or float severity inputs
    - optional LLM scores
    - optional human override signals
    - range normalization
    - weight blending

    Intended Use
    ------------
    severity = engine.compute({
        "llm_score": 4.2,
        "human_score": 3,
