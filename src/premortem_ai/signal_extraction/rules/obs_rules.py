from __future__ import annotations

from premortem_ai.signal_extraction.normalize import NormalizedDoc
from premortem_ai.signal_extraction.rules.base import RuleResult, Signal


OBS_KEYWORDS = (
    "logging",
    "logs",
    "log retention",
    "metrics",
    "monitoring",
    "tracing",
    "trace",
    "observability",
    "opentelemetry",
)


class NoLoggingRule:
    rule_id = "R_OBS_001"

    def run(self, doc: NormalizedDoc) -> RuleResult:
        text_lower = doc.text.lower()
        if any(k in text_lower for k in OBS_KEYWORDS):
            return RuleResult(signals=[])

        return RuleResult(
            signals=[
                Signal(
                    signal_id="NO_LOGGING",
                    severity="high",
                    summary="No mention of logging/metrics/tracing (observability) practices.",
                    rule_id=self.rule_id,
                    confidence=0.85,
                    evidence=[],
                )
            ]
        )