"""
normalize.py

Deterministic text normalization for the PreMortem intake layer.

Responsibilities:
- Merge extracted document text with optional user-provided description
- Preserve source boundaries for auditability
- Perform light, non-semantic cleanup only
- Enforce hard size limits

This module must remain free of reasoning or interpretation logic.
"""

from typing import List, Dict, Optional

from premortem_ai.exceptions import PremortemException


class NormalizationError(PremortemException):
    """Raised when normalization fails."""


MAX_CHARS = 200_000  # hard safety limit


def normalize_input(
    extracted_documents: List[Dict[str, str]],
    typed_description: Optional[str] = None,
) -> Dict[str, object]:
    """
    Normalize extracted text and optional typed description into
    a single canonical text block.

    Args:
        extracted_documents: Output of extract_documents()
        typed_description: Optional free-text description from the user

    Returns:
        Dict with keys:
            - combined_text
            - sources
            - stats
    """
    sections: List[str] = []
    sources: List[Dict[str, str]] = []

    # Typed description comes first (if provided)
    if typed_description and typed_description.strip():
        sections.append("===== USER DESCRIPTION =====")
        sections.append(_clean_text(typed_description))

    for doc in extracted_documents:
        filename = doc["filename"]
        file_type = doc["file_type"]
        text = doc["text"]

        if not text or not text.strip():
            raise NormalizationError(
                f"Document '{filename}' contains no extractable text"
            )

        sections.append(
            f"===== SOURCE: {filename} ({file_type}) ====="
        )
        sections.append(_clean_text(text))

        sources.append(
            {
                "filename": filename,
                "file_type": file_type,
            }
        )

    combined_text = "\n\n".join(sections)

    if len(combined_text) > MAX_CHARS:
        raise NormalizationError(
            f"Normalized input exceeds max size of {MAX_CHARS} characters "
            f"({len(combined_text)} chars)"
        )

    return {
        "combined_text": combined_text,
        "sources": sources,
        "stats": {
            "document_count": len(extracted_documents),
            "character_count": len(combined_text),
        },
    }


def _clean_text(text: str) -> str:
    """
    Perform minimal, non-semantic cleanup.
    """
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Trim leading/trailing whitespace
    text = text.strip()

    # Collapse excessive blank lines (3+ -> 2)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text
