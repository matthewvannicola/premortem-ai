"""
metadata.py

Canonical metadata envelope for pipeline execution context.

Used in:
    • PipelineResponse
    • RiskReport
    • Logging + monitoring layers
    • Auditing + reproducibility

This model provides extensible, versioned metadata suitable for
enterprise observability and governance.
"""

from typing import Optional, Dict, Any
from pydantic import Field
from .base_model import CanonicalModel


class Metadata(CanonicalModel):
    """
    Execution metadata for the PreMortem AI pipeline.

    Fields are intentionally optional and expansible for:
        • traceability
        • reproducibility
        • audit logs
        • debugging
        • analytics dashboards
    """

    pipeline_version: Optional[str] = Field(
        None, description="Version of the pipeline used for execution."
    )

    model_used: Optional[str] = Field(
        None, description="LLM model actually executed after resolution."
    )

    execution_time_ms: Optional[int] = Field(
        None,
        ge=0,
        description="Total pipeline execution time in milliseconds.",
    )

    trace_id: Optional[str] = Field(
        None,
        description="Optional trace or correlation ID for distributed tracing.",
    )

    warnings: Optional[list[str]] = Field(
        None,
        description="List of non-fatal warnings generated during execution.",
    )

    extra: Optional[Dict[str, Any]] = Field(
        None,
        description="Extensible metadata namespace for advanced consumers.",
    )
