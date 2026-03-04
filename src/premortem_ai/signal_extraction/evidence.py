from __future__ import annotations

from premortem_ai.signal_extraction.line_map import LineMap


def make_span(text: str, start: int, end: int) -> dict:
    start = max(0, start)
    end = min(len(text), end)

    snippet = text[start:end].strip()

    lm = LineMap(text)
    line_start = lm.line_of(start)
    line_end = lm.line_of(max(start, end - 1))

    return {
        "snippet": snippet,
        "start": start,
        "end": end,
        "line_start": line_start,
        "line_end": line_end,
    }