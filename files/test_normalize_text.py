"""
Utility functions for normalizing free-form text input before sending it
into LLM inference, schema validation, or downstream processing.

Normalization is CRITICAL for deterministic behavior across:
- scoring models
- schema validators
- multi-pass LLM inference
- reporting and comparison logic
"""

import re
import unicodedata


def normalize_text(value):
    """
    Normalize free-form text into a clean, safe, machine-readable form.

    Steps:
    1. Convert to string if needed
    2. Normalize unicode (NFKC form)
    3. Strip leading / trailing whitespace
    4. Collapse repeated internal spaces
    5. Remove invisible / zero-width characters
    6. Lowercase final output
    """
    if value is None:
        return ""

    # Convert non-strings safely
    if not isinstance(value, str):
        value = str(value)

    # Unicode normalization (handles accented chars, full-width forms)
    value = unicodedata.normalize("NFKC", value)

    # Remove zero-width characters (common in copy/paste)
    value = re.sub(r"[\u200B-\u200D\uFEFF]", "", value)

    # Strip whitespace
    value = value.strip()

    # Collapse multiple spaces
    value = re.sub(r"\s+", " ", value)

    # Final lowercase
    return value.lower()


def normalize_multiline_text(value):
    """
    Normalize multi-line content for:
    - project descriptions
    - LLM context windows
    - dataset cleaning
    - prompt construction

    Keeps newlines, but normalizes everything else.
    """
    if value is None:
        return ""

    # Convert non-string
    if not isinstance(value, str):
        value = str(value)

    value = unicodedata.normalize("NFKC", value)

    # Remove zero-width characters
    value = re.sub(r"[\u200B-\u200D\uFEFF]", "", value)

    # Normalize line endings
    value = value.replace("\r\n", "\n").replace("\r", "\n")

    # Strip spaces on each line
    lines = [re.sub(r"\s+", " ", line).strip() for line in value.split("\n")]

    # Join + lowercase
    return "\n".join(lines).lower()
