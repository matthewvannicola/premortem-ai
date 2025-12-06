from typing import List
from pydantic import Field, field_validator

from premortem_ai.core.normalize_text import normalize_text
from .base_model import CanonicalModel


class Summary(CanonicalModel):
    """
    Executive-level project health summary.

    Mirrors summary.schema.json and is used by:
      - summary generation module
      - risk_report assembly
      - dashboard or reporting layers

    Inherits:
      - strict schema validation
      - deterministic serialization
      - immutable model behavior
      - version tagging
    """

    health_score: int = Field(
        ...,
        description="Overall project health score (0–100). Lower scores indicate higher risk.",
        ge=0,
        le=100,
    )

    top_risks: List[str] = Field(
        ...,
        description="Ordered list of the top risk_ids contributing most to poor project health.",
        min_items=1,
    )

    narrative: str = Field(
        ...,
        description="Human-readable executive narrative summarizing the risk posture.",
        min_length=5,
        max_length=10000,
    )

    recommendations: List[str] | None = Field(
        None,
        description="Optional high-level recommendations summarizing strategic actions.",
        min_items=1,
    )

    # ---------------------------------------------------------
    # Normalize narrative + recommendations
    # ---------------------------------------------------------
    @field_validator("narrative", mode="before")
    def _normalize_narrative(cls, v):
        if isinstance(v, str):
            return normalize_text(v)
        return v

    @field_validator("recommendations", mode="before")
    def _normalize_recommendations(cls, v):
        if isinstance(v, list):
            return [normalize_text(x) for x in v if isinstance(x, str)]
        return v

    # ---------------------------------------------------------
    # Validate top_risks contain no duplicates
    # ---------------------------------------------------------
    @field_validator("top_risks")
    def _validate_unique_top_risks(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("top_risks must not contain duplicate risk_ids.")
        return v

    # ---------------------------------------------------------
    # Convenience constructors
    # ---------------------------------------------------------
    @classmethod
    def from_llm(cls, raw: dict):
        """
        Create a Summary object directly from LLM output.

        Ensures:
          - deterministic formatting
          - safety validation
          - normalization of narrative & recommendations
        """
        return cls(**raw)

    def to_dict(self):
        """Return canonical JSON-serializable summary."""
        return self.model_dump()
