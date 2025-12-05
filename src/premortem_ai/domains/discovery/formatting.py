"""
Formatting utilities for the Discovery domain.

This module contains small, deterministic transformation helpers used to
post-process risk items before they move into downstream pipeline stages.

Responsibilities:
    - Normalize titles + descriptions beyond basic text cleaning
    - Enforce minimum-length requirements
    - Remove duplicates or near-duplicates (optional extension point)
    - Ensure final output is shaped consistently for schema validation

These functions are intentionally narrow in scope and side-effect free.
"""

from typing import List, Dict
from premortem_ai.core.normalize_text import normalize_text


def format_risk_title(title: str) -> str:
    """
    Apply additional normalization rules specific to risk titles.
    """

    title = normalize_text(title)

    # Capitalize for readability (post-normalization)
    if title:
        title = title.capitalize()

    return title


def format_risk_description(text: str) -> str:
    """
    Normalize risk descriptions while preserving readability.
    """

    text = normalize_text(text)

    # Basic formatting rule: ensure first letter capitalized
    if text:
        text = text[0].upper() + text[1:]

    return text


def apply_risk_formatting(risks: List[Dict]) -> List[Dict]:
    """
    Apply formatting rules to a list of risk items.

    Args:
        risks (list[dict]): Raw or partially cleaned risk objects.

    Returns:
        list[dict]: Formatted risk objects.
    """

    formatted = []

    for item in risks:

        title = format_risk_title(item.get("title", ""))
        description = format_risk_description(item.get("description", ""))

        formatted.append(
            {
                "title": title,
                "description": description,
            }
        )

    return formatted


__all__ = [
    "format_risk_title",
    "format_risk_description",
    "apply_risk_formatting",
]
