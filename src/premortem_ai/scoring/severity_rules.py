"""
severity_rules.py

Defines deterministic, verifiable scoring rules for PreMortem AI.

This module provides:
    • Allowed numeric ranges for likelihood & impact
    • Mapping from qualitative categories to numeric values (LLM outputs)
    • A canonical severity formula
    • Fallback scoring for non-LLM flows
    • Input validation utilities

These rules MUST remain stable, as they define the core governance logic
of risk scoring across all environments and pipeline versions.
"""

from typing import Optional
from premortem_ai.exceptions import ValidationError


# ----------------------------------------------------------------------
# Canonical numeric ranges enforced across the system
# ----------------------------------------------------------------------

LIKELIHOOD_MIN = 1
LIKELIHOOD_MAX = 5

IMPACT_MIN = 1
IMPACT_MAX = 5


# ----------------------------------------------------------------------
# Qualitative → Numeric mappings (used by LLM scoring outputs)
# ----------------------------------------------------------------------

LIKELIHOOD_MAP = {
    "very low": 1,
    "low": 2,
    "medium": 3,
    "high": 4,
    "very high": 5,
}

IMPACT_MAP = {
    "minimal": 1,
    "low": 2,
    "moderate": 3,
    "significant": 4,
    "critical": 5,
}


# ----------------------------------------------------------------------
# Validation Utilities
# ----------------------------------------------------------------------

def normalize_category(value: str) -> str:
    """Normalize qualitative labels for consistent mapping."""
    return value.strip().lower()


def validate_numeric_range(
    value: int, *, min_val: int, max_val: int, field_name: str
) -> None:
    """Ensure numeric values are within expected ranges."""
    if not (min_val <= value <= max_val):
        raise ValidationError(
            f"{field_name} value {value} is out of range [{min_val}, {max_val}]."
        )


# ----------------------------------------------------------------------
# Canonical severity formula
# ----------------------------------------------------------------------

def compute_severity_score(likelihood: int, impact: int) -> int:
    """
    Compute a deterministic severity score.

    Formula:
        severity = likelihood × impact

    Examples:
        likelihood=3, impact=4 → 12
        likelihood=5, impact=5 → 25
    """
    validate_numeric_range(
        likelihood,
        min_val=LIKELIHOOD_MIN,
        max_val=LIKELIHOOD_MAX,
        field_name="Likelihood",
    )
    validate_numeric_range(
        impact,
        min_val=IMPACT_MIN,
        max_val=IMPACT_MAX,
        field_name="Impact",
    )

    return likelihood * impact


# ----------------------------------------------------------------------
# Qualitative Scoring Helpers (LLM outputs)
# ----------------------------------------------------------------------

def resolve_likelihood(value: str) -> int:
    """Resolve qualitative likelihood labels to numeric values."""
    key = normalize_category(value)
    if key not in LIKELIHOOD_MAP:
        raise ValidationError(f"Unknown likelihood category: {value}")
    return LIKELIHOOD_MAP[key]


def resolve_impact(value: str) -> int:
    """Resolve qualitative impact labels to numeric values."""
    key = normalize_category(value)
    if key not in IMPACT_MAP:
        raise ValidationError(f"Unknown impact category: {value}")
    return IMPACT_MAP[key]


# ----------------------------------------------------------------------
# Fallback deterministic scoring
# ----------------------------------------------------------------------

def fallback_score(
    likelihood: Optional[int] = None, impact: Optional[int] = None
) -> int:
    """
    Compute a stable fallback score when LLM scoring is unavailable.

    Rules:
        • Missing values default to system median (3)
        • Severity is always computed via canonical formula
    """
    likelihood = likelihood or 3
    impact = impact or 3

    return compute_severity_score(likelihood, impact)
