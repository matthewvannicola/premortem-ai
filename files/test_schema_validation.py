import json
import pytest
from src.utils.validate_schema import validate_against_schema

# Path to your schema file
SCHEMA_PATH = "schemas/risk_output.schema.json"

# Load schema once for all tests
with open(SCHEMA_PATH, "r") as f:
    SCHEMA = json.load(f)


def test_valid_output_passes_validation():
    """A correct JSON structure should pass."""
    sample = {
        "risk_items": [
            {
                "id": "R-001",
                "title": "Unclear requirements",
                "severity": 3,
                "probability": "Medium",
                "impact": "High",
                "category": "Requirements",
                "details": "Ambiguity in specification",
                "mitigation": "Clarify scope with stakeholders"
            }
        ],
        "summary": {
            "total_risks": 1,
            "highest_severity": 3
        }
    }

    result = validate_against_schema(sample, SCHEMA)
    assert result.is_valid, f"Validation failed: {result.errors}"


def test_missing_required_field_fails():
    """Removing mandatory fields should fail schema validation."""
    bad_sample = {
        "risk_items": [
            {
                "title": "Missing ID field"
            }
        ]
    }

    result = validate_against_schema(bad_sample, SCHEMA)
    assert not result.is_valid
    assert "id" in result.errors[0].lower()


def test_invalid_enum_value_fails():
    """Ensure enums are enforced correctly."""
    bad_sample = {
        "risk_items": [
            {
                "id": "R-002",
                "title": "Risk with invalid probability",
                "severity": 2,
                "probability": "Unknown",  # invalid enum
                "impact": "Low",
                "category": "Requirements",
                "details": "Testing enum failure",
                "mitigation": "Fix enum"
            }
        ],
        "summary": {
            "total_risks": 1,
            "highest_severity": 2
        }
    }

    result = validate_against_schema(bad_sample, SCHEMA)
    assert not result.is_valid
    assert "probability" in result.errors[0].lower()
