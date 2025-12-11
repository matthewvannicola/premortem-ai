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

    Now supports:
        start(stage_name)
        stop()
    """

    def __init__(self):
        self._start = None
        self._end = None
        self.duration_ms = None
        self.stage_name = None

    def start(self, stage_name=None):
        """Start timing a stage."""
        self.stage_name = stage_name
        self._start = now_ms()
        return self

    def stop(self) -> int:
        """Stop timing and return duration in ms."""
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
    start = now_ms()
    container = {"ms": None}
    yield container
    container["ms"] = now_ms() - start
