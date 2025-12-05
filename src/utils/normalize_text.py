import pytest

from src.scoring.severity_engine import compute_severity


# -------------------------------
# Fixtures
# -------------------------------

@pytest.fixture
def baseline_mapping():
    """
    Expected numeric mapping used by the model:
    Low = 1, Medium = 2, High = 3
    """
    return {"low": 1, "medium": 2, "high": 3}


# -------------------------------
# Severity Calculation Tests
# -------------------------------

def test_low_low_severity(baseline_mapping):
    """Low probability + Low impact should be minimal severity."""
    sev = compute_severity("low", "low")
    assert sev == baseline_mapping["low"] + baseline_mapping["low"] - 1
    assert sev == 1


def test_medium_high_severity(baseline_mapping):
    """Medium probability + High impact should calculate correctly."""
    sev = compute_severity("medium", "high")
    expected = baseline_mapping["medium"] + baseline_mapping["high"] - 1
    assert sev == expected
    assert sev == 4


def test_high_high_severity():
    """High + High should yield the maximum allowed severity of 5."""
    sev = compute_severity("high", "high")
    assert sev == 5


def test_case_insensitivity():
    """Engine should treat 'High', 'HIGH', 'high' the same."""
    sev1 = compute_severity("HIGH", "Medium")
    sev2 = compute_severity("high", "medium")
    assert sev1 == sev2


# -------------------------------
# Error Handling Tests
# -------------------------------

def test_invalid_probability_raises():
    """Unknown probability levels must raise ValueError."""
    with pytest.raises(ValueError):
        compute_severity("sometimes", "high")


def test_invalid_impact_raises():
    """Unknown impact levels must raise ValueError."""
    with pytest.raises(ValueError):
        compute_severity("low", "catastrophic")


# -------------------------------
# Normalization & Safety Tests
# -------------------------------

def test_whitespace_and_extra_spaces():
    """Inputs with extra whitespace should be normalized."""
    sev_clean = compute_severity("low", "high")
    sev_dirty = compute_severity("  low  ", "   high ")
    assert sev_clean == sev_dirty


def test_clamping_never_exceeds_5():
    """Even maximum inputs should not exceed severity 5."""
    sev = compute_severity("high", "high")
    assert sev <= 5


def test_minimum_never_below_1():
    """Even minimum inputs should not drop severity below 1."""
    sev = compute_severity("low", "low")
    assert sev >= 1
