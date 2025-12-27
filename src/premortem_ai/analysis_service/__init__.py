"""
analysis_service package

Provides the high-level service interface for executing the
PreMortem AI pipeline from API layers, CLIs, or automated workflows.
"""

from .service import AnalysisService

__all__ = ["AnalysisService"]
