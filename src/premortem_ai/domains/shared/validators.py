"""
validators.py

Common validation utilities used across discovery, scoring, themes, and mitigation.
"""

from premortem_ai.exceptions import ValidationError

def require_fields(data: dict, fields: list, context: str = ""):
    for field in fields:
        if field not in data:
            raise ValidationError(
                f"Missing field '{field}' in {context}: {data}"
            )
