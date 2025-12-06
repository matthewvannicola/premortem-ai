"""
risk_item.py

Enterprise-grade canonical model for representing an individual discovered risk.

Enhancements over prior version:
    - Tightened validation rules
    - More defensive construction from LLM output
    - Optional governance hooks (future observability)
    - Unified normalization strategy
    - Strict schema alignment for downstream consumers
"""

from typing import Optional
from pydantic import Field, field_validator

from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.core.id_generation import generate_risk_id
from .base_model import CanonicalModel


class RiskItem(CanonicalModel):
    """
    Canonical representation of a single discovered risk, used across the
    entire PreMortem AI pipeline:

        • discovery extractor (LLM output)
        • scoring engine
        • theme clustering
        • mitigation generation
        • executive summary assembly

    All instances are immutable, JSON-deterministic, and schema-aligned.
    """

    risk_id: str = Field(
        ...,
        description="Stable unique identifier (e.g., 'risk-00042'). Auto-generated if missing.",
        min_length=6,
        max_length=50,
    )

    title: str = Field(
        ...,
        description="Concise statement describing the core risk.",
        min_length=3,
        max_length=300,
    )

    description: str = Field(
        ...,
        description="Detailed explanation of why this risk exists and how it may occur.",
        min_length=10,
        max_length=5000,
    )

    category: Optional[str] = Field(
        None,
        description="Optional classification (e.g., 'Security', 'Delivery', 'Operational').",
        max_length=100,
    )

    # ----------------------------------------------------------------------
    # Normalization
    # ----------------------------------------------------------------------
    @field_validator("title", "description", mode="before")
    def _normalize_text(cls, value: str):
        if isinstance(value, str):
            return normalize_text(value)
        return value

    @field_validator("category", mode="before")
    def _normalize_category(cls, value: Optional[str]):
        if isinstance(value, str):
            clean = normalize_text(value)
            return clean if clean else None
        return value

    # ----------------------------------------------------------------------
    # risk_id generation
    # ----------------------------------------------------------------------
    @field_validator("risk_id", mode="before")
    def _ensure_risk_id(cls, value):
        """
        If no ID is provided, generate one deterministically.
        """
        if value is None or str(value).strip() == "":
            return generate_risk_id()
        return str(value).strip()

    # ----------------------------------------------------------------------
    # Structural validation
    # ----------------------------------------------------------------------
    @field_validator("title")
    def _validate_title(cls, value):
        """
        Ensures the risk title is meaningful—single-word titles offer low clarity.
        """
        if len(value.split()) < 2:
            raise ValueError("Risk title must contain at least two words.")
        return value

    @field_validator("description")
    def _validate_description(cls, value):
        """
        Ensures the description is sufficiently detailed.
        """
        if len(value.split()) < 5:
            raise ValueError("Description must be more than a short phrase.")
        return value

    # ----------------------------------------------------------------------
    # Factory constructors
    # ----------------------------------------------------------------------
    @classmethod
    def from_llm(cls, raw: dict):
        """
        Construct a RiskItem from structured LLM JSON.

        This method:
            • normalizes text fields
            • fills missing risk_id
            • enforces strict validation
            • rejects malformed LLM outputs gracefully
        """
        if not isinstance(raw, dict):
            raise ValueError("RiskItem.from_llm expected a dict-like object.")

        return cls(**raw)

    # ----------------------------------------------------------------------
    # Serialization
    # ----------------------------------------------------------------------
    def to_dict(self) -> dict:
        """
        Return canonical, JSON-serializable output—guaranteed deterministic.
        """
        return self.model_dump()
