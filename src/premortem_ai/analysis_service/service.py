"""
analysis_service/service.py

High-level service responsible for executing the full PreMortem AI pipeline.
This module provides the public-facing interface used by:

    - REST API handlers
    - CLI tools
    - SDK consumers
    - Pipedream / Make.com integrations
    - Internal automation workflows

The AnalysisService orchestrates:
    1. Input validation (PipelineRequest)
    2. Orchestrator execution
    3. Result packaging (PipelineResponse)
    4. Error wrapping with domain-friendly exceptions
"""

from premortem_ai.models import PipelineRequest, PipelineResponse
from premortem_ai.pipelines.orchestrator import PipelineOrchestrator


class AnalysisService:
    """
    Thin service wrapper around the pipeline orchestrator.

    Provides a stable boundary where:
        - API / CLI / SDKs interact with the system
        - Versioning and overrides are centrally enforced
        - Errors can be abstracted and normalized
    """

    def __init__(self, default_model_version: str = "gpt-5.1", default_pipeline_version: str = "v1.0.0"):
        self.default_model_version = default_model_version
        self.default_pipeline_version = default_pipeline_version
        self._orchestrator = PipelineOrchestrator()

    # ----------------------------------------------------------------------
    # Main public service entry point
    # ----------------------------------------------------------------------
    def run_analysis(self, raw_request: dict) -> PipelineResponse:
        """
        Execute a full PreMortem AI pipeline run.

        Args:
            raw_request (dict):
                Raw user or API payload. Will be normalized and validated
                using PipelineRequest.from_api().

        Returns:
            PipelineResponse:
                Fully validated pipeline output containing a RiskReport.

        Raises:
            ValueError: For malformed inputs.
            RuntimeError: For unexpected pipeline failures.
        """

        # -------------------------------------------------------------
        # 1. Normalize + validate request
        # -------------------------------------------------------------
        request = PipelineRequest.from_api(raw_request)

        model_version = (
            request.model_version_override
            if request.model_version_override
            else self.default_model_version
        )

        pipeline_version = (
            request.pipeline_version_override
            if request.pipeline_version_override
            else self.default_pipeline_version
        )

        # -------------------------------------------------------------
        # 2. Execute orchestrator
        # -------------------------------------------------------------
        try:
            report = self._orchestrator.execute(
                project_description=request.project_description,
                max_risks=request.max_risks,
                model_version=model_version,
                pipeline_version=pipeline_version,
                include_metadata=request.include_metadata,
            )
        except Exception as exc:
            raise RuntimeError(f"Pipeline execution failed: {exc}") from exc

        # -------------------------------------------------------------
        # 3. Wrap & return stable response shape
        # -------------------------------------------------------------
        return PipelineResponse.from_report(report)

    # ----------------------------------------------------------------------
    # Convenience helper for CLI / debugging
    # ----------------------------------------------------------------------
    def run(self, project_description: str) -> PipelineResponse:
        """
        Convenience wrapper allowing a simple string → full analysis run.
        Ideal for CLI usage or lightweight integrations.
        """
        return self.run_analysis({"project_description": project_description})
