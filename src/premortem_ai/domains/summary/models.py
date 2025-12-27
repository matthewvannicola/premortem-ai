"""
models.py

Pydantic data models for summary-level reporting outputs.

The SummaryItem model is the canonical representation of the final
executive-layer output produced by the summary_generator. This is the
primary data structure used for:
    - PDF/HTML report generation
    - API responses
    - Dashboard visualizations
    - PipelineResponse assembly

The model enforces strict typing, normalization, and ordered risk
references to ensure deterministic downstream processing.
"""

from typing import List
from uuid import uuid4
from pydantic import BaseModel, field_validator


class SummaryItem(BaseModel):
    """
    SummaryItem represents the final structured summary produced by the
    LLM after ingesting risks, themes, and mitigations. It captures the
    narrative and the ranked "top risks" list.
    """

    summary_id: str = None
    executive_summary: str
    top_risks_summary: str
    themes_summary: str
    mitigation_overview: str
    top_risk_ids: List[str]

    # ------------------------------------------------------------
    # Validators & Normalizers
    # ------------------------------------------------------------

    @field_validator("summary_id", mode="before")
    def assign_uuid(cls, v):
        """Assign UUID if not explicitly provided."""
        return v or f"summary-{uuid4().hex}"

    @field_validator(
        "executive_summary",
        "top_risks_summary",
        "themes_summary",
        "mitigation_overview",
        mode="before",
    )
    def clean_text_fields(cls, v):
        """Ensure narratives are normalized as strings."""
        if v is None:
            return ""
        return str(v).strip()

    @field_validator("top_risk_ids")
    def ensure_non_empty_list(cls, v):
        """Ensure at least one top risk ID is present."""
        if not v or not isinstance(v, list):
            raise ValueError("top_risk_ids must contain at least one risk ID.")
        return [str(x).strip() for x in v if str(x).strip()]

    # ------------------------------------------------------------
    # Utility Methods
    # ------------------------------------------------------------

    def normalize(self) -> "SummaryItem":
        """
        Optional hook to perform higher-level normalization on fields.
        This is extended by the summary_generator after LLM output.
        """
        cleaned_exec = self.executive_summary.strip()
        cleaned_top = self.top_risks_summary.strip()
        cleaned_themes = self.themes_summary.strip()
        cleaned_mit = self.mitigation_overview.strip()

        return SummaryItem(
            summary_id=self.summary_id,
            executive_summary=cleaned_exec,
            top_risks_summary=cleaned_top,
            themes_summary=cleaned_themes,
            mitigation_overview=cleaned_mit,
            top_risk_ids=self.top_risk_ids,
        )

    class Config:
        validate_assignment = True
        extra = "forbid"
        frozen = False
