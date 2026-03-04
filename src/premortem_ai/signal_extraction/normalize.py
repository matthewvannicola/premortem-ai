from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedDoc:
    doc_id: str
    source_type: str
    text: str


def normalize_text(text: str) -> str:
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    return t.strip()