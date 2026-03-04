from __future__ import annotations

import re

from premortem_ai.signal_extraction.evidence import make_span
from premortem_ai.signal_extraction.normalize import NormalizedDoc
from premortem_ai.signal_extraction.rules.base import RuleResult, Signal


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


class PiiPresentRule:
    rule_id = "R_PRIV_001"

    def run(self, doc: NormalizedDoc) -> RuleResult:
        text = doc.text
        evidence: list[dict] = []

        for m in EMAIL_RE.finditer(text):
            evidence.append(make_span(text, m.start(), m.end()))
        for m in SSN_RE.finditer(text):
            evidence.append(make_span(text, m.start(), m.end()))

        if not evidence:
            return RuleResult(signals=[])

        return RuleResult(
            signals=[
                Signal(
                    signal_id="PII_PRESENT",
                    severity="high",
                    summary="Potential PII detected (email and/or SSN patterns found).",
                    rule_id=self.rule_id,
                    confidence=0.90,
                    evidence=evidence[:10],
                )
            ]
        )