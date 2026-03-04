from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from premortem_ai.signal_extraction.normalize import NormalizedDoc


@dataclass(frozen=True)
class Signal:
    signal_id: str
    severity: str # low, medium, high, critical
    summary: str
    rule_id: str
    confidence: float
    evidence: list[dict]


@dataclass(frozen=True)
class RuleResult:
    signals: list[Signal]


class Rule(Protocol):
    rule_id: str

    def run(self, doc: NormalizedDoc) -> RuleResult: ...