from typing import List
from pydantic import Field, field_validator

from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.core.id_generation import generate_theme_id
from .base_model import CanonicalModel


class ThemeItem(CanonicalModel):
    """
    Canonical representation of a thematic grouping of related risks.

    Mirrors theme_item.schema.json and is used by:
      - theme_clusterer (domain/themes/theme_clusterer.py)
      - severity aggregation
      - final summary generation
      - mitigation alignment

    Inherits:
      - strict schema enforcement
      - deterministic serialization
      - immutable model behavior
      - model version tagging
    """

    theme_id: str = Field(
        ...,
        description="Stable unique theme identifier (e.g., 'theme-00012').",
        min_length=6,
        max_length=50,
    )

    label: str = Field(
        ...,
        description="Human-readable label describing the systemic theme.",
        min_length=3,
        max_length=300,
    )

    risk_ids: List[str] = Field(
        ...,
        description="List of risk_ids that belong to this theme.",
        min_items=1,
    )

    rationale: str | None = Field(
        None,
        description="Optional explanation of why these risks are grouped together.",
        max_length=2000,
    )

    # ---------------------------------------------------------
    # Normalize text fields for deterministic output
    # ---------------------------------------------------------
    @field_validator("label", "rationale", mode="before")
    def _normalize_text(cls, v):
        if isinstance(v, str):
            return normalize_text(v)
        return v

    # ---------------------------------------------------------
    # Auto-generate theme_id if missing
    # ---------------------------------------------------------
    @field_validator("theme_id", mode="before")
    def _ensure_theme_id(cls, v):
        if v is None or str(v).strip() == "":
            return generate_theme_id()
        return v

    # ---------------------------------------------------------
    # Ensure risk_ids contain no duplicates
    # ---------------------------------------------------------
    @field_validator("risk_ids")
    def _validate_unique_risks(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("risk_ids must be unique within a theme.")
        return v

    # ---------------------------------------------------------
    # Convenience constructors
    # ---------------------------------------------------------
    @classmethod
    def from_llm(cls, raw: dict):
        """
        Build a ThemeItem from an LLM output dict.

        Ensures:
          - auto theme_id assignment
          - text normalization
          - validation of risk_ids list structure
        """
        return cls(**raw)

    def to_dict(self):
        """Return a clean JSON-serializable dict."""
        return self.model_dump()
