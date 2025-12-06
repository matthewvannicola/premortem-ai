from pydantic import BaseModel, Field, field_validator
from typing import Optional
from premortem_ai.core.normalize_text import normalize_text


class PipelineRequest(BaseModel):
    """
    Top-level request object for initiating a PreMortem AI analysis.

    Mirrors pipeline_request.schema.json and is consumed by:
      - analysis_service
      - orchestrator
      - preprocessing pipeline
      - API layer (REST or CLI)
    """

    project_description: str = Field(
        ...,
        description="Raw free-form description of the project to analyze. Normalized before pipeline execution.",
        min_length=10,
        max_length=20_000,
    )

    max_risks: Optional[int] = Field(
        50,
        description="Optional limit for maximum risks returned during discovery.",
        ge=1,
        le=500,
    )

    include_metadata: bool = Field(
        True,
        description="Whether to include execution metadata in the final response."
    )

    model_version_override: Optional[str] = Field(
        None,
        description="Optional override specifying the LLM model version to use.",
        min_length=1,
        max_length=100,
    )

    pipeline_version_override: Optional[str] = Field(
        None,
        description="Optional override specifying which pipeline version should execute this request.",
        min_length=1,
        max_length=20,
    )

    # ---------------------------------------------------------
    # Normalize project description deterministically
    # ---------------------------------------------------------
    @field_validator("project_description", mode="before")
    def _normalize_description(cls, v):
        if isinstance(v, str):
            return normalize_text(v)
        return v

    # ---------------------------------------------------------
    # Normalize pipeline_version_override (ensure it begins with 'v')
    # ---------------------------------------------------------
    @field_validator("pipeline_version_override", mode="before")
    def _normalize_pipeline_version(cls, v):
        if v is None:
            return v
        v = v.strip()
        if v and not v.startswith("v"):
            return f"v{v}"
        return v

    # ---------------------------------------------------------
    # Convenience constructors
    # ---------------------------------------------------------
    @classmethod
    def from_api(cls, raw: dict):
        """
        Build a PipelineRequest from API input.

        Useful for:
          - API gateway
          - CLI parser
          - Pipedream/Make.com service hooks

        Automatically:
          - normalizes text
          - validates overrides
        """
        return cls(**raw)

    def to_dict(self):
        """Return JSON-serializable request."""
        return self.model_dump()
