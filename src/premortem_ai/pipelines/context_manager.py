"""
context_manager.py

PipelineContext stores all intermediate artifacts produced by each stage
of the PreMortem AI pipeline. The Orchestrator passes a single context
object through each stage, ensuring:
    - clean isolation
    - centralized metadata
    - reproducible pipeline execution
    - stage-level timing metrics
"""

from typing import Dict, Any, List, Optional
from premortem_ai.core.utils.timer import Timer


class PipelineContext:
    """
    Accumulates results across all pipeline stages.
    Domain services should ONLY read/write within this object.
    """

    def __init__(self):
        # Core stage outputs
        self.risks: Dict[str, Any] = {}
        self.scores: Dict[str, Any] = {}
        self.themes: List[Any] = []
        self.mitigations: List[Any] = []
        self.summary: Optional[Any] = None

        # Metadata for analytics + observability
        self.stage_timings: Dict[str, float] = {}
        self.request_metadata: Dict[str, Any] = {}

        # Internal high-precision timer object
        self._timer = Timer()

    # -------------------------------------------------------------
    # Stage timing helpers
    # -------------------------------------------------------------

    def mark_stage_start(self, stage_name: str):
        """Begin timing a stage execution."""
        self._timer.start(stage_name)

    def mark_stage_end(self, stage_name: str):
        """End timing and record elapsed duration."""
        elapsed = self._timer.stop(stage_name)
        self.stage_timings[stage_name] = elapsed
