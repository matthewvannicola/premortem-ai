"""
Text normalization utilities for the PreMortem AI pipeline.

LLM-driven systems require deterministic, stable text preprocessing to ensure
consistent scoring, validation, and downstream inference. This module provides
safe normalization functions used across all pipeline stages.

Normalization Goals:
- Ensure unicode consistency (NFKC)
- Remove invisible characters
- Normalize whitespace
- Guarantee string output even for unexpected input types
"""

import re
import unicodedata


def normalize_text(value: str) -> str:
    """
    Normalize free-form text into a stable, machine-safe representation.

    Steps:
        1. Convert input to string safely.
        2. Normalize unicode into NFKC form.
        3. Strip leading/trailing whitespace.
        4. Collapse repeated internal whitespace.
        5. Remove zero-width and invisible characters.

    Args:
        value (str | Any): Raw input text.

    Returns:
        str: Normalized, safe, lower-cased text.
    """

    if value is None:
        return ""

    # Convert non-strings safely
    if not isinstance(value, str):
        value = str(value)

    # Unicode normalization (handles accented chars, full-width forms)
    value = unicodedata.normalize("NFKC", value)

    # Remove zero-width & invisible characters
    value = re.sub(r"[\u200B-\u200D\uFEFF]", "", value)

    # Collapse repeated whitespace
    value = re.sub(r"\s+", " ", value)

    # Trim + lowercase for deterministic comparison
    value = value.strip().lower()

    return value


__all__ = ["normalize_text"]
