"""
pipeline_request.py

Enterprise-grade canonical request model for initiating a PreMortem AI analysis.
"""

from typing import Optional

from pydantic import Field, field_validator

from premortem_ai.core.normalize_text import normalize_text
from premortem_ai.output.base import OutputFormat
from .base_model import CanonicalModel


class PipelineRequest(CanonicalModel):
    """
    Top-level validated request object for triggering a PreMortem AI analysis.
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

    output_format: OutputFormat = Field(
        OutputFormat.JSON,
        description="Desired output format for the final report.",
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

    
    # --------------------------------------------------
    # Validators
    # --------------------------------------------------

    @field_validator("project_description", mode="before")
    def _normalize_description(cls, value):
        if isinstance(value, str):
            return normalize_text(value)
        return value

    @field_validator("pipeline_version_override", mode="before")
    def _normalize_pipeline_version(cls, value):
        if value is None:
            return None
        clean = value.strip()
        if clean and not clean.startswith("v"):
            return f"v{clean}"
        return clean

    @field_validator("model_version_override", mode="before")
    def _normalize_model_override(cls, value):
        if value is None:
            return None
        clean = value.strip()
        return clean if clean else None

