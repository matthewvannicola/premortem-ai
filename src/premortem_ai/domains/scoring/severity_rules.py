"""
severity_rules.py

Applies business rules to adjust severity values.

IMPORTANT:
- Severity is a deterministic metric derived as likelihood × impact.
- LLM-provided severity is advisory only and is NOT persisted.
- This function exists for future extensibility, not arithmetic blending.
"""

from typing import Optional


def apply_severity_rules(
    base_severity: int,
    model_output_severity: Optional[int] = None,
) -> int:
    """
    Apply post-processing rules to computed severity.

    Args:
        base_severity (int): Deterministically computed severity (likelihood × impact)
        model_output_severity (Optional[int]): LLM-suggested severity (ignored)

    Returns:
        int: Authoritative severity value
    """
    return base_severity
