"""
timer.py

Lightweight, enterprise-safe timing utility for measuring execution durations.

This module is used by:
    • analysis_service
    • orchestrator
    • pipeline steps (discovery, scoring, themes, mitigation, summary)
    • metadata generation
    • observability & performance instrumentation

Provides:
    • Precise millisecond timing
    • Context-manager API
    • Deterministic behavior across environments
"""

import time
from contextlib import contextmanager


def now_ms() -> int:
    """Return current time in milliseconds."""
    return int(time.time() * 1000)


class Timer:
    """
    Simple timer object for measuring execution duration.

    Usage:
        t = Timer()
        t.start()
        ... work ...
        duration = t.stop()  # returns ms

    Also supports:
        with Timer() as t:
            ... work ...
        print(t.duration_ms)
    """

    def __init__(self):
        self._start = None
        self._end = None
        self.duration_ms = None

    def start(self):
        self._start = now_ms()
        return self

    def stop(self) -> int:
        self._end = now_ms()
        self.duration_ms = self._end - self._start
        return self.duration_ms

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()


@contextmanager
def timing() -> int:
    """
    Simple context manager for timing blocks of code.

    Example:
        with timing() as t:
            run_pipeline()

        print(t["ms"])
    """
    start = now_ms()
    container = {"ms": None}
    yield container
    container["ms"] = now_ms() - start
