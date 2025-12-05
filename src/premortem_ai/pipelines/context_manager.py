"""
Pipeline context manager for the PreMortem AI system.

The execution context is a controlled state container shared across all
pipeline stages. Its responsibilities include:

- Holding intermediate artifacts (risks, scores, themes, etc.)
- Preserving inputs and outputs in a predictable structure
- Enforcing controlled mutation (no uncontrolled globals)
- Capturing snapshots for audit logs or error reproduction
- Enabling safe, debuggable pipeline execution

This module ensures that each pipeline stage reads/writes state explicitly
and traceably, supporting enterprise-level observability.
"""

from copy import deepcopy
from typing import Dict, Any


class ContextError(Exception):
    """Raised when invalid context operations or mutations occur."""


class PipelineContext:
    """
    A controlled state container for pipeline execution.

    Behavior:
        - All stage outputs must be explicitly written using `set()`
        - All reads occur through `get()`
        - The context enforces predictable keys only
        - Provides snapshotting for audit/debug workflows
    """

    # Allowed context keys (enforced for controlled data flow)
    ALLOWED_KEYS = {
        "project_description",
        "risks",
        "scores",
        "themes",
        "mitigations",
        "summary",
        "report",
        "metadata",
    }

    def __init__(self, project_description: str):
        self._state: Dict[str, Any] = {
            "project_description": project_description
        }

    # ------------------------------------------------------------------
    # State Access
    # ------------------------------------------------------------------

    def get(self, key: str) -> Any:
        """Retrieve a value from the context."""
        if key not in self._state:
            return None
        return self._state[key]

    def set(self, key: str, value: Any) -> None:
        """Write a value into the context (with strict key validation)."""
        if key not in self.ALLOWED_KEYS:
            raise ContextError(f"Invalid context key '{key}'")

        self._state[key] = value

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        """
        Return a deep copy of the full context state.

        Useful for:
            - Logging
            - Debug traces
            - Failure reproduction
            - Governance reporting
        """
        return deepcopy(self._state)

    def keys(self):
        """Return currently-populated context keys."""
        return list(self._state.keys())

    def as_dict(self) -> Dict[str, Any]:
        """Return raw context dictionary (shallow copy)."""
        return dict(self._state)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def assert_populated(self, key: str) -> None:
        """Enforce that required context keys exist before proceeding."""
        if key not in self._state:
            raise ContextError(f"Required context key '{key}' not set.")

    # ------------------------------------------------------------------
    # Reset Utilities
    # ------------------------------------------------------------------

    def reset(self, preserve_description: bool = True) -> None:
        """
        Reset the context to an empty state.

        Args:
            preserve_description (bool):
                If True, retain original project description.
        """
        description = self._state.get("project_description")
        self._state.clear()

        if preserve_description and description:
            self._state["project_description"] = description


__all__ = ["PipelineContext", "ContextError"]
