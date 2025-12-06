"""
run_pipeline.py

The master orchestrator for PreMortem AI.
This function executes the full analytic workflow:

    1. Discovery
    2. Scoring
    3. Theme Clustering
    4. Mitigation Strategy Generation
    5. Executive Summary Synthesis

Returns:
    PipelineResponse — the canonical structured output for all interfaces
    (API, CLI, UI, PDF generator, etc.)
"""

from premortem_ai.models import PipelineRequest, PipelineResponse
from premortem_ai.utils.logger import info, error
from premortem_ai.exceptions import PipelineExecutionError

from premortem_ai.domains.discovery import run_discovery
from premortem_ai.domains.scoring import run_scoring
from premortem_ai.domains.themes import cluster_themes
from premortem_ai.domains.mitigation import generate_mitigations

from premortem_ai.summary import build_summary


def run_pipeline(request: PipelineRequest) -> PipelineResponse:
    """
    Execute the full PreMortem AI processing chain for a given project.

    Args:
        request (PipelineRequest): User-supplied input containing project description,
        configuration overrides, and model preferences.

    Returns:
        PipelineResponse: Full structured output containing risks, scores,
        themes, mitigations, and summary.
    """

    info("🚀 Starting PreMortem AI pipeline execution...")

    try:
        # ------------------------------------------------------------------
        # STEP 1 — DISCOVERY
        # ------------------------------------------------------------------
        info("Step 1: Running discovery...")
        risks = run_discovery(
            project_description=request.project_description,
            model_override=request.model_version_override,
        )
        info(f"✓ Discovery complete — {len(risks)} risks identified.")

        # ------------------------------------------------------------------
        # STEP 2 — SCORING
        # ------------------------------------------------------------------
        info("Step 2: Running scoring...")
        scores = run_scoring(
            risks=risks,
            model_override=request.model_version_override,
        )
        info("✓ Scoring complete.")

        # ------------------------------------------------------------------
        # STEP 3 — THEME CLUSTERING
        # ------------------------------------------------------------------
        info("Step 3: Clustering themes...")
        themes = cluster_themes(
            risks=risks,
            scores=scores,
            model_override=request.model_version_override,
        )
        info(f"✓ Theme clustering complete — {len(themes)} themes generated.")

        # ------------------------------------------------------------------
        # STEP 4 — MITIGATIONS
        # ------------------------------------------------------------------
        info("Step 4: Generating mitigations...")
        mitigations = generate_mitigations(
            risks=risks,
            model_override=request.model_version_override,
        )
        info("✓ Mitigation generation complete.")

        # ------------------------------------------------------------------
        # STEP 5 — EXECUTIVE SUMMARY
        # ------------------------------------------------------------------
        info("Step 5: Building executive summary...")
        summary = build_summary(
            risks=risks,
            scores=scores,
            themes=themes,
            mitigations=mitigations,
            model_override=request.model_version_override,
        )
        info("✓ Executive summary complete.")

        # ------------------------------------------------------------------
        # BUILD FINAL PIPELINE RESPONSE
        # ------------------------------------------------------------------
        response = PipelineResponse(
            request=request,
            risks=risks,
            scores=scores,
            themes=themes,
            mitigations=mitigations,
            summary=summary,
        )

        info("🎉 PreMortem AI pipeline completed successfully.")
        return response

    except Exception as exc:
        error(f"Pipeline failure: {exc}")
        raise PipelineExecutionError(f"Pipeline failed: {exc}")
