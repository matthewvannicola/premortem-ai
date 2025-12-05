import pytest
from src.utils.schema_validation import validate_schema, SchemaValidationError


# ------------------------------------------------------------
# BASIC OBJECT VALIDATION
# ------------------------------------------------------------

def test_valid_simple_object():
    data = {"risk": "Failure", "severity": 3}
    schema = {
        "type": "object",
        "required": ["risk", "severity"],
        "properties": {
            "risk": {"type": "string"},
            "severity": {"type": "integer"},
        },
    }

    # Should not raise
    validate_schema(data, schema)


def test_missing_required_field():
    data = {"risk": "Failure"}  # missing severity
    schema = {
        "type": "object",
        "required": ["risk", "severity"],
        "properties": {
            "risk": {"type": "string"},
            "severity": {"type": "integer"},
        },
    }

    with pytest.raises(SchemaValidationError) as exc:
        validate_schema(data, schema)

    assert "Missing required field 'severity'" in str(exc.value)
    assert "severity" in str(exc.value)


def test_wrong_type_simple_field():
    data = {"risk": "Failure", "severity": "high"}  # wrong type
    schema = {
        "type": "object",
        "required": ["risk", "severity"],
        "properties": {
            "risk": {"type": "string"},
            "severity": {"type": "integer"},
        },
    }

    with pytest.raises(SchemaValidationError) as exc:
        validate_schema(data, schema)

    assert "Expected integer" in str(exc.value)
    assert ".severity" in str(exc.value)


# ------------------------------------------------------------
# NESTED OBJECTS
# ------------------------------------------------------------

def test_nested_object_validation():
    data = {
        "risk": {
            "name": "Latency spike",
            "category": {"type": "performance"}
        }
    }

    schema = {
        "type": "object",
        "required": ["risk"],
        "properties": {
            "risk": {
                "type": "object",
                "required": ["name", "category"],
                "properties": {
                    "name": {"type": "string"},
                    "category": {
                        "type": "object",
                        "required": ["type"],
                        "properties": {
                            "type": {"type": "string"}
                        },
                    },
                },
            },
        },
    }

    validate_schema(data, schema)  # should not raise


def test_nested_object_missing_field():
    data = {
        "risk": {
            "name": "Latency spike",
            "category": {}
        }
    }

    schema = {
        "type": "object",
        "required": ["risk"],
        "properties": {
            "risk": {
                "type": "object",
                "required": ["name", "category"],
                "properties": {
                    "name": {"type": "string"},
                    "category": {
                        "type": "object",
                        "required": ["type"],
                        "properties": {
                            "type": {"type": "string"}
                        },
                    },
                },
            },
        },
    }

    with pytest.raises(SchemaValidationError) as exc:
        validate_schema(data, schema)

    assert "Missing required field 'type'" in str(exc.value)
    assert "risk.category.type" in str(exc.value)


# ------------------------------------------------------------
# ARRAYS + ITEM SCHEMA
# ------------------------------------------------------------

def test_valid_array_items():
    data = ["A", "B", "C"]
    schema = {
        "type": "array",
        "items": {"type": "string"},
    }

    validate_schema(data, schema)  # should not raise


def test_invalid_array_item_type():
    data = ["A", 123, "C"]
    schema = {
        "type": "array",
        "items": {"type": "string"},
    }

    with pytest.raises(SchemaValidationError) as exc:
        validate_schema(data, schema)

    assert "Expected string" in str(exc.value)
    assert "[1]" in str(exc.value)  # index path


def test_array_of_objects():
    data = [
        {"risk": "Failure", "severity": 2},
        {"risk": "Latency", "severity": 4},
    ]

    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["risk", "severity"],
            "properties": {
                "risk": {"type": "string"},
                "severity": {"type": "integer"},
            },
        },
    }

    validate_schema(data, schema)  # should pass


# ------------------------------------------------------------
# TYPE VALIDATION
# ------------------------------------------------------------

@pytest.mark.parametrize(
    "value,expected_type",
    [
        (123, "string"),
        ("abc", "integer"),
        (1.5, "integer"),
        (True, "number"),
        ("yes", "boolean"),
    ],
)
def test_type_validation_failures(value, expected_type):
    schema = {"type": expected_type}
    with pytest.raises(SchemaValidationError):
        validate_schema(value, schema)


# ------------------------------------------------------------
# UNKNOWN TYPE HANDLING
# ------------------------------------------------------------

def test_unknown_schema_type():
    schema = {"type": "mysteryType"}
    with pytest.raises(SchemaValidationError) as exc:
        validate_schema("value", schema)

    assert "Unknown schema type" in str(exc.value)


# ------------------------------------------------------------
# NON-OBJECT ROOT FAILURES
# ------------------------------------------------------------

def test_root_type_mismatch():
    data = "not-an-object"
    schema = {
        "type": "object",
        "required": [],
        "properties": {},
    }

    with pytest.raises(SchemaValidationError):
        validate_schema(data, schema)


# ------------------------------------------------------------
# OPTIONAL FIELDS TEST
# ------------------------------------------------------------

def test_optional_fields_are_ignored_when_missing():
    data = {"risk": "Failure"}
    schema = {
        "type": "object",
        "required": ["risk"],
        "properties": {
            "risk": {"type": "string"},
            "severity": {"type": "integer"},  # optional
        },
    }
    validate_schema(data, schema)  # should not raise
