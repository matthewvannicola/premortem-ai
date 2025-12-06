from typing import List, Optional
from pydantic import Field, field_validator

from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.core.id_generation import generate_mitigation_id
from .base_model import CanonicalModel


class MitigationAction(CanonicalModel):
    """
    Represents a single actionable step in a mitigation plan.

    Used for:
      - structured LLM output
      - ordered mitigation formatting
      - deterministic report generation
    """

    step: int = Field(
        ...,
        description="Ordered step number for execution.",
        ge=1,
        le=50,
    )

    action: str = Field(
        ...,
        description="Concrete mitigation action to reduce risk likelihood or impact.",
        min_length=3,
        max_length=2000,
    )

    owner: Optional[str] = Field(
        None,
        description="Optional owner or role responsible (e.g., 'Tech Lead', 'PM', 'Security').",
        max_length=200,
    )

    @field_validator("action", mode="before")
    def _normalize_action(cls, v):
        if isinstance(v, str):
            return normalize_text(v)
        return v


class MitigationItem(CanonicalModel):
    """
    Represents a mitigation package associated with one or more risks.

    Mirrors mitigation_item.schema.json and is used by:
      - mitigation_generator (LLM-driven reasoning)
      - summary/report generation
      - theme alignment

    Inherits:
      - strict schema enforcement
      - deterministic serialization
      - immutable/frozen model behavior
      - version tagging
    """

    mitigation_id: str = Field(
        ...,
        description="Stable unique identifier for this mitigation set (e.g., 'mitigation-00045').",
        min_length=6,
        max_length=50,
    )

    risk_ids: List[str] = Field(
        ...,
        description="List of risk_ids this mitigation applies to.",
        min_items=1,
    )

    actions: List[MitigationAction] = Field(
        ...,
        description="Ordered list of actionable mitigation steps.",
        min_items=1,
    )

    notes: Optional[str] = Field(
        None,
        description="Optional additional context or reasoning.",
        max_length=3000,
    )

    # ---------------------------------------------------------
    # Auto-generate mitigation_id if missing
    # ---------------------------------------------------------
    @field_validator("mitigation_id", mode="before")
    def _ensure_mitigation_id(cls, v):
        if v is None or str(v).strip() == "":
            return generate_mitigation_id()
        return v

    # ---------------------------------------------------------
    # Normalize notes for deterministic output
    # ---------------------------------------------------------
    @field_validator("notes", mode="before")
    def _normalize_notes(cls, v):
        if isinstance(v, str):
            return normalize_text(v)
        return v

    # ---------------------------------------------------------
    # Ensure unique risk_ids
    # ---------------------------------------------------------
    @field_validator("risk_ids")
    def _validate_unique_risks(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("risk_ids must be unique within a mitigation group.")
        return v

    # ---------------------------------------------------------
    # Convenience constructors
    # ---------------------------------------------------------
    @classmethod
    def from_llm(cls, raw: dict):
        """
        Construct a MitigationItem from an LLM output dictionary.
        Ensures:
          - deterministic text normalization
          - auto mitigation_id assignment
          - validation of structured steps
        """
        return cls(**raw)

    def to_dict(self):
        """Return a clean JSON-serializable dict."""
        return self.model_dump()
