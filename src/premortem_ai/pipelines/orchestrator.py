"""
orchestrator.py

Functional pipeline orchestrator for PreMortem AI.
Executes all stages (discovery → scoring → themes → mitigation → summary)
and returns a PipelineResponse.
"""

from premortem_ai.pipelines.context_manager import PipelineContext
from premortem_ai.pipelines.execution_graph import get_execution_graph
from premortem_ai.models import PipelineRequest, PipelineResponse

# Domain engines
from premortem_ai.domains.discovery import run_discovery
from premortem_ai.domains.scoring import compute_scores_for_risks
from premortem_ai.domains.themes import cluster_themes
from premortem_ai.domains.mitigation import generate_mitigations
from premortem_ai.summary import run_summary

from premortem_ai.core.logger import info


def run_pipeline(request: PipelineRequest) -> PipelineResponse:
    """
    Main orchestrator for the PreMortem AI pipeline.
    Executes each stage in order and returns a PipelineResponse.

    Args:
        request: PipelineRequest describing the project
    """
    ctx = PipelineContext()
    ctx.request_metadata = {
        "project_title": request.project_title,
        "model_override": request.model_version_override,
    }

    stages = get_execution_graph()

    for stage in stages:
        info(f"Running stage: {stage}")
        ctx.mark_stage_start(stage)

        if stage == "discovery":
            ctx.risks = run_discovery(
                request.project_description,
                model_override=request.model_version_override,
            )

        elif stage == "scoring":
            ctx.scores = compute_scores_for_risks(
                ctx.risks,
                model_override=request.model_version_override,
            )

        elif stage == "themes":
            ctx.themes = cluster_themes(
                ctx.risks,
                ctx.scores,
                model_override=request.model_version_override,
            )

        elif stage == "mitigation":
            ctx.mitigations = generate_mitigations(
                ctx.risks,
                ctx.scores,
                ctx.themes,
                model_override=request.model_version_override,
            )

        elif stage == "summary":
            ctx.summary = run_summary(
                ctx.risks,
                ctx.scores,
                ctx.themes,
                ctx.mitigations,
                model_override=request.model_version_override,
            )

        else:
            raise RuntimeError(f"Unexpected pipeline stage '{stage}'")

        ctx.mark_stage_end(stage)
        info(f"Completed stage: {stage}")

    # ---------------------------------------------------------
    # BUILD RESPONSE
    # ---------------------------------------------------------
    response = PipelineResponse(
        project_title=request.project_title,
        risks=list(ctx.risks.values()),
        scores=list(ctx.scores.values()),
        themes=ctx.themes,
        mitigations=ctx.mitigations,
        summary=ctx.summary,
        timings=ctx.stage_timings,
    )

    return response
