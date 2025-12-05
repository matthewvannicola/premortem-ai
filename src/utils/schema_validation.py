"""
Schema validation utilities for ensuring deterministic, structured output
from LLM-generated data or upstream system components.

PreMortem AI relies heavily on strict JSON schemas for:
- risk item formatting
- severity scoring inputs
- multi-pass consistency checks
- pipeline debugging and system reliability

This module provides lightweight, dependency-free schema validation
(avoiding heavy frameworks unless needed), with clear error reporting.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


class SchemaValidationError(Exception):
    """Raised when input data does not conform to the expected schema."""
    def __init__(self, message: str, path: Optional[str] = None):
        self.message = message
        self.path = path
        super().__init__(self.__str__())

    def __str__(self) -> str:
        if self.path:
            return f"SchemaValidationError at '{self.path}': {self.message}"
        return f"SchemaValidationError: {self.message}"


def validate_schema(
    data: Any,
    schema: Dict[str, Any],
    path: str = "",
) -> None:
    """
    Validate a Python object (typically LLM output) against a simple schema.

    Supported schema structure:
    ---------------------------
    {
        "type": "object",
        "required": ["field1", "field2"],
        "properties": {
            "field1": {"type": "string"},
            "field2": {"type": "integer"},
            "field3": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }

    Parameters
    ----------
    data : Any
        The object to validate (dict, list, str, int, etc.)
    schema : dict
        A dictionary describing the expected schema.
    path : str
        Internal recursion helper for error paths.

    Raises
    ------
    SchemaValidationError
        If validation fails at any level.

    Returns
    -------
    None
        The function returns only if validation succeeds.

    Examples
    --------
    >>> validate_schema(
            {"risk": "Latency spike", "severity": 4},
            {
                "type": "object",
                "required": ["risk", "severity"],
                "properties": {
                    "risk": {"type": "string"},
                    "severity": {"type": "integer"}
                }
            }
        )
    # No error -> valid
    """

    expected_type = schema.get("type")

    #
    # 1. Root Type Validation
    #
    if expected_type == "object":
        if not isinstance(data, dict):
            raise SchemaValidationError(
                f"Expected object, got {type(data).__name__}",
                path or "$"
            )

        # Required fields
        required = schema.get("required", [])
        for field in required:
            if field not in data:
                raise SchemaValidationError(
                    f"Missing required field '{field}'",
                    _extend_path(path, field)
                )

        # Validate properties
        props = schema.get("properties", {})
        for field, subschema in props.items():
            if field in data:
                validate_schema(
                    data[field],
                    subschema,
                    _extend_path(path, field)
                )

        return

    elif expected_type == "array":
        if not isinstance(data, list):
            raise SchemaValidationError(
                f"Expected array, got {type(data).__name__}",
                path or "$"
            )

        item_schema = schema.get("items")
        if not item_schema:
            return  # Nothing to validate inside

        for idx, item in enumerate(data):
            validate_schema(
                item,
                item_schema,
                _extend_path(path, str(idx))
            )

        return

    elif expected_type == "string":
        if not isinstance(data, str):
            raise SchemaValidationError(
                f"Expected string, got {type(data).__name__}",
                path or "$"
            )
        return

    elif expected_type == "integer":
        if not isinstance(data, int):
            raise SchemaValidationError(
                f"Expected integer, got {type(data).__name__}",
                path or "$"
            )
        return

    elif expected_type == "number":
        if not isinstance(data, (int, float)):
            raise SchemaValidationError(
                f"Expected number, got {type(data).__name__}",
                path or "$"
            )
        return

    elif expected_type == "boolean":
        if not isinstance(data, bool):
            raise SchemaValidationError(
                f"Expected boolean, got {type(data).__name__}",
                path or "$"
            )
        return

    else:
        raise SchemaValidationError(
            f"Unknown schema type '{expected_type}'",
            path or "$"
        )


def _extend_path(base: str, key: str) -> str:
    """
    Safely extend a JSON path for nested schema validation errors.

    Examples:
        base=""     key="risk"     -> "risk"
        base="root" key="severity" -> "root.severity"
        base="arr"  key="0"        -> "arr[0]"
    """
    if base == "":
        return key
    if key.isdigit():
        return f"{base}[{key}]"
    return f"{base}.{key}"
