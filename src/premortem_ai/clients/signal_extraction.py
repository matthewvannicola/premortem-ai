from __future__ import annotations

from premortem_ai.signal_extraction.extractor import SignalExtractor

_extractor = SignalExtractor()


def extract_signals(*, doc_id: str, source_type: str, text: str) -> dict:
    """
    Stable interface for signal extraction.
    Today: in-process deterministic engine.
    Future: swap to HTTP client without changing callers.
    """
    return _extractor.extract(doc_id=doc_id, source_type=source_type, text=text)