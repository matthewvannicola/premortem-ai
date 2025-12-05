"""
Execution graph utilities for the PreMortem AI pipeline.

This module defines a lightweight execution graph abstraction that models
the ordered pipeline stages and their dependencies. It does not execute
domain logic; rather, it provides structure, metadata, and introspection
to support the orchestrator.

Core Responsibilities:
- Maintain canonical pipeline order
- Represent dependencies between stages
- Validate that all required stages are present
- Provide a traceable execution plan for auditing
"""

from typing import List, Dict


class ExecutionGraphError(Exception):
    """Raised when the execution graph is malformed or incomplete."""


class ExecutionGraph:
    """
    Represents the ordered pipeline stages for PreMortem AI.

    Designed for:
        - Deterministic execution order
        - Clear stage boundaries
        - Dependency awareness
        - Auditability / logging / introspection

    Stages are stored as a list of identifiers, e.g.:

        ["discovery", "scoring", "themes", "mitigation", "summary", "report"]

    Each identifier corresponds to a domain execution function implemented
    elsewhere in the codebase.
    """

    DEFAULT_STAGES = [
        "discovery",
        "scoring",
        "themes",
        "mitigation",
        "summary",
        "report",
    ]

    def __init__(self, stages: List[str] = None):
        self.stages = stages or self.DEFAULT_STAGES
        self._validate()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _validate(self) -> None:
        """Ensure the execution graph meets minimum structural requirements."""

        if not self.stages:
            raise ExecutionGraphError("Execution graph cannot be empty.")

        # All stages must be strings
        if any(not isinstance(stage, str) for stage in self.stages):
            raise ExecutionGraphError("Stage identifiers must be strings.")

        # Ensure no duplicates (ordering must be unique)
        if len(self.stages) != len(set(self.stages)):
            raise ExecutionGraphError("Duplicate stage identifiers detected.")

        # Must include all required default stages (or a subset specifically allowed)
        missing = [s for s in self.DEFAULT_STAGES if s not in self.stages]
        if missing:
            raise ExecutionGraphError(
                f"Execution graph missing required stages: {missing}"
            )

    # ------------------------------------------------------------------
    # Introspection / API
    # ------------------------------------------------------------------

    def list_stages(self) -> List[str]:
        """Return the ordered list of pipeline stages."""
        return list(self.stages)

    def index_of(self, stage: str) -> int:
        """Return the index of a stage in the execution graph."""
        try:
            return self.stages.index(stage)
        except ValueError:
            raise ExecutionGraphError(f"Stage '{stage}' not found in execution graph.")

    def to_dict(self) -> Dict[str, List[str]]:
        """Return a JSON-serializable representation of the graph."""
        return {"stages": self.stages}

    # ------------------------------------------------------------------
    # Modification Utilities
    # ------------------------------------------------------------------

    def add_stage_after(self, stage: str, after: str) -> None:
        """Insert a new stage after a given stage."""
        idx = self.index_of(after)
        self.stages.insert(idx + 1, stage)
        self._validate()

    def add_stage_before(self, stage: str, before: str) -> None:
        """Insert a new stage before a given stage."""
        idx = self.index_of(before)
        self.stages.insert(idx, stage)
        self._validate()

    def remove_stage(self, stage: str) -> None:
        """Remove a stage from the graph."""
        if stage not in self.stages:
            raise ExecutionGraphError(f"Cannot remove stage '{stage}': not present.")
        self.stages.remove(stage)
        self._validate()


__all__ = ["ExecutionGraph", "ExecutionGraphError"]
