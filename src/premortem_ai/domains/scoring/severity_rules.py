"""
severity_rules.py

Applies business rules to adjust severity values.
"""

def apply_severity_rules(base_severity: int, model_output_severity: int) -> int:
    """
    Blend deterministic severity with the LLM's suggested severity.

    Current rule:
        - If they differ, average them.
        - Ensures consistency and prevents outlier LLM values.

    Args:
        base_severity (int)
        model_output_severity (int)

    Returns:
        int: adjusted severity
    """
    if base_severity == model_output_severity:
        return base_severity

    return round((base_severity + model_output_severity) / 2)
