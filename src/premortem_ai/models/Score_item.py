from pydantic import Field, field_validator
from premortem_ai.core.normalize_text import normalize_text

from .base_model import CanonicalModel


class ScoreItem(CanonicalModel):
    """
    Canonical probability/impact/severity scoring structure.

    Mirrors scoring_item.schema.json and is used by:
      - scoring.severity_engine
      - scoring.aggregator
      - theme clustering (for weighted grouping)
      - final RiskReport assembly

    Inherits:
      - strict schema enforcement
      - deterministic serialization
      - immutable model behavior
      - version tagging
    """

    risk_id: str = Field(
        ...,
        description="Foreign key linking this score entry to a RiskItem.",
        min_length=6,
        max_length=50,
    )

    likelihood: int = Field(
        ...,
        description="Estimated probability (1–5) that this risk will occur.",
        ge=1,
        le=5,
    )

    impact: int = Field(
        ...,
        description="Estimated impact severity (1–5) if this risk does occur.",
        ge=1,
        le=5,
    )

    severity: int = Field(
        ...,
        description="Composite score (likelihood × impact), range 1–25.",
        ge=1,
        le=25,
    )

    rationale: str | None = Field(
        None,
        description="Optional explanation of how the scoring was derived.",
        max_length=2000,
    )

    # ---------------------------------------------------------
    # Normalize rationale for deterministic output
    # ---------------------------------------------------------
    @field_validator("rationale", mode="before")
    def _normalize_rationale(cls, v):
        if isinstance(v, str):
            return normalize_text(v)
        return v

    # ---------------------------------------------------------
    # Validate severity = likelihood × impact
    # ---------------------------------------------------------
    @field_validator("severity")
    def _validate_severity(cls, severity_value, info):
        likelihood = info.data.get("likelihood")
        impact = info.data.get("impact")

        if likelihood and impact:
            expected = likelihood * impact
            if severity_value != expected:
                raise ValueError(
                    f"Severity must equal likelihood × impact ({likelihood} × {impact} = {expected}). "
                    f"Received: {severity_value}"
                )
        return severity_value

    # ---------------------------------------------------------
    # Convenience constructors
    # ---------------------------------------------------------
    @classmethod
    def from_llm(cls, raw: dict):
        """
        Construct a ScoreItem directly from an LLM output dictionary.
        Ensures:
          - normalization
          - severity consistency validation
        """
        return cls(**raw)

    def to_dict(self):
        """Return clean JSON-serializable dict."""
        return self.model_dump()
