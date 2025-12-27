"""
Canonical Pydantic v2 data models for the PreMortem AI system.

This module re-exports all public-facing model classes to provide:
  - clean import paths (e.g., from premortem_ai.models import RiskItem)
  - stable, governed public API boundaries
  - deterministic model behavior via CanonicalModel
  - IDE auto-completion + documentation consistency
  - a single source of truth for schema-aligned model definitions
"""

from .base_model import CanonicalModel

from .risk_item import RiskItem
from .score_item import ScoreItem
from .theme_item import ThemeItem
from .mitigation_item import MitigationItem, MitigationAction
from .summary import Summary
from .metadata import Metadata
from .risk_report import RiskReport
from .pipeline_request import PipelineRequest
from .pipeline_response import PipelineResponse


__all__ = [
    "CanonicalModel",
    "Metadata",
    "MitigationAction",
    "MitigationItem",
    "PipelineRequest",
    "PipelineResponse",
    "RiskItem",
    "RiskReport",
    "ScoreItem",
    "Summary",
    "ThemeItem",
]
