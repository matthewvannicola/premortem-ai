from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class Metadata(BaseModel):
    """
    Execution-level metadata describing pipeline runtime context.
    
    Mirrors metadata.schema.json and is used by:
      - orchestrator (pipeline runs)
      - summary + report generation
      - audit logs / reproducibility features
      - model/version analytics
    """

    timestamp_utc: str = Field(
        ...,
        description="UTC timestamp of pipeline execution in ISO-8601 format (YYYY-MM-DDTHH:MM:SSZ).",
        min_length=20,
        max_length=25,
    )

    pipeline_version: str = Field(
        ...,
        description="Semantic version of the pipeline used for this analysis (e.g., '1.2.0' or 'v1.2.0').",
        min_length=3,
        max_length=20,
    )

    model_version: str = Field(
        ...,
        description="Identifier of the LLM model used during this execution.",
        min_length=1,
        max_length=100,
    )

    execution_time_ms: int = Field(
        ...,
        description="Total execution time of the pipeline in milliseconds.",
        ge=0,
        le=600_000,  # 10 minutes max
    )

    determinism_fingerprint: Optional[str] = Field(
        None,
        description="Optional reproducibility fingerprint capturing normalized inputs, model, pipeline settings.",
        max_length=200,
    )

    # ---------------------------------------------------------
    # Validate and normalize timestamp
    # ---------------------------------------------------------
    @field_validator("timestamp_utc", mode="before")
    def _validate_timestamp_format(cls, v):
        if isinstance(v, str):
            try:
                # Must match YYYY-MM-DDTHH:MM:SSZ exactly
                datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                raise ValueError(
                    "timestamp_utc must be ISO-8601 UTC format: YYYY-MM-DDTHH:MM:SSZ"
                )
        else:
            raise ValueError("timestamp_utc must be a string.")
        return v

    # ---------------------------------------------------------
    # Normalize pipeline_version to always include leading 'v'
    # ---------------------------------------------------------
    @field_validator("pipeline_version", mode="before")
    def _normalize_pipeline_version(cls, v):
        if isinstance(v, str):
            if not v.startswith("v"):
                return f"v{v}"
        return v

    # ---------------------------------------------------------
    # Provide convenience constructors
    # ---------------------------------------------------------
    @classmethod
    def new(cls, pipeline_version: str, model_version: str, execution_time_ms: int,
            determinism_fingerprint: Optional[str] = None):
        """
        Smart constructor used by orchestrator.

        Automatically:
          - inserts current UTC timestamp
          - normalizes pipeline_version
          - validates all fields
        """
        ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        return cls(
            timestamp_utc=ts,
            pipeline_version=pipeline_version,
            model_version=model_version,
            execution_time_ms=execution_time_ms,
            determinism_fingerprint=determinism_fingerprint,
        )

    def to_dict(self):
        """Return JSON-serializable metadata dict."""
        return self.model_dump()
