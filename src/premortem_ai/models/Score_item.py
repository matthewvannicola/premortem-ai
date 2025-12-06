"""
score_item.py

Enterprise-grade canonical scoring model for PreMortem AI.

Used across:
    - scoring severity engine
    - scoring aggregator
    - theme clustering
    - executive reporting

This rewrite adds:
    • Stronger validation logic
    • Guaranteed consistency between likelihood/impact/severity
    • Normalized rationale text
    • Defensive LLM ingestion
    • Compatibility with rewritten RiskItem IDs
"""

from pydantic import Field, field_validator
from premortem_ai.core.normalize_text import normalize_text
from .base_model import CanonicalModel


class ScoreItem(CanonicalModel):
    """
    Canonical probability/impact/severity scoring representation.

    All fields follow strict validation rules to ensure:
        - consistency across LLM outputs
        - deterministic behavior in reports
        - clean integration with theme and summary layers
    """

    risk_id: str = Field(
        ...,
        description="Foreign key linking this score entry to a RiskItem (e.g., 'risk-00123').",
        min_length=6,
        max_length=50,
    )

    likelihood: int = Field(
        ...,
        description="Probability the risk occurs (1–5).",
        ge=1,
        le=5,
    )

    impact: int = Field(
        ...,
        description="Impact severity if risk occurs (1–5).",
        ge=1,
        le=5,
    )

    severity: int = Field(
        ...,
        description="Composite score likelihood × impact (1–25).",
        ge=1,
        le=25,
    )

    rationale: str | None = Field(
        None,
        description="Optional explanation of how the score was derived.",
        max_length=5000,
    )

    # ----------------------------------------------------------------------
    # Normalization
    # ----------------------------------------------------------------------
    @field_validator("rationale", mode="before")
    def _normalize_rationale(cls, value):
        if isinstance(value, str):
            return normalize_text(value)
        return value

    # ----------------------------------------------------------------------
    # Severity validation
    # ----------------------------------------------------------------------
    @field_validator("severity")
    def _validate_severity(cls, severity_value, info):
        """
        Ensures that severity = likelihood × impact.
        """
        likelihood = info.data.get("likelihood")
        impact = info.data.get("impact")

        if likelihood is not None and impact is not None:
            expected = likelihood * impact
            if severity_value != expected:
                raise ValueError(
                    f"Severity must equal likelihood × impact "
                    f"({likelihood} × {impact} = {expected}). Received: {severity_value}"
                )
        return severity_value

    # ----------------------------------------------------------------------
    # Defensive risk_id validation
    # ----------------------------------------------------------------------
    @field_validator("risk_id")
    def _validate_risk_id_format(cls, v):
        """
        Ensures risk_id is non-empty and well-formed.
        Compatible with rewritten RiskItem.
        """
        if not isinstance(v, str) or len(v.strip()) < 6:
            raise ValueError("risk_id must be a valid RiskItem identifier.")
        return v.strip()

    # ----------------------------------------------------------------------
    # Constructors
    # ----------------------------------------------------------------------
    @classmethod
    def from_llm(cls, raw: dict):
        """
        Consumes structured LLM JSON and returns a validated ScoreItem.

        Automatically validates:
            • score consistency
            • ID format
            • rationale normalization
        """
        if not isinstance(raw, dict):
            raise ValueError("ScoreItem.from_llm expected a dict.")

        return cls(**raw)

    # ----------------------------------------------------------------------
    # Serialization
    # ----------------------------------------------------------------------
    def to_dict(self):
        """Return deterministic JSON-serializable dict."""
        return self.model_dump()
