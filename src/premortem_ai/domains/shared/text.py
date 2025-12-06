"""
text.py

Shared text utilities for the domains layer.
"""

import re

def collapse_whitespace(value: str) -> str:
    if not isinstance(value, str):
        return value
    return re.sub(r"\s+", " ", value).strip()


def normalize_sentence(value: str) -> str:
    """Ensure sentences start capitalized and end with a period."""
    if not value:
        return value
    v = value.strip()
    if not v.endswith("."):
        v += "."
    return v[0].upper() + v[1:]
