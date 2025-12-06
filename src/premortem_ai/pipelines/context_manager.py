"""
context_manager.py

Holds all intermediate products of the pipeline during execution.
This object is passed through each stage for safe accumulation of results.
"""

from typing import Dict, Any, List, Optional
from premortem_ai.core.timer import Timer


class PipelineContext:
    def __init__(self):
        # Stages accumulate into these collections
        self.risks: Dict[str, Any] = {}
        self.scores: Dict[str, Any] = {}
        self.themes: List[Any] = []
        self.mitigations: List[Any] = []
        self.summary: Optional[Any] = None

        # Metadata
        self.stage_timings: Dict[str, float] = {}
        self.request_metadata: Dict[str, Any] = {}

        # Internal timer
        self._timer = Timer()

    def mark_stage_start(self, stage_name: str):
        self._timer.start(stage_name)

    def mark_stage_end(self, stage_name: str):
        elapsed = self._timer.stop(stage_name)
        self.stage_timings[stage_name] = elapsed
