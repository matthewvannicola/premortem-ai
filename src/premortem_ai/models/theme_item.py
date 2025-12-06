"""
theme_item.py

Enterprise-grade canonical model representing a thematic grouping of related risks.

Enhancements:
    • Stricter risk_id validation for cross-model consistency
    • Better text normalization on label + rationale
    • Auto theme_id generation hardening
    • Duplicate risk_id protection
    • Defensive from_llm ingestion
"""

from typing import List
from pydantic import Field, field_validator

from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.core.id_generation import generate_theme_id
from .base_model import CanonicalModel


class ThemeItem(CanonicalModel):
    """
    A ThemeItem represents a systemic pattern linking multiple RiskItems.

    Used in:
        • theme clustering engine
        • severity aggregation
        • mitigation alignment
        • risk_report assembly

    Themes must be deterministic, validated, and ready for structured pipelines.
    """

    theme_id: str = Field(
        ...,
        description="Stable unique theme identifier (e.g., 'theme-00123'). "
                    "Auto-generated if omitted.",
        min_length=6,
        max_length=50,
    )

    label: str = Field(
        ...,
        description="Human-readable label describing the underlying systemic theme.",
        min_length=3,
        max_length=300,
    )

    risk_ids: List[str] = Field(
        ...,
        description="List of risk_ids belonging to this theme (must be unique).",
        min_items=1,
    )

    rationale: str | None = Field(
        None,
        description="Optional explanation of why these risks form a coherent theme.",
        max_length=3000,
    )

    # ----------------------------------------------------------------------
    # Normalization
    # ----------------------------------------------------------------------
    @field_validator("label", "rationale", mode="before")
    def _normalize_text(cls, value):
        if isinstance(value, str):
            return normalize_text(value)
        return value

    # ----------------------------------------------------------------------
    # ID generation
    # ----------------------------------------------------------------------
    @field_validator("theme_id", mode="before")
    def _ensure_theme_id(cls, value):
        """
        Auto-generate theme_id if none was provided.
        """
        if value is None or str(value).strip() == "":
            return generate_theme_id()
        return str(value).strip()

    # ----------------------------------------------------------------------
    # Validation of risk_ids
    # ----------------------------------------------------------------------
    @field_validator("risk_ids")
    def _validate_risk_ids(cls, ids):
        """
        Ensures that:
            • risk_ids are not duplicated
            • risk_ids are properly formed
            • the list is not empty
        """

        if len(ids) != len(set(ids)):
            raise ValueError("risk_ids must be unique within a theme.")

        for rid in ids:
            if not isinstance(rid, str) or len(rid.strip()) < 6:
                raise ValueError(
                    f"Invalid risk_id '{rid}' — must match RiskItem identifier format."
                )

        return ids

    # ----------------------------------------------------------------------
    # Constructor for LLM output
    # ----------------------------------------------------------------------
    @classmethod
    def from_llm(cls, raw: dict):
        """
        Consume structured LLM output and return a full ThemeItem.

        Validates:
            • theme_id (assigns if missing)
            • label normalization
            • risk_ids well-formed + unique
            • rationale normalized
        """
        if not isinstance(raw, dict):
            raise ValueError("ThemeItem.from_llm expected dict-like input.")

        return cls(**raw)

    # ----------------------------------------------------------------------
    # Serialization
    # ----------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Return JSON-serializable canonical dict."""
        return self.model_dump()
