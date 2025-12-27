"""
timer.py

Execution timing utility for the PreMortem AI pipeline.
Supports both:
    • context manager timing
    • explicit start/stop timing for pipeline stages
"""

import time
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Timer:
    # For context manager mode
    start_time: float = 0.0
    end_time: float = 0.0
    duration_ms: Optional[int] = None

    # For pipeline stage tracking
    stage_start_times: Dict[str, float] = field(default_factory=dict)
    stage_durations: Dict[str, float] = field(default_factory=dict)

    # ----------------------------
    # Context Manager Support
    # ----------------------------
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.end_time = time.time()
        self.duration_ms = int((self.end_time - self.start_time) * 1000)
        return False  # allow exceptions through

    # ----------------------------
    # Stage Timing (Pipeline)
    # ----------------------------
    def start(self, stage: str):
        self.stage_start_times[stage] = time.time()

    def stop(self, stage: str) -> float:
        if stage not in self.stage_start_times:
            raise RuntimeError(f"Timer.stop('{stage}') called without start().")

        elapsed = time.time() - self.stage_start_times[stage]
        self.stage_durations[stage] = round(elapsed, 4)
        return elapsed

    def get(self, stage: str) -> Optional[float]:
        return self.stage_durations.get(stage)

