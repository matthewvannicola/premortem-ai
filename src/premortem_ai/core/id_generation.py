"""
Deterministic ID generation utilities for the PreMortem AI pipeline.

Risk, theme, and mitigation items must be assigned stable identifiers so that:
- Downstream components (scoring, themes, mitigation) can reference items safely.
- Reports and audit logs remain consistent across executions.
- External systems (Google Docs, Notion, dashboards) have stable cross-links.

This module provides safe, human-readable ID generators with strict prefixes.
"""

import uuid


def _generate(prefix: str) -> str:
    """
    Internal helper for generating compact UUID4-based identifiers.

    Args:
        prefix (str): Short domain prefix (e.g. "risk", "theme").

    Returns:
        str: An identifier of the form "<prefix>-xxxxxxxx".
    """
    raw = uuid.uuid4().hex[:8]  # short but collision-resistant
    return f"{prefix}-{raw}"


def generate_risk_id() -> str:
    """
    Generate a unique ID for a risk item.

    Example:
        risk-3fa29bc1
    """
    return _generate("risk")


def generate_theme_id() -> str:
    """
    Generate a unique ID for a theme item.

    Example:
        theme-a91be442
    """
    return _generate("theme")


__all__ = ["generate_risk_id", "generate_theme_id"]
