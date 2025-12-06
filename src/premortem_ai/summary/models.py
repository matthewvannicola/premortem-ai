"""
models.py

Pydantic models for structured summary output in the PreMortem AI system.

The SummaryItem represents the consolidated executive narrative
produced after risk discovery, scoring, theming, and mitigation generation.
"""

from typing import List
from pydantic import BaseModel, Field
from premortem_ai.core.id_generation import generate_summary_id
from premortem_ai.core.normalize_text import normalize_text


class SummaryItem(BaseModel):
    """
    Canonical executive summary block returned by the pipeline.

    This object is included in PipelineResponse and downstream
    reporting layers (PDF, dashboard, exports).
    """

    summary_id: str = Field(
        default_factory=generate_summary_id,
        description="Stable unique identifier for this summary block.",
    )

    executive_summary: str = Field(
        ...,
        description="High-level narrative overview of project risk posture."
    )

    top_risks_summary: str = Field(
        ...,
        description="Synthesis of the most severe and urgent risks."
    )

    themes_summary: str = Field(
        ...,
        description="Narrative explanation of systemic patterns derived from themes."
    )

    mitigation_overview: str = Field(
        ...,
        description="High-level overview synthesizing mitigation strategy."
    )

    top_risk_ids: List[str] = Field(
        ...,
        description="Ordered list of risk IDs representing the most severe risks."
    )

    # ------------------------------------------------------------------
    # NORMALIZATION HOOKS
    # ------------------------------------------------------------------
    def normalize(self) -> "SummaryItem":
        """
        Apply global normalization rules to all narrative fields.
        Ensures consistent casing, whitespace, unicode normalization,
        and downstream serializable output.
        """
        return SummaryItem(
            summary_id=self.summary_id,
            executive_summary=normalize_text(self.executive_summary),
            top_risks_summary=normalize_text(self.top_risks_summary),
            themes_summary=normalize_text(self.themes_summary),
            mitigation_overview=normalize_text(self.mitigation_overview),
            top_risk_ids=[r.strip() for r in self.top_risk_ids],
        )
