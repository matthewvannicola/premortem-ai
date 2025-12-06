from typing import Optional
from pydantic import Field, field_validator

from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.core.id_generation import generate_risk_id
from .base_model import CanonicalModel


class RiskItem(CanonicalModel):
    """
    Canonical representation of a single discovered risk.

    Mirrors JSON Schema:
      - risk_item.schema.json

    Used across:
      - discovery extractor
      - scoring pipeline
      - theme clustering
      - mitigation generation
      - final RiskReport assembly

    Inherits:
      - strict validation
      - deterministic serialization
      - immutability (frozen model)
      - version tagging
    """

    risk_id: str = Field(
        ...,
        description="Stable unique identifier for this risk (e.g., 'risk-00042').",
        min_length=6,
        max_length=50,
    )

    title: str = Field(
        ...,
        description="A concise statement describing the core risk.",
        min_length=3,
        max_length=300,
    )

    description: str = Field(
        ...,
        description="Detailed explanation of why this risk exists and when it may occur.",
        min_length=5,
        max_length=5000,
    )

    category: Optional[str] = Field(
        None,
        description="Optional categorical grouping (e.g., 'Security', 'Delivery', 'Operational').",
        max_length=100,
    )

    # ---------------------------------------------------------
    # Text normalization for deterministic behavior
    # ---------------------------------------------------------
    @field_validator("title", "description", mode="before")
    def _normalize_text(cls, v):
        if isinstance(v, str):
            return normalize_text(v)
        return v

    # ---------------------------------------------------------
    # risk_id auto-generation if missing
    # ---------------------------------------------------------
    @field_validator("risk_id", mode="before")
    def _ensure_risk_id(cls, v):
        if v is None or str(v).strip() == "":
            return generate_risk_id()
        return v

    # ---------------------------------------------------------
    # Sanity validator to ensure risk structure is sensible
    # ---------------------------------------------------------
    @field_validator("title")
    def _validate_title(cls, v):
        if len(v.split()) < 2:
            raise ValueError("Risk title must contain at least two words.")
        return v

    # ---------------------------------------------------------
    # Convenience constructors
    # ---------------------------------------------------------
    @classmethod
    def from_llm(cls, raw: dict):
        """
        Construct a RiskItem from an LLM output dictionary.
        Ensures:
          - missing fields handled
          - normalization applied
          - auto risk_id assignment
        """
        return cls(**raw)

    def to_dict(self):
        """Return clean JSON-serializable dict."""
        return self.model_dump()
