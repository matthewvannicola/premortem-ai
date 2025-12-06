from typing import List
from pydantic import Field, field_validator

from premortem_ai.models.risk_item import RiskItem
from premortem_ai.models.score_item import ScoreItem
from premortem_ai.models.theme_item import ThemeItem
from premortem_ai.models.mitigation_item import MitigationItem
from premortem_ai.models.summary import Summary
from premortem_ai.models.metadata import Metadata

from .base_model import CanonicalModel


class RiskReport(CanonicalModel):
    """
    Canonical top-level aggregate for the full PreMortem AI analysis output.

    Mirrors risk_report.schema.json and is used by:
      - orchestrator (final pipeline result)
      - pipeline_response model
      - PDF/Docs/Notion report generation
      - dashboards + analytics
      - regression + invariant validation

    Inherits:
      - strict schema enforcement
      - deterministic serialization
      - immutable model behavior
      - version tagging
    """

    risks: List[RiskItem] = Field(
        ...,
        description="List of all discovered RiskItem objects.",
        min_items=1
    )

    scores: List[ScoreItem] = Field(
        ...,
        description="List of ScoreItem objects, one per risk.",
        min_items=1
    )

    themes: List[ThemeItem] = Field(
        ...,
        description="List of thematic clusters derived from risks.",
        min_items=0
    )

    mitigations: List[MitigationItem] = Field(
        ...,
        description="List of mitigation sets aligned to risks and themes.",
        min_items=0
    )

    summary: Summary = Field(
        ...,
        description="Executive project health summary."
    )

    metadata: Metadata = Field(
        ...,
        description="Execution metadata describing model, pipeline, runtime."
    )

    # ---------------------------------------------------------
    # Cross-reference validation
    # ---------------------------------------------------------
    @field_validator("scores")
    def _validate_scores_reference_known_risks(cls, scores, info):
        if "risks" not in info.data:
            return scores

        known_ids = {r.risk_id for r in info.data["risks"]}

        for score in scores:
            if score.risk_id not in known_ids:
                raise ValueError(
                    f"ScoreItem references unknown risk_id: {score.risk_id}"
                )
        return scores

    @field_validator("themes")
    def _validate_themes_reference_known_risks(cls, themes, info):
        if "risks" not in info.data:
            return themes

        known_ids = {r.risk_id for r in info.data["risks"]}

        for theme in themes:
            for rid in theme.risk_ids:
                if rid not in known_ids:
                    raise ValueError(
                        f"ThemeItem references unknown risk_id: {rid}"
                    )
        return themes

    @field_validator("mitigations")
    def _validate_mitigations_reference_known_risks(cls, mitigations, info):
        if "risks" not in info.data:
            return mitigations

        known_ids = {r.risk_id for r in info.data["risks"]}

        for mit in mitigations:
            for rid in mit.risk_ids:
                if rid not in known_ids:
                    raise ValueError(
                        f"MitigationItem references unknown risk_id: {rid}"
                    )
        return mitigations

    # ---------------------------------------------------------
    # Convenience helper
    # ---------------------------------------------------------
    @classmethod
    def from_components(
        cls,
        risks: List[RiskItem],
        scores: List[ScoreItem],
        themes: List[ThemeItem],
        mitigations: List[MitigationItem],
        summary: Summary,
        metadata: Metadata,
    ):
        """
        Clean, safe aggregate builder used by orchestrator.

        Ensures:
          - all ID references are validated
          - deterministic serialization
          - schema alignment
        """
        return cls(
            risks=risks,
            scores=scores,
            themes=themes,
            mitigations=mitigations,
            summary=summary,
            metadata=metadata,
        )

    def to_dict(self):
        """Return JSON-serializable shape aligned with risk_report.schema.json."""
        return self.model_dump()
