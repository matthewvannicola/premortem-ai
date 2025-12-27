"""
risk_report.py

Enterprise-grade canonical model representing the full output of the PreMortem AI pipeline.

A RiskReport unifies:
    • RiskItem list
    • ScoreItem list
    • ThemeItem list
    • MitigationItem list
    • Summary
    • Metadata

This model enforces global consistency and prevents schema drift.
"""

from typing import List
from pydantic import Field, field_validator

from .base_model import CanonicalModel
from .risk_item import RiskItem
from .score_item import ScoreItem
from .theme_item import ThemeItem
from .mitigation_item import MitigationItem
from .summary import Summary
from .metadata import Metadata


class RiskReport(CanonicalModel):
    """
    Unified, validated representation of all results produced by the pipeline.

    This is the primary payload consumed by:
        • PipelineResponse
        • Reporting engine (PDF, dashboards)
        • External APIs
        • Clients + integrations

    MUST remain stable, deterministic, and schema-aligned.
    """

    risks: List[RiskItem] = Field(..., min_items=1)
    scores: List[ScoreItem] = Field(..., min_items=1)
    themes: List[ThemeItem] = Field(..., min_items=0)
    mitigations: List[MitigationItem] = Field(..., min_items=0)
    summary: Summary = Field(...)
    metadata: Metadata = Field(...)

    # ----------------------------------------------------------------------
    # Global Consistency Validators
    # ----------------------------------------------------------------------

    @field_validator("scores")
    def _validate_scores_link_risks(cls, scores, info):
        """
        Ensures all ScoreItems reference valid RiskItem IDs.
        """
        valid_risks = {r.risk_id for r in info.data.get("risks", [])}

        for score in scores:
            if score.risk_id not in valid_risks:
                raise ValueError(
                    f"ScoreItem references unknown risk_id '{score.risk_id}'."
                )
        return scores

    @field_validator("themes")
    def _validate_themes_link_risks(cls, themes, info):
        """
        Ensures every ThemeItem references valid RiskItem IDs.
        """
        valid_risks = {r.risk_id for r in info.data.get("risks", [])}

        for theme in themes:
            for rid in theme.risk_ids:
                if rid not in valid_risks:
                    raise ValueError(
                        f"ThemeItem references unknown risk_id '{rid}'."
                    )
        return themes

    @field_validator("mitigations")
    def _validate_mitigations_link_risks(cls, mitigations, info):
        """
        Ensures every MitigationItem references valid RiskItem IDs.
        """
        valid_risks = {r.risk_id for r in info.data.get("risks", [])}

        for m in mitigations:
            for rid in m.risk_ids:
                if rid not in valid_risks:
                    raise ValueError(
                        f"MitigationItem references unknown risk_id '{rid}'."
                    )
        return mitigations

    @field_validator("summary")
    def _validate_summary_top_risks(cls, summary, info):
        """
        Ensures summary.top_risks correspond to real RiskItems.
        """
        valid_risks = {r.risk_id for r in info.data.get("risks", [])}

        for rid in summary.top_risks:
            if rid not in valid_risks:
                raise ValueError(
                    f"Summary references unknown risk_id '{rid}'."
                )

        return summary
