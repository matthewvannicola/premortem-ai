"""
Analysis Service Package

Provides the high-level execution interface for running a full PreMortem AI
analysis. The service layer wraps the orchestrator, enforces stable input/output
contracts, and exposes a clean boundary for API, CLI, and SDK consumers.

Public Exports:
    - AnalysisService
"""

from .service import AnalysisService

__all__ = [
    "AnalysisService",
]
