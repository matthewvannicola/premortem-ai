"""
service.py

Intake orchestration for PreMortem.

This module wires together:
- extraction
- normalization
- canonical input construction

It is the ONLY place where these steps are composed.
"""

from pathlib import Path
from typing import List, Optional

from premortem_ai.intake.extract import extract_documents
from premortem_ai.intake.normalize import normalize_input
from premortem_ai.intake.build_input import build_canonical_input


def intake_submission(
    *,
    file_paths: Optional[List[Path]],
    typed_description: Optional[str],
    user_id: str,
) -> dict:
    """
    Execute the full intake flow and return canonical input.

    This function is safe to call from API layers.
    """

    extracted = []

    if file_paths:
        extracted = extract_documents(file_paths)

    normalized = normalize_input(
        extracted_documents=extracted,
        typed_description=typed_description,
    )

    canonical_input = build_canonical_input(
        normalized_input=normalized,
        user_id=user_id,
    )

    return canonical_input
