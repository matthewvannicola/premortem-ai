"""
Pipeline execution layer for the PreMortem AI system.

This package coordinates all ordered pipeline stages, including:
    - Risk Discovery
    - Scoring
    - Theme Clustering
    - Mitigation Generation
    - Summary Synthesis
    - Report Assembly

The pipeline modules are responsible for:
    - Orchestrating domain components
    - Managing execution context
    - Enforcing schema validation
    - Selecting models consistently
    - Maintaining deterministic run metadata

External modules should only import high-level orchestration interfaces,
not individual domain implementations.
"""

from .orchestrator import PipelineOrchestrator, PipelineExecutionError

__all__ = [
    "PipelineOrchestrator",
    "PipelineExecutionError",
]
