import json
import pytest
from src.utils.validate_schema import validate_json

# Load the schema for testing
with open("schemas/risk_output.schema.json", "r") as f:
    RISK_SCHEMA = json.load(f)


def test_valid_risk_output_passes_validation():
    """A fully valid risk output JSON should pass schema validation."""

    valid_item = {
        "id": "RISK-001",
        "category": "technical",
        "probability": "medium",
        "impact": "high",
        "severity": 4,
        "description": "API dependency may fail under high load.",
        "mitigation": "Implement caching + fallback."
    }

    # Should NOT raise any exception
    validate_json(valid_item, RISK_SCHEMA)


def test_invalid_enum_fails_validation():
    """Invalid probability or impact values should fail validation."""

    invalid_item = {
        "id": "RISK-XYZ",
        "category": "technical",
        "probability": "sometimes",  # ❌ invalid enum
        "impact": "high",
        "severity": 3,
        "description": "Bad enum value",
        "mitigation": "Fix enums"
    }

    with pytest.raises(Exception):
        validate_json(invalid_item, RISK_SCHEMA)


def test_missing_required_field_fails_validation():
    """Items missing required fields should fail."""

    invalid_item = {
        # "id" missing ❌
        "category": "operational",
        "probability": "low",
        "impact": "low",
        "severity": 1,
        "description": "Missing required field",
        "mitigation": "Add the field"
    }

    with pytest.raises(Exception):
        validate_json(invalid_item, RISK_SCHEMA)
