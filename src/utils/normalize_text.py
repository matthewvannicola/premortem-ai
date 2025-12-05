"""
Utility functions for normalizing free-form text input before sending it
into LLM inference, schema validation, or downstream processing.

Normalization is CRITICAL for deterministic behavior across:
- scoring models
- schema validators
- multi-pass LLM inference
- reporting and comparison logic
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any


# Precompiled regex patterns for performance
_WHITESPACE_RE = re.compile(r"\s+")
# Zero-width / invisible characters that often sneak in from copy-paste
_INVISIBLE_RE = re.compile(r"[\u200B-\u200D\uFEFF]")


def normalize_text(
    value: Any,
    *,
    preserve_case: bool = False,
    collapse_whitespace: bool = True,
) -> str:
    """
    Normalize free-form text into a clean, safe, machine-readable form.

    Steps:
    1. Convert to string if needed (None -> "")
    2. Normalize unicode (NFKC form)
    3. Strip leading / trailing whitespace
    4. Optionally collapse repeated internal whitespace
    5. Remove invisible / zero-width characters
    6. Lowercase final output (unless preserve_case=True)

    Parameters
    ----------
    value:
        Any incoming value (user input, JSON field, etc.).
    preserve_case:
        If True, the function will NOT lowercase the result.
        Defaults to False for more deterministic comparisons.
    collapse_whitespace:
        If True, internal runs of whitespace are collapsed to a single space.
        Set False if the exact spacing is semantically meaningful.

    Returns
    -------
    str
        A normalized text string safe for downstream processing.

    Examples
    --------
    >>> normalize_text("  Héllo\\u200b   WORLD  ")
    'hello world'

    >>> normalize_text("  Héllo   WORLD  ", preserve_case=True)
    'Héllo WORLD'
    """
    if value is None:
        return ""

    # Convert non-strings safely (e.g., numbers, booleans)
    if not isinstance(value, str):
        value = str(value)

    # Unicode normalization (handles accented chars, full-width forms, etc.)
    value = unicodedata.normalize("NFKC", value)

    # Strip leading / trailing whitespace
    value = value.strip()

    # Optionally collapse internal whitespace to a single space
    if collapse_whitespace:
        value = _WHITESPACE_RE.sub(" ", value)

    # Remove invisible / zero-width characters
    value = _INVISIBLE_RE.sub("", value)

    # Default to lowercase for stable comparisons
    if not preserve_case:
        value = value.lower()

    return value
