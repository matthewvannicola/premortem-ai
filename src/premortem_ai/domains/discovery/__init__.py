"""
Risk Discovery domain for the PreMortem AI pipeline.

This domain is responsible for:
    - Interpreting the project description
    - Extracting raw risk statements using LLM-assisted analysis
    - Normalizing, structuring, and preparing risk items
    - Ensuring outputs conform to the risk schema

The discovery stage produces the initial dataset that all downstream
pipeline stages depend on (scoring, themes, mitigation, summary).
"""

from .extractor import run_discovery

__all__ = [
    "run_discovery",
]
