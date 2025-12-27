"""
summary.py

Enterprise-grade canonical model representing the executive risk summary.

Enhancements:
    • Stronger validation on top_risks
    • Better narrative + recommendation normalization
    • Defensive construction from LLM output
    • Guaranteed structure alignment for reporting + RiskReport assembly
"""

from typing import List, Optional
from pydantic import Field, field_validator

from premortem_ai.core.normalize_text import normalize_text
from .base_model import CanonicalModel


class Summary(CanonicalModel):
    """
    Executive-level project health summary.

    Used by:
        • Summary generation engine (LLM)
        • RiskReport assembly
        • Dashboard/reporting layers
        • Client-facing API responses

    The summary must be deterministic, human-readable, and structurally safe.
    """

    health_score: int = Field(
        ...,
        description="Overall project health score (0–100). Lower scores indicate higher risk.",
        ge=0,
        le=100,
    )

    top_risks: List[str] = Field(
        ...,
        description="Ordered list of risk_ids contributing most to low health score.",
        min_items=1,
    )

    narrative: str = Field(
        ...,
        description="High-level executive narrative describing project risk posture.",
        min_length=10,
        max_length=20_000,
    )

    recommendations: Optional[List[str]] = Field(
        None,
        description="Optional list of high-level strategic recommendations.",
        min_items=1,
    )

    # ----------------------------------------------------------------------
    # Normalization
    # ----------------------------------------------------------------------
    @field_validator("narrative", mode="before")
    def _normalize_narrative(cls, value):
        if isinstance(value, str):
            return normalize_text(value)
        return value

    @field_validator("recommendations", mode="before")
    def _normalize_recommendations(cls, value):
        if isinstance(value, list):
            return [normalize_text(x) for x in value if isinstance(x, str)]
        return value

    # ----------------------------------------------------------------------
    # Validate top_risks for compatibility with RiskItem
    # ----------------------------------------------------------------------
    @field_validator("top_risks")
    def _validate_top_risks(cls, ids):
        """
        Ensures:
            • no duplicate risks
            • all IDs appear valid (≥ 6 chars)
        """
        if len(ids) != len(set(ids)):
            raise ValueError("top_risks must not contain duplicate risk IDs.")

        for rid in ids:
            if not isinstance(rid, str) or len(rid.strip()) < 6:
                raise ValueError(
                    f"Invalid risk_id '{rid}' — must match RiskItem identifier format."
                )

        return ids

    # ----------------------------------------------------------------------
    # Defensive constructor for LLM output
    # ----------------------------------------------------------------------
    @classmethod
    def from_llm(cls, raw: dict):
        """
        Construct a Summary object from structured LLM output.

        Validates:
            • proper narrative structure
            • valid risk_id formatting
            • deterministic normalization of text fields
            • recommendations list safety
        """
        if not isinstance(raw, dict):
            raise ValueError("Summary.from_llm expected dict-like input.")
        return cls(**raw)

    # ----------------------------------------------------------------------
    # Serialization
    # ----------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Return canonical JSON-ready summary."""
        return self.model_dump()
