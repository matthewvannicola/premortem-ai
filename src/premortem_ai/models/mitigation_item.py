"""
mitigation_item.py

Enterprise-grade canonical models representing mitigation steps and mitigation groups.

Enhancements:
    • Stronger validation for step ordering
    • Stricter risk_id enforcement for compatibility with RiskItem
    • Better text normalization for all free-form text
    • Hardened mitigation_id auto-generation
    • Defensive LLM ingestion with structure guarantees
"""

from typing import List, Optional
from pydantic import Field, field_validator

from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.core.id_generation import generate_mitigation_id
from .base_model import CanonicalModel


# ----------------------------------------------------------------------
# Submodel: A single mitigation action/step
# ----------------------------------------------------------------------

class MitigationAction(CanonicalModel):
    """
    Represents one actionable mitigation step.

    Used by:
        • mitigation generator (LLM inference)
        • report assembly
        • compliance/operations tooling downstream
    """

    step: int = Field(
        ...,
        description="Ordered step number (must be >=1 and sequential in the pipeline).",
        ge=1,
        le=999,
    )

    action: str = Field(
        ...,
        description="Concrete mitigation action to reduce risk likelihood or impact.",
        min_length=3,
        max_length=3000,
    )

    owner: Optional[str] = Field(
        None,
        description="Optional owner or responsible role (e.g., 'Security Lead', 'PM').",
        max_length=200,
    )

    # ------------------------------------------------------
    # Normalization
    # ------------------------------------------------------
    @field_validator("action", "owner", mode="before")
    def _normalize_text(cls, value):
        if isinstance(value, str):
            clean = normalize_text(value)
            return clean if clean else None
        return value


# ----------------------------------------------------------------------
# The full mitigation item
# ----------------------------------------------------------------------

class MitigationItem(CanonicalModel):
    """
    Represents a complete mitigation package tied to one or more risks.

    Used for:
        • mitigation generation (LLM)
        • theme alignment
        • summary + risk report assembly
    """

    mitigation_id: str = Field(
        ...,
        description="Stable unique identifier for a mitigation group "
                    "(e.g., 'mitigation-00042').",
        min_length=6,
        max_length=50,
    )

    risk_ids: List[str] = Field(
        ...,
        description="List of RiskItem IDs this mitigation addresses.",
        min_items=1,
    )

    actions: List[MitigationAction] = Field(
        ...,
        description="Ordered list of actionable mitigation steps.",
        min_items=1,
    )

    notes: Optional[str] = Field(
        None,
        description="Optional additional context or reasoning behind the mitigation set.",
        max_length=5000,
    )

    # ------------------------------------------------------
    # Auto-ID generation
    # ------------------------------------------------------
    @field_validator("mitigation_id", mode="before")
    def _ensure_mitigation_id(cls, value):
        if value is None or str(value).strip() == "":
            return generate_mitigation_id()
        return str(value).strip()

    # ------------------------------------------------------
    # Validate risk_ids
    # ------------------------------------------------------
    @field_validator("risk_ids")
    def _validate_risk_ids(cls, ids):
        """
        Ensures:
            • IDs are non-empty, valid RiskItem identifiers
            • No duplicates
        """
        if len(ids) != len(set(ids)):
            raise ValueError("risk_ids must be unique within a mitigation group.")

        for rid in ids:
            if not isinstance(rid, str) or len(rid.strip()) < 6:
                raise ValueError(
                    f"Invalid risk_id '{rid}' — must match RiskItem identifier format."
                )

        return ids

    # ------------------------------------------------------
    # Validate step ordering
    # ------------------------------------------------------
    @field_validator("actions")
    def _validate_sequential_steps(cls, actions):
        """
        Ensures mitigation steps are sequential (1..N).
        """
        steps = [a.step for a in actions]
        expected = list(range(1, len(actions) + 1))

        if steps != expected:
            raise ValueError(
                f"Mitigation steps must be sequential starting at 1. "
                f"Expected: {expected}, received: {steps}"
            )

        return actions

    # ------------------------------------------------------
    # Normalize notes
    # ------------------------------------------------------
    @field_validator("notes", mode="before")
    def _normalize_notes(cls, value):
        if isinstance(value, str):
            return normalize_text(value)
        return value

    # ------------------------------------------------------
    # LLM ingestion helper
    # ------------------------------------------------------
    @classmethod
    def from_llm(cls, raw: dict):
        """
        Construct a fully validated MitigationItem from structured LLM output.

        Validates:
            • mitigation_id assignment
            • sequential, valid steps
            • risk_id structure
            • normalized text fields
        """
        if not isinstance(raw, dict):
            raise ValueError("MitigationItem.from_llm expected a dict-like input.")
        return cls(**raw)

    # ------------------------------------------------------
    # Serialization
    # ------------------------------------------------------
    def to_dict(self) -> dict:
        """Return deterministic JSON-ready structure."""
        return self.model_dump()
