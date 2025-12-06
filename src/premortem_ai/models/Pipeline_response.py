"""
pipeline_response.py

Defines the canonical output model for the PreMortem AI pipeline.

This model is returned by:
    - FastAPI endpoint
    - CLI tool
    - Any internal automation

It is constructed from a PipelineContext produced by run_pipeline().
"""


from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from premortem_ai.models.risk_item import RiskItem
from premortem_ai.models.score_item import ScoreItem
from premortem_ai.models.theme_item import ThemeItem
from premortem_ai.models.mitigation_item import MitigationItem
from premortem_ai.models.summary_item import SummaryItem


class PipelineResponse(BaseModel):
    """
    Structured, validated, API-safe container for all pipeline outputs.
    """

    risks: Dict[str, RiskItem] = Field(
        ..., description="All discovered risks indexed by risk_id."
    )

    scores: Dict[str, ScoreItem] = Field(
        ..., description="Scoring results for each risk."
    )

    themes: List[ThemeItem] = Field(
        ..., description="Clustered thematic groupings of risks."
    )

    mitigations: List[MitigationItem] = Field(
        ..., description="Generated mitigation strategies for each risk."
    )

    summary: SummaryItem = Field(
        ..., description="Executive summary synthesizing the entire analysis output."
    )

    stage_timings: Dict[str, float] = Field(
        default_factory=dict,
        description="Execution time (seconds) for each pipeline stage."
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Original PipelineRequest fields and supplemental metadata."
    )

    # ------------------------------------------------------------------
    # Construction helper
    # ------------------------------------------------------------------

    @classmethod
    def from_context(cls, context) -> "PipelineResponse":
        """
        Convert the PipelineContext produced by run_pipeline() into a
        hardened, API-safe PipelineResponse Pydantic model.

        Args:
            context: PipelineContext object

        Returns:
            PipelineResponse instance
        """

        return cls(
            risks=context.risks,
            scores=context.scores,
            themes=context.themes,
            mitigations=context.mitigations,
            summary=context.summary,
            stage_timings=context.stage_timings,
            metadata=context.request_metadata,
        )
