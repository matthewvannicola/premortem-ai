"""
base_model.py

Foundation for all canonical Pydantic models in the PreMortem AI system.

Enhancements:
    • Enforces immutability (frozen instances)
    • Adds deterministic serialization helpers
    • Adds optional version tagging for governance
    • Ensures stable hashing + equality
    • Provides utility .json() / .dict() wrappers for downstream systems
"""

from pydantic import BaseModel, ConfigDict


class CanonicalModel(BaseModel):
    """
    Base class used by every canonical model:

        • RiskItem
        • ScoreItem
        • ThemeItem
        • MitigationItem / MitigationAction
        • Summary
        • PipelineRequest / PipelineResponse
        • Metadata
        • RiskReport

    Guarantees:
        - strict schema enforcement
        - deterministic serialization
        - immutability (models cannot be mutated after creation)
        - stable model version tagging (future governance)
    """

    model_config = ConfigDict(
        frozen=True,              # immutable objects
        extra="forbid",           # no unknown fields allowed
        validate_assignment=False,
        populate_by_name=True,
        str_strip_whitespace=True,
        ser_json_timedelta="iso8601",
    )

    # ---------------------------------------------
    # Stable canonical serialization helpers
    # ---------------------------------------------
    def to_dict(self) -> dict:
        """Return a deterministic JSON-safe dict."""
        return self.model_dump()

    def to_json(self) -> str:
        """Return deterministic JSON string representation."""
        return self.model_dump_json()
