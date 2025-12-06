"""
pipeline_response.py

Enterprise-grade canonical response model for the PreMortem AI analysis pipeline.

Enhancements:
    • Clearer documentation
    • Defensive from_report constructor
    • Guaranteed serialization stability
    • Future-proofing hooks for metadata or diagnostics
"""

from pydantic import Field

from premortem_ai.models.risk_report import RiskReport
from .base_model import CanonicalModel


class PipelineResponse(CanonicalModel):
    """
    Canonical response envelope for the PreMortem AI pipeline.

    Returned by:
        • analysis_service
        • orchestrator (public interface)
        • REST API endpoints
        • CLI workflow runners
        • automated job runners (Pipedream, Make.com)

    This object must remain a stable, versioned contract for all consumers.
    """

    report: RiskReport = Field(
        ...,
        description=(
            "Fully validated RiskReport object representing the complete output "
            "of the PreMortem AI pipeline."
        ),
    )

    # ------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------
    @classmethod
    def from_report(cls, report: RiskReport):
        """
        Wrap a RiskReport in a PipelineResponse.

        Provides:
            • deterministic wrapping
            • strict validation before returning to external clients
        """
        if not isinstance(report, RiskReport):
            raise TypeError(
                f"PipelineResponse.from_report expected RiskReport, received {type(report)}"
            )
        return cls(report=report)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------
    def to_dict(self):
        """
        Return a clean, deterministic JSON representation suitable for
        external APIs, logging, storage, dashboards, or PDF generation.
        """
        return self.model_dump()
