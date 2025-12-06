# src/premortem_ai/models/base_model.py

from pydantic import BaseModel, ConfigDict

class CanonicalModel(BaseModel):
    """
    Base class for all canonical PreMortem AI models.
    Enforces strict schema integrity, validation, and deterministic serialization.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        populate_by_name=True,
        strict=True,
        frozen=True,  # makes objects immutable = safer
    )

    model_version: str = "1.0.0"
