"""
execution_graph.py

Defines the canonical ordered execution stages for the PreMortem AI system.
This module is the single source of truth for pipeline flow, ensuring that
domain services, orchestrators, and external callers remain synchronized.

Each stage name MUST correspond to:
    - a domain module (premortem_ai/domains/<stage>)
    - a service function that implements that stage
    - a PipelineContext attribute that stores the result

This ensures deterministic behavior and simplifies validation + debugging.
"""

PIPELINE_STAGES = [
    "discovery",
    "scoring",
    "themes",
    "mitigation",
    "summary",
]


def validate_stage_name(stage: str) -> None:
    """Ensure a stage name is valid before execution."""
    if stage not in PIPELINE_STAGES:
        raise ValueError(
            f"Invalid pipeline stage '{stage}'. "
            f"Must be one of: {', '.join(PIPELINE_STAGES)}"
        )


def get_execution_graph() -> list:
    """
    Return the canonical ordered list of pipeline stages.
    A defensive copy is returned to avoid mutation.
    """
    return PIPELINE_STAGES.copy()
