"""
Public pipeline API.

Recommended usage:
    from premortem_ai.pipelines import run_pipeline
"""

from .orchestrator import run_pipeline

__all__ = ["run_pipeline"]
