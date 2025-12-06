"""
risk_to_text.py

Convert RiskItem objects into standardized textual blocks.
Used by themes, summary, and mitigation domains.
"""

from premortem_ai.models import RiskItem

def risk_to_text(risk_id: str, risk: RiskItem) -> str:
    return f"{risk_id}: {risk.title} — {risk.description}"
