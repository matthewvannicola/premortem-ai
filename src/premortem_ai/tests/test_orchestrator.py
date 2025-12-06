"""
test_orchestrator.py

Unit tests for the Orchestrator — the core engine that glues together
LLM discovery, scoring, theming, mitigation, and summarization.

These tests:
    - mock LLM responses for each stage
    - validate correct orchestration order
    - ensure parsed JSON outputs produce canonical model objects
    - verify failure behavior on malformed LLM output
    - check early exit logic for empty discovery
"""

import pytest
from unittest.mock import MagicMock

from premortem_ai.orchestrator import Orchestrator
from premortem_ai.models import (
    PipelineRequest,
    RiskReport,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_llm():
    """Mock LLM client that simulates responses for each orchestrator stage."""
    mock = MagicMock()

    mock.run.side_effect = [
        # ---- Discovery ----
        """
        {
          "risks": [
            {
              "risk_id": "risk-001",
              "title": "unclear ownership",
              "description": "no explicit API owner"
            }
          ]
        }
        """,

        # ---- Scoring ----
        """
        {
          "scores": [
            {
              "risk_id": "risk-001",
              "likelihood": 3,
              "impact": 5,
              "severity": 15
            }
          ]
        }
        """,

        # ---- Themes ----
        """
        {
          "themes": [
            {
              "theme_id": "theme-001",
              "label": "Operational Gaps",
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
                {"step": 1, "action": "assign API owner"}
              ]
            }
          ]
        }
        """,

        # ---- Summary ----
        """
        {
          "summary": {
            "health_score": 70,
            "top_risks": ["risk-001"],
            "narrative": "Ownership ambiguity poses delivery challenges"
          }
        }
        """
    ]

    return mock


@pytest.fixture
def orchestrator(mock_llm):
    """Inject the mock LLM client into the orchestrator (DI pattern)."""
    return Orchestrator(llm_client=mock_llm)


# ---------------------------------------------------------------------------
# CORE ORCHESTRATION TEST
# ---------------------------------------------------------------------------

def test_orchestrator_full_pipeline(orchestrator):
    """
    Ensures:
        - orchestrator runs through all stages
        - output is a valid RiskReport
        - cross-stage references remain consistent
        - correct number of LLM calls occur
    """

    req = PipelineRequest(project_description="We have no API owner.")

    report = orchestrator.run_pipeline(req)

    assert isinstance(report, RiskReport)

    # Basic shape checks
    assert len(report.risks) == 1
    assert len(report.scores) == 1
    assert len(report.themes) == 1
    assert len(report.mitigations) == 1

    # Cross-reference validation
    rid = report.risks[0].risk_id
    assert report.scores[0].risk_id == rid
    assert rid in report.themes[0].risk_ids
    assert rid in report.mitigations[0].risk_ids

    # LLM invoked exactly 5 times
    assert orchestrator.llm_client.run.call_count == 5


# ---------------------------------------------------------------------------
# MALFORMED LLM OUTPUT TEST
# ---------------------------------------------------------------------------

def test_orchestrator_invalid_llm_output(orchestrator, mock_llm):
    """If LLM returns invalid JSON, orchestrator must raise."""
    mock_llm.run.side_effect = ['{ BAD JSON }']  # First stage breaks

    req = PipelineRequest(project_description="broken test")

    with pytest.raises(Exception):
        orchestrator.run_pipeline(req)


# ---------------------------------------------------------------------------
# EMPTY DISCOVERY TEST
# ---------------------------------------------------------------------------

def test_orchestrator_empty_discovery(orchestrator, mock_llm):
    """
    If discovery returns no risks:
        - orchestrator should stop early
        - scores/themes/mitigations should all be empty
        - summary.health_score should default to 0
    """

    mock_llm.run.side_effect = ['{ "risks": [] }']

    req = PipelineRequest(project_description="no risks exist")

    report = orchestrator.run_pipeline(req)

    assert report.risks == []
    assert report.scores == []
    assert report.themes == []
    assert report.mitigations == []
    assert report.summary.health_score == 0


# ---------------------------------------------------------------------------
# MODEL OVERRIDE ROUTING TEST
# ---------------------------------------------------------------------------

def test_orchestrator_respects_model_override(orchestrator, mock_llm):
    """
    Ensures that PipelineRequest.model_version_override is supplied
    to the model router and then to the LLM client.
    """

    req = PipelineRequest(
        project_description="override model test",
        model_version_override="gpt-4.1"
    )

    orchestrator.run_pipeline(req)

    # Model override must be passed to all five LLM calls
    # Ensures orchestrator → model_router → llm_client → run() chain is correct.
    for call in mock_llm.run.call_args_list:
        args, kwargs = call
        # All calls must include model_override in kwargs
        assert "model_override" in kwargs
        assert kwargs["model_override"] == "gpt-4.1"
