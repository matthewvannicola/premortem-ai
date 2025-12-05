"""
Schema validation utilities for the PreMortem AI pipeline.

LLM-generated JSON must be validated rigorously to ensure downstream steps
receive predictable, contract-aligned structures. This module provides a
minimal and dependable schema validation mechanism optimized for pipelines
where deterministic behavior and clear error traces are essential.

Design Notes:
- Avoid heavy dependencies (e.g., jsonschema) for speed and portability.
- Validate only the structural requirements needed by downstream components.
- Provide clear, human-readable error messages for debugging and logs.
"""

from typing import Any, Dict, List, Optional


class SchemaValidationError(Exception):
    """Raised when a data payload fails schema validation."""


def validate_schema(
    data: Any,
    schema: Dict[str, Any],
    context: Optional[str] = None,
) -> None:
    """
    Validate a Python object against a simplified JSON schema definition.

    Supported schema fields:
        - type: "object", "array", "string", "number", "boolean"
        - required: list of required keys (for objects)
        - properties: nested schemas for object fields
        - items: schema definition for array elements

    Args:
        data (Any): The payload to validate.
        schema (dict): The schema contract.
        context (str | None): Optional string describing the validation context
            (e.g., "risk item", "summary block"). Used for clearer error traces.

    Raises:
        SchemaValidationError: If the payload violates the schema contract.
    """

    context_label = f"[{context}] " if context else ""

    expected_type = schema.get("type")

    # Validate top-level type
    if expected_type == "object":
        if not isinstance(data, dict):
            raise SchemaValidationError(
                f"{context_label}Expected object, received {type(data).__name__}"
            )
        _validate_object(data, schema, context_label)

    elif expected_type == "array":
        if not isinstance(data, list):
            raise SchemaValidationError(
                f"{context_label}Expected array, received {type(data).__name__}"
            )
        _validate_array(data, schema, context_label)

    elif expected_type == "string":
        if not isinstance(data, str):
            raise SchemaValidationError(
                f"{context_label}Expected string, received {type(data).__name__}"
            )

    elif expected_type == "number":
        if not isinstance(data, (int, float)):
            raise SchemaValidationError(
                f"{context_label}Expected number, received {type(data).__name__}"
            )

    elif expected_type == "boolean":
        if not isinstance(data, bool):
            raise SchemaValidationError(
                f"{context_label}Expected boolean, received {type(data).__name__}"
            )

    else:
        raise SchemaValidationError(
            f"{context_label}Unsupported or missing schema type '{expected_type}'"
        )


def _validate_object(data: Dict[str, Any], schema: Dict[str, Any], ctx: str) -> None:
    """Internal helper to validate object properties and required fields."""

    required_fields: List[str] = schema.get("required", [])
    properties: Dict[str, Any] = schema.get("properties", {})

    # Check required fields
    for field in required_fields:
        if field not in data:
            raise SchemaValidationError(f"{ctx}Missing required field '{field}'")

    # Validate property schemas
    for key, value in data.items():
        if key not in properties:
            # Allow extra fields—keep schema flexible for model evolution
            continue

        validate_schema(value, properties[key], context=f"{ctx}{key}")


def _validate_array(data: List[Any], schema: Dict[str, Any], ctx: str) -> None:
    """Internal helper to validate array items."""
    item_schema = schema.get("items")
    if not item_schema:
        return

    for idx, item in enumerate(data):
        validate_schema(item, item_schema, context=f"{ctx}item[{idx}]")


__all__ = ["validate_schema", "SchemaValidationError"]
