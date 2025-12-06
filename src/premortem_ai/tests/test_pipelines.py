"""
test_pipelines.py

End-to-end pipeline tests for PreMortem AI — using dependency injection +
mocked LLM behavior. These tests validate the orchestrator-level execution
flow WITHOUT relying on external systems like OpenAI.

Goals:
    - Ensure pipeline processes LLM outputs correctly
    - Validate correct construction of RiskReport
    - Confirm orchestrator calls expected components in correct order
    - Verify cross-stage data contracts remain consistent

These tests are intentionally lightweight so they run fast in CI.
"""

import pytest
from unittest.mock import MagicMock

from premortem_ai.analysis_service import AnalysisService
from premortem_ai.models import PipelineRequest, RiskReport


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_llm_client():
    """
    Create a mock LLM client that simulates LLM responses for:
        - risk discovery
        - scoring
        - theme clustering
        - mitigation generation
        - summary generation

    Each return value mirrors what your orchestrator expects structurally.
    """
    mock = MagicMock()

    # Simulated responses for each phase
    mock.run.side_effect = [
        # ---- Discovery Output ----
        """
        {
          "risks": [
            {
              "risk_id": "risk-001",
              "title": "ownership gaps",
              "description": "no clear API owner"
            }
          ]
        }
        """,

        # ---- Scoring Output ----
        """
        {
          "scores": [
            {
              "risk_id": "risk-001",
              "likelihood": 4,
              "impact": 5,
              "severity": 20
            }
          ]
        }
        """,

        # ---- Theme Clustering ----
        """
        {
          "themes": [
            {
              "theme_id": "theme-001",
              "label": "Operational Risk",
              "risk_ids": ["risk-001"]
            }
          ]
        }
        """,

        # ---- Mitigations ----
        """
        {
          "mitigations": [
            {
              "mitigation_id": "mitigation-001",
              "risk_ids": ["risk-001"],
              "actions": [
                {"step": 1, "action": "Define an API owner"}
              ]
            }
          ]
        }
        """,

        # ---- Summary Generation ----
        """
        {
          "summary": {
            "health_score": 72,
            "top_risks": ["risk-001"],
            "narrative": "Project exhibits ownership uncertainty"
          }
        }
        """
    ]

    return mock


@pytest.fixture
def service(mock_llm_client):
    """Inject mock LLM client into AnalysisService (DI pattern)."""
    return AnalysisService(llm_client=mock_llm_client)


# ---------------------------------------------------------------------------
# Full Pipeline Test
# ---------------------------------------------------------------------------

def test_pipeline_end_to_end(service):
    """
    Validates:
        - All pipeline stages execute in correct order
        - A full RiskReport is produced
        - Cross-stage references remain consistent
        - LLM is invoked correct number of times
    """

    req = PipelineRequest(
        project_description="We have no clear API owner",
        max_risks=10,
        include_metadata=True
    )

    response = service.run_analysis(req)

    # Should return structured PipelineResponse
    assert hasattr(response, "report")
    assert isinstance(response.report, RiskReport)

    report = response.report

    # ---- Validate shape ----
    assert len(report.risks) == 1
    assert len(report.scores) == 1
    assert len(report.themes) == 1
    assert len(report.mitigations) == 1

    # ---- Validate cross-reference integrity ----
    assert report.scores[0].risk_id == report.risks[0].risk_id
    assert report.themes[0].risk_ids[0] == report.risks[0].risk_id
    assert report.mitigations[0].risk_ids[0] == report.risks[0].risk_id

    # ---- Validate summary ----
    assert report.summary.health_score == 72
    assert report.summary.top_risks == ["risk-001"]

    # ---- Validate LLM was called exactly 5 times ----
    # discovery → scoring → themes → mitigation → summary
    assert service.llm_client.run.call_count == 5


# ---------------------------------------------------------------------------
# Pipeline Failure Tests
# ---------------------------------------------------------------------------

def test_pipeline_invalid_llm_output(service, mock_llm_client):
    """
    If an LLM returns malformed JSON or invalid structure,
    the orchestrator should raise an appropriate error.
    """

    # Mock one stage returning broken JSON
    mock_llm_client.run.side_effect = ['{ INVALID JSON }']

    req = PipelineRequest(
        project_description="broken test",
        include_metadata=False
    )

    with pytest.raises(Exception):
        service.run_analysis(req)


def test_pipeline_handles_empty_discovery(service, mock_llm_client):
    """
    If discovery returns zero risks, pipeline should NOT proceed through the
    rest of the stages — this tests correct early-exit behavior.
    """

    mock_llm_client.run.side_effect = [
        '{ "risks": [] }'
    ]

    req = PipelineRequest(project_description="empty discovery")

    response = service.run_analysis(req)

    # Should return *empty* RiskReport but still valid
    assert response.report.risks == []
    assert response.report.scores == []
    assert response.report.themes == []
    assert response.report.mitigations == []
    assert response.report.summary.health_score == 0
