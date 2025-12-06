"""
timer.py

Lightweight timing utility used throughout the PreMortem AI pipeline.

This module provides:
    - A context manager for measuring code block duration
    - A simple `.duration_ms` attribute for downstream logging or metrics
    - A future-friendly design for integration with observability tooling

Usage:

    from premortem_ai.utils.timer import Timer

    with Timer() as t:
        run_pipeline_stage()

    print(t.duration_ms)

"""

import time
from dataclasses import dataclass


@dataclass
class Timer:
    """
    Simple context manager for measuring execution time in milliseconds.

    Attributes:
        start (float): timestamp at context entry (epoch seconds)
        end (float): timestamp at context exit
        duration_ms (int): total elapsed time in milliseconds
    """

    start: float = 0.0
    end: float = 0.0
    duration_ms: int | None = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.end = time.time()
        self.duration_ms = int((self.end - self.start) * 1000)

        # Returning False allows exceptions to propagate normally.
        return False
