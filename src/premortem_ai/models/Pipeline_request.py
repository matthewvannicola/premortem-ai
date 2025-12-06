"""
pipeline_request.py

Enterprise-grade canonical request model for initiating a PreMortem AI analysis.

Enhancements:
    • Stronger normalization for project description
    • Overall schema hardening
    • Strict model_version_override and pipeline_version_override sanitation
    • Governance alignment with model_router
    • Defensive LLM/API ingestion support
    • Better documentation and future-extensibility
"""

from typing import Optional
from pydantic import Field, field_validator

from premortem_ai.core.normalize_text import normalize_text
from .base_model import CanonicalModel


class PipelineRequest(CanonicalModel):
    """
    Top-level validated request object for triggering a PreMortem AI analysis.

    Consumed by:
        • analysis_service
        • orchestrator
        • preprocessing pipeline
        • REST API layer
        • CLI entrypoints
        • serverless automation platforms (Pipedream, Make.com)

    This model acts as the FIRST LINE OF DEFENSE:
        - It blocks malformed input
        - Normalizes noisy user text
        - Ensures override formats are consistent
        - Ensures downstream components receive validated, deterministic data
    """

    project_description: str = Field(
        ...,
        description="Raw free-form project description. Automatically normalized.",
        min_length=10,
        max_length=20_000,
    )

    max_risks: Optional[int] = Field(
        50,
        description="Maximum number of risks to return from discovery.",
        ge=1,
        le=500,
    )

    include_metadata: bool = Field(
        True,
        description="If True, include execution metadata in the PipelineResponse.",
    )

    model_version_override: Optional[str] = Field(
        None,
        description="Optional override for which LLM model to use.",
        min_length=1,
        max_length=100,
    )

    pipeline_version_override: Optional[str] = Field(
        None,
        description="Optional override specifying which pipeline version to execute.",
        min_length=1,
        max_length=30,
    )

    # ----------------------------------------------------------------------
    # Normalization: project description
    # ----------------------------------------------------------------------
    @field_validator("project_description", mode="before")
    def _normalize_description(cls, value):
        if isinstance(value, str):
            return normalize_text(value)
        return value

    # ----------------------------------------------------------------------
    # Normalize pipeline version override
    # Enforce prefixing with "v" for consistency (`v1`, `v2-beta`, etc.)
    # ----------------------------------------------------------------------
    @field_validator("pipeline_version_override", mode="before")
    def _normalize_pipeline_version(cls, value):
        if value is None:
            return None
        clean = value.strip()
        if clean and not clean.startswith("v"):
            return f"v{clean}"
        return clean

    # ----------------------------------------------------------------------
    # Normalize model version override
    # (model_router will perform final validation)
    # ----------------------------------------------------------------------
    @field_validator("model_version_override", mode="before")
    def _normalize_model_override(cls, value):
        if value is None:
            return None
        clean = value.strip()
        return clean if clean else None

    # ----------------------------------------------------------------------
    # Convenience factory for API gateways
    # ----------------------------------------------------------------------
    @classmethod
    def from_api(cls, raw: dict):
        """
        Build a PipelineRequest from raw user/API input.

        Guarantees:
            • deterministic normalization
            • safe override enforcement
            • schema validation before orchestrator execution
        """
        if not isinstance(raw, dict):
            raise ValueError("PipelineRequest.from_api expected dict-like input.")
        return cls(**raw)

    # ----------------------------------------------------------------------
    # Serialization
    # ----------------------------------------------------------------------
    def to_dict(self):
        """Return deterministic JSON-safe representation."""
        return self.model_dump()
