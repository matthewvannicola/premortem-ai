"""
run_pipeline.py

The top-level orchestration engine for the PreMortem AI pipeline.

Responsible for:
    - building & preparing PipelineContext
    - validating execution graph
    - dispatching each stage to the appropriate domain service
    - recording execution timings
    - returning structured PipelineResponse

This module intentionally avoids business logic.
Actual computation lives inside domain packages.
"""

from typing import Callable, Dict
from premortem_ai.pipelines.execution_graph import (
    get_execution_graph,
    validate_stage_name,
)
from premortem_ai.pipelines.context_manager import PipelineContext

# Domain service imports (each must expose `run_stage(context)`)

from premortem_ai.domains.discovery.discovery_engine import run_discovery_stage
from premortem_ai.domains.scoring.scoring_engine import run_scoring_stage
from premortem_ai.domains.themes.theme_clusterer import run_theme_stage
from premortem_ai.domains.mitigation.mitigation_generator import run_mitigation_stage
from premortem_ai.domains.summary.summary_generator import run_summary_stage


# -----------------------------------------------------------
# Mapping between stage name and callable service function
# -----------------------------------------------------------

STAGE_DISPATCH_TABLE: Dict[str, Callable] = {
    "discovery": run_discovery_stage,
    "scoring": run_scoring_stage,
    "themes": run_theme_stage,
    "mitigation": run_mitigation_stage,
    "summary": run_summary_stage,
}


def run_pipeline(request) -> PipelineContext:
    """
    Execute all stages of the PreMortem AI system in deterministic order.

    Args:
        request: Pydantic PipelineRequest model

    Returns:
        PipelineContext containing all stage outputs
    """

    context = PipelineContext()
    context.request_metadata = request.model_dump()

    execution_order = get_execution_graph()

    for stage in execution_order:
        validate_stage_name(stage)
        handler = STAGE_DISPATCH_TABLE.get(stage)

        if handler is None:
            raise RuntimeError(f"No handler registered for stage '{stage}'")

        # Measure stage runtime
        context.mark_stage_start(stage)
        handler(context=context, request=request)
        context.mark_stage_end(stage)

    return context
