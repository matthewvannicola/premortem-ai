"""
Pipeline orchestrator for the PreMortem AI system.

This module coordinates execution across all structured pipeline stages:
    1. Risk Discovery
    2. Scoring
    3. Theme Clustering
    4. Mitigation Generation
    5. Summary Synthesis
    6. Report Assembly

The orchestrator enforces:
- Ordered execution
- Strict schema validation after each stage
- Model selection governance
- Context propagation across steps
- Deterministic run metadata for auditing
"""

from typing import Dict, Any

from premortem_ai.core.model_selector import select_model
from premortem_ai.core.schema_validation import validate_schema
from premortem_ai.core.id_generation import generate_risk_id, generate_theme_id

from premortem_ai.domains.discovery.extractor import run_discovery
from premortem_ai.domains.scoring.severity_engine import run_scoring
from premortem_ai.domains.themes.theme_clusterer import run_theme_clustering
from premortem_ai.domains.mitigation.mitigation_generator import run_mitigation
from premortem_ai.domains.summary.summary_builder import run_summary
from premortem_ai.domains.reporting.report_builder import assemble_report

from premortem_ai.validation.risk_schema import RISK_SCHEMA
from premortem_ai.validation.scoring_schema import SCORING_SCHEMA
from premortem_ai.validation.themes_schema import THEMES_SCHEMA
from premortem_ai.validation.mitigation_schema import MITIGATION_SCHEMA
from premortem_ai.validation.summary_schema import SUMMARY_SCHEMA


class PipelineExecutionError(Exception):
    """Raised when any pipeline stage fails unexpectedly."""


class PipelineOrchestrator:
    """
    Main controller for PreMortem AI pipeline execution.

    Attributes:
        model (str): Selected LLM inference model.
        run_metadata (dict): Information about the pipeline run for auditing/logging.
    """

    def __init__(self, model: str = None):
        self.model = select_model(model)
        self.run_metadata: Dict[str, Any] = {
            "model": self.model,
            "generated_risks": 0,
            "generated_themes": 0,
        }

    # ----------------------------------------------------------------------
    # Core Pipeline Execution
    # ----------------------------------------------------------------------

    def execute(self, project_description: str) -> Dict[str, Any]:
        """
        Execute all pipeline stages in the required order.

        Args:
            project_description (str): Raw project description from user/system input.

        Returns:
            dict: Pipeline output including risks, scores, themes, mitigations,
            summary, and report metadata.
        """

        try:
            # 1. Risk Discovery -------------------------------------------------
            risks = run_discovery(project_description, model=self.model)
            validate_schema(risks, RISK_SCHEMA, "risk_discovery")

            # Assign IDs if missing
            for r in risks:
                r.setdefault("risk_id", generate_risk_id())

            self.run_metadata["generated_risks"] = len(risks)

            # 2. Scoring --------------------------------------------------------
            scores = run_scoring(risks, model=self.model)
            validate_schema(scores, SCORING_SCHEMA, "scoring")

            # 3. Theme Clustering ----------------------------------------------
            themes = run_theme_clustering(risks, scores, model=self.model)
            validate_schema(themes, THEMES_SCHEMA, "themes")

            for t in themes:
                t.setdefault("theme_id", generate_theme_id())

            self.run_metadata["generated_themes"] = len(themes)

            # 4. Mitigation Generation -----------------------------------------
            mitigations = run_mitigation(risks, themes, model=self.model)
            validate_schema(mitigations, MITIGATION_SCHEMA, "mitigations")

            # 5. Summary Synthesis ---------------------------------------------
            summary = run_summary(risks, scores, themes, mitigations, model=self.model)
            validate_schema(summary, SUMMARY_SCHEMA, "summary")

            # 6. Report Assembly ------------------------------------------------
            report_metadata = assemble_report(
                risks=risks,
                scores=scores,
                themes=themes,
                mitigations=mitigations,
                summary=summary,
                run_metadata=self.run_metadata,
            )

            # Construct final output -------------------------------------------
            return {
                "risks": risks,
                "scores": scores,
                "themes": themes,
                "mitigations": mitigations,
                "summary": summary,
                "report": report_metadata,
                "metadata": self.run_metadata,
            }

        except Exception as exc:
            raise PipelineExecutionError(f"Pipeline failed: {exc}") from exc


__all__ = ["PipelineOrchestrator", "PipelineExecutionError"]
