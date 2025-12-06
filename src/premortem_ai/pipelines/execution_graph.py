"""
execution_graph.py

Defines the ordered execution stages for the PreMortem AI pipeline.
Provides a canonical reference for pipeline structure and validation.
"""

PIPELINE_STAGES = [
    "discovery",
    "scoring",
    "themes",
    "mitigation",
    "summary",
]

def validate_stage_name(stage: str) -> None:
    if stage not in PIPELINE_STAGES:
        raise ValueError(
            f"Invalid pipeline stage '{stage}'. "
            f"Must be one of: {', '.join(PIPELINE_STAGES)}"
        )

def get_execution_graph() -> list:
    """Return the canonical ordered list of stages."""
    return PIPELINE_STAGES.copy()
