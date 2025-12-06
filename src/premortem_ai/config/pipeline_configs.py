"""
pipeline_configs.py

Centralized configuration for PreMortem AI pipeline behavior.

These settings define:
    - default discovery parameters
    - scoring + clustering behavior
    - mitigation generation toggles
    - feature flags for pipeline modules
    - forward-compatible extension points

This file provides a single source of truth for pipeline execution settings
used by:
    - the orchestrator
    - AnalysisService
    - internal processing modules (discovery, scoring, themes, etc.)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineConfig:
    """
    Immutable pipeline configuration object.

    Notes:
        - All values must be serializable and version-safe.
        - Values should be considered part of the public execution contract.
        - Additive-only changes should be made unless pipeline version is bumped.
    """

    # -----------------------------------------------------------
    # Risk Discovery
    # -----------------------------------------------------------
    max_risks_default: int = 50
    enable_risk_filtering: bool = True
    enable_risk_deduplication: bool = True

    # -----------------------------------------------------------
    # Scoring
    # -----------------------------------------------------------
    severity_model: str = "likelihood_impact"   # future: "bayesian", "ml", etc.
    enforce_severity_consistency: bool = True

    # -----------------------------------------------------------
    # Theming / Clustering
    # -----------------------------------------------------------
    enable_theme_clustering: bool = True
    theme_min_group_size: int = 1

    # -----------------------------------------------------------
    # Mitigation Generation
    # -----------------------------------------------------------
    enable_mitigations: bool = True
    max_mitigation_steps: int = 10

    # -----------------------------------------------------------
    # Summary + Narrative
    # -----------------------------------------------------------
    enable_summary_narrative: bool = True
    enable_recommendations: bool = True

    # -----------------------------------------------------------
    # Future expansion
    # -----------------------------------------------------------
    # model_routing_strategy: str = "default"
    # enable_experimental_features: bool = False
    # fallback_model: str = "gpt-4.1"


# Global singleton configuration instance
PIPELINE_CONFIG = PipelineConfig()
