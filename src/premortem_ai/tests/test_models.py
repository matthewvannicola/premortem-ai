"""
test_models.py

Unit tests for PreMortem AI canonical data models.
Ensures:
    - Pydantic validators behave as expected
    - Normalization logic triggers correctly
    - ID auto-generation works
    - Cross-object reference validation in RiskReport is enforced
"""

import pytest

from premortem_ai.models import (
    RiskItem,
    ScoreItem,
    ThemeItem,
    MitigationItem,
    MitigationAction,
    Summary,
    Metadata,
    RiskReport,
)


# ---------------------------------------------------------------------------
# RiskItem Tests
# ---------------------------------------------------------------------------

def test_risk_item_auto_id_and_normalization():
    item = RiskItem(
        risk_id="",
        title="  Undefined  Ownership  ",
        description=" Example risk description "
    )

    assert item.risk_id.startswith("risk-")
    assert item.title == "undefined ownership"
    assert item.description == "example risk description"


def test_risk_item_invalid_title_short():
    with pytest.raises(ValueError):
        RiskItem(
            risk_id="risk-001",
            title="short",
            description="valid desc"
        )


# ---------------------------------------------------------------------------
# ScoreItem Tests
# ---------------------------------------------------------------------------

def test_score_item_valid_severity():
    score = ScoreItem(
        risk_id="risk-001",
        likelihood=4,
        impact=5,
        severity=20,
    )
    assert score.severity == 20


def test_score_item_invalid_severity():
    with pytest.raises(ValueError):
        ScoreItem(
            risk_id="risk-001",
            likelihood=4,
            impact=5,
            severity=18,  # invalid
        )


# ---------------------------------------------------------------------------
# ThemeItem Tests
# ---------------------------------------------------------------------------

def test_theme_item_auto_id_and_unique_risks():
    theme = ThemeItem(
        theme_id="",
        label="  Operational Risk ",
        risk_ids=["risk-001", "risk-002"]
    )

    assert theme.theme_id.startswith("theme-")
    assert theme.label == "operational risk"


def test_theme_item_duplicate_risks():
    with pytest.raises(ValueError):
        ThemeItem(
            theme_id="theme-123",
            label="Test",
            risk_ids=["risk-001", "risk-001"]
        )


# ---------------------------------------------------------------------------
# MitigationItem Tests
# ---------------------------------------------------------------------------

def test_mitigation_item_auto_id_and_action_normalization():
    mit = MitigationItem(
        mitigation_id="",
        risk_ids=["risk-001"],
        actions=[
            MitigationAction(step=1, action="  Fix API Ownership "),
        ]
    )

    assert mit.mitigation_id.startswith("mitigation-")
    assert mit.actions[0].action == "fix api ownership"


def test_mitigation_item_duplicate_risks():
    with pytest.raises(ValueError):
        MitigationItem(
            mitigation_id="mitigation-001",
            risk_ids=["risk-001", "risk-001"],
            actions=[MitigationAction(step=1, action="test")]
        )


# ---------------------------------------------------------------------------
# Summary Tests
# ---------------------------------------------------------------------------

def test_summary_normalization_and_unique_top_risks():
    summary = Summary(
        health_score=80,
        top_risks=["risk-001", "risk-002"],
        narrative="  Major risks exist ",
        recommendations=[" Improve ownership ", " Add monitoring "]
    )

    assert summary.narrative == "major risks exist"
    assert summary.recommendations == ["improve ownership", "add monitoring"]


def test_summary_duplicate_top_risks():
    with pytest.raises(ValueError):
        Summary(
            health_score=90,
            top_risks=["risk-001", "risk-001"],
            narrative="valid"
        )


# ---------------------------------------------------------------------------
# Metadata Tests
# ---------------------------------------------------------------------------

def test_metadata_auto_timestamp_and_version_normalization():
    md = Metadata.new(
        pipeline_version="1.0.0",
        model_version="gpt-5.1",
        execution_time_ms=150,
    )

    assert md.pipeline_version == "v1.0.0"
    assert md.model_version == "gpt-5.1"
    assert isinstance(md.timestamp_utc, str)


def test_metadata_invalid_timestamp():
    with pytest.raises(ValueError):
        Metadata(
            timestamp_utc="not-a-timestamp",
            pipeline_version="v1",
            model_version="gpt",
            execution_time_ms=10,
        )


# ---------------------------------------------------------------------------
# RiskReport Cross-Reference Tests
# ---------------------------------------------------------------------------

def test_risk_report_cross_reference_validation():
    risks = [
        RiskItem(risk_id="risk-001", title="Valid title here", description="Valid desc"),
    ]
    scores = [
        ScoreItem(risk_id="risk-001", likelihood=4, impact=5, severity=20)
    ]
    themes = [
        ThemeItem(theme_id="theme-001", label="Test", risk_ids=["risk-001"])
    ]
    mitigations = [
        MitigationItem(
            mitigation_id="mitigation-001",
            risk_ids=["risk-001"],
            actions=[MitigationAction(step=1, action="fix")]
        )
    ]
    summary = Summary(
        health_score=80,
        top_risks=["risk-001"],
        narrative="test"
    )
    metadata = Metadata.new("1.0.0", "gpt-5.1", 100)

    report = RiskReport(
        risks=risks,
        scores=scores,
        themes=themes,
        mitigations=mitigations,
        summary=summary,
        metadata=metadata,
    )

    assert isinstance(report, RiskReport)


def test_risk_report_invalid_cross_reference():
    risks = [
        RiskItem(risk_id="risk-001", title="Valid title here", description="Valid desc"),
    ]
    scores = [
        ScoreItem(risk_id="risk-999", likelihood=4, impact=5, severity=20)  # invalid FK
    ]

    with pytest.raises(ValueError):
        RiskReport(
            risks=risks,
            scores=scores,
            themes=[],
            mitigations=[],
            summary=Summary(
                health_score=90,
                top_risks=["risk-001"],
                narrative="test"
            ),
            metadata=Metadata.new("1.0.0", "gpt-5.1", 100),
        )
