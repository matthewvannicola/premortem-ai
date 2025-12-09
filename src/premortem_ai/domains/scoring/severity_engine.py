"""
severity_engine.py

Generates a severity score using standard risk-matrix logic.
This is a standalone deterministic helper — it does NOT call the LLM.
"""

def compute_severity(likelihood: int, impact: int) -> int:
    """
    Basic multiplicative severity model.

    Args:
        likelihood (int): LLM-estimated likelihood (1–n)
        impact (int): LLM-estimated impact (1–n)

    Returns:
        int: computed severity score
    """
    return likelihood * impact
