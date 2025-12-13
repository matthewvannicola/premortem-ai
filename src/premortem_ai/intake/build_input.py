"""
build_input.py

Canonical input builder for the PreMortem intake layer.

Responsibilities:
- Wrap normalized input into the canonical PreMortem input schema
- Attach submission metadata
- Generate stable identifiers

This module must remain free of reasoning or transformation logic.
"""

from typing import Dict, Optional
from datetime import datetime, timezone
import uuid

from premortem_ai.exceptions import PremortemException


class BuildInputError(PremortemException):
    """Raised when canonical input construction fails."""


def build_canonical_input(
    normalized_input: Dict[str, object],
    user_id: str,
    submission_id: Optional[str] = None,
) -> Dict[str, object]:
    """
    Build the canonical PreMortem input object.

    Args:
        normalized_input: Output from normalize_input()
        user_id: Opaque user identifier
        submission_id: Optional external submission ID

    Returns:
        Canonical input dict suitable for PreMortem pipelines
    """
    if "combined_text" not in normalized_input:
        raise BuildInputError("Missing combined_text in normalized input")

    if "sources" not in normalized_input:
        raise BuildInputError("Missing sources in normalized input")

    submission_id = submission_id or _generate_submission_id()

    input_type = _infer_input_type(
        normalized_input.get("sources", []),
        normalized_input.get("combined_text", ""),
    )

    return {
        "project_context": {
            "combined_text": normalized_input["combined_text"],
            "sources": normalized_input["sources"],
        },
        "submission_metadata": {
            "submission_id": submission_id,
            "user_id": user_id,
            "submitted_at": _utc_now(),
            "input_type": input_type,
        },
    }


def _generate_submission_id() -> str:
    return str(uuid.uuid4())


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _infer_input_type(sources, combined_text: str) -> str:
    """
    Infer how the submission was provided.
    """
    has_files = bool(sources)
    has_text = bool(combined_text and combined_text.strip())

    if has_files and has_text:
        return "mixed"
    if has_files:
        return "file_upload"
    return "text_only"
