from pydantic import Field

from premortem_ai.models.risk_report import RiskReport
from .base_model import CanonicalModel


class PipelineResponse(CanonicalModel):
    """
    Canonical response envelope for the /analysis pipeline endpoint.

    Mirrors pipeline_response.schema.json and is returned by:
      - analysis_service
      - orchestrator (public interface)
      - API gateway (REST)
      - CLI integrations
      - SDK consumers

    Provides a stable, versionable contract around the RiskReport payload.

    Inherits:
      - strict schema validation
      - deterministic serialization
      - immutable model behavior
      - version tagging
    """

    report: RiskReport = Field(
        ...,
        description="Fully validated RiskReport object representing the entire pipeline output."
    )

    # ---------------------------------------------------------
    # Convenience constructors
    # ---------------------------------------------------------
    @classmethod
    def from_report(cls, report: RiskReport):
        """
        Create a PipelineResponse directly from a RiskReport.
        Used by orchestrator or service layer.
        """
        return cls(report=report)

    def to_dict(self):
        """Return a clean JSON-serializable response aligned with schema."""
        return self.model_dump()
