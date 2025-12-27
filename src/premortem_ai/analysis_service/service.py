"""
service.py

The AnalysisService coordinates:
    - request validation (Pydantic)
    - model routing
    - pipeline orchestration
    - response transformation

It is the only place in the system that directly invokes the pipeline engine.
"""

from typing import Any, Dict

from premortem_ai.pipelines import run_pipeline
from premortem_ai.models.pipeline_request import PipelineRequest
from premortem_ai.models.pipeline_response import PipelineResponse
from premortem_ai.llm.model_router import resolve_model_version
from premortem_ai.exceptions import ValidationError, PipelineExecutionError
from premortem_ai.observability.metrics import record_pipeline_execution
from premortem_ai.core.logger import logger


class AnalysisService:
    """
    High-level facade for executing the PreMortem AI system.

    API and CLI layers should call ONLY this class — never the pipeline
    orchestrator directly. This preserves abstraction boundaries.
    """

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    # Public Main Entry Point
    # ----------------------------------------------------------------------

    def execute(self, request_data: Dict[str, Any]) -> PipelineResponse:
        """
        Accept raw inbound request data (from FastAPI, CLI, workflow runners),
        validate it, execute the pipeline, and return a structured response.

        Args:
            request_data: dict containing request fields

        Returns:
            PipelineResponse
        """

        # ---------------------------------------------------------
        # 1. Validate request
        # ---------------------------------------------------------
        try:
            request = PipelineRequest(**request_data)
        except Exception as exc:
            logger.error(f"Request validation failed: {exc}")
            raise ValidationError(str(exc))

        # ---------------------------------------------------------
        # 2. Model routing
        # ---------------------------------------------------------
        try:
            request.model_version = resolve_model_version(
                request.model_version_override
            )
        except Exception as exc:
            logger.error(f"Model version resolution failed: {exc}")
            raise ValidationError(str(exc))

        # ---------------------------------------------------------
        # 3. Execute pipeline
        # ---------------------------------------------------------
        try:
            context = run_pipeline(request)
        except Exception as exc:
            logger.exception(f"Pipeline execution failed: {exc}")
            raise PipelineExecutionError(str(exc))

        # ---------------------------------------------------------
        # 4. Record metrics
        # ---------------------------------------------------------
        try:
            record_pipeline_execution(context)
        except Exception as exc:
            logger.warning(f"Pipeline metrics failed: {exc}")

        # ---------------------------------------------------------
        # 5. Transform to response object
        # ---------------------------------------------------------
        response = PipelineResponse.from_context(context)

        return response
