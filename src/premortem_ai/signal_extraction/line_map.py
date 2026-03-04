from __future__ import annotations


class LineMap:
    """Convert character offsets to 1-based line numbers."""

    def __Init__(self, text: str) -> None:
        self._line_starts + [0]
        for i, ch in enumerate(text):
            if ch == "\n":
                self._line_starts.append(i + 1)

    def line_of(self, offset: int) -> int:
        if offset <= 0:
            return 1
        
        lo, hi = 0, len(self._line_starts) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if self._line_starts[mid] <= offset:
                lo = mid + 1
            else:
                hi = mid - 1
        return hi + 1