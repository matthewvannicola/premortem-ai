"""
normalize_text.py

Enterprise-grade normalization utility used throughout the entire PreMortem AI system.

Goals:
    • Produce deterministic, machine-friendly, low-noise text output
    • Remove invisible & zero-width characters
    • Normalize unicode variations (NFKC)
    • Ensure consistent whitespace behaviors across all pipelines
"""

import re
import unicodedata


def normalize_text(value: str) -> str:
    """
    Normalize free-form text into a stable, safe, machine-readable format.

    Steps:
        1. Convert to string (if necessary)
        2. Normalize unicode (NFKC) — collapses accented/full-width characters
        3. Strip leading/trailing whitespace
        4. Remove zero-width & invisible characters
        5. Collapse repeated internal whitespace
        6. Ensure deterministic single-space separation
        7. Return clean, normalized text

    This ensures consistent behavior across:
        • LLM inputs
        • Pydantic models
        • Theme clustering
        • Mitigation generation
        • Summary generation
    """

    if value is None:
        return ""

    if not isinstance(value, str):
        value = str(value)

    # Step 1: Unicode normalization
    text = unicodedata.normalize("NFKC", value)

    # Step 2: Strip leading/trailing whitespace
    text = text.strip()

    # Step 3: Remove zero-width & invisible chars
    invisible_pattern = r"[\u200B\u200C\u200D\uFEFF]"
    text = re.sub(invisible_pattern, "", text)

    # Step 4: Collapse repeated whitespace (spaces, tabs, newlines)
    text = re.sub(r"\s+", " ", text)

    return text
