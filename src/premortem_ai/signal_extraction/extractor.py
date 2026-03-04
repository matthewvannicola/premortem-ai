from __future__ import annotations

import time
from uuid import uuid4

from premortem_ai.signal_extraction.normalize import NormalizedDoc, normalize_text
from premortem_ai.signal_extraction.rules.base import Signal
from premortem_ai.signal_extraction.rules.obs_rules import NoLoggingRule
from premortem_ai.signal_extraction.rules.pii_rules import PiiPresentRule


class SignalExtractor:
    def __init__(self) -> None:
        self.rules = [
            PiiPresentRule(),
            NoLoggingRule(),
        ]

    def extract(self, *, doc_id: str, source_type: str, text: str) -> dict:
        t0 = time.perf_counter()
        trace_id = str(uuid4())

        doc = NormalizedDoc(doc_id=doc_id, source_type=source_type, text=normalize_text(text))

        signals: list[Signal] = []
        for rule in self.rules:
            signals.extend(rule.run(doc).signals)

        runtime_ms = int((time.perf_counter() - t0) * 1000)
        
        return {
            "trace_id": trace_id,
            "doc_id": doc_id,
            "source_type": source_type,
            "signals": [signal.dict() for signal in signals],
            "stats": {
                "rules_run": len(self.rules),
                "signals_emitted": len(signals),
                "runtime_ms": runtime_ms,
            },
        }
