from pydantic import BaseModel, Field
from premortem_ai.models.risk_report import RiskReport


class PipelineResponse(BaseModel):
    """
    Canonical response envelope for the /analysis pipeline endpoint.

    Mirrors pipeline_response.schema.json and is returned by:
      - analysis_service
      - orchestrator (public interface)
      - API gateway (REST)
      - CLI integrations
      - SDK consumers

    Provides a stable, versionable contract around the RiskReport payload.
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
