import pytest
from src.utils.severity_engine import SeverityEngine


# ------------------------------------------------------------
# BASIC BLENDING BEHAVIOR
# ------------------------------------------------------------

def test_blend_llm_only():
    engine = SeverityEngine()
    data = {"llm_score": 4.0}
    assert engine.compute(data) == pytest.approx(4.0)


def test_blend_human_only():
    engine = SeverityEngine()
    data = {"human_score": 2.5}
    assert engine.compute(data) == pytest.approx(2.5)


def test_blend_both_scores_default_weights():
    engine = SeverityEngine(human_weight=0.4, llm_weight=0.6)
    data = {"human_score": 2, "llm_score": 4}
    # expected = (2 * 0.4/1.0) + (4 * 0.6/1.0)
    expected = (2 * 0.4) + (4 * 0.6)
    assert engine.compute(data) == pytest.approx(expected)


def test_midpoint_when_no_scores():
    engine = SeverityEngine(min_score=1, max_score=5)
    result = engine.compute({})
    assert result == pytest.approx(3.0)  # midpoint


# ------------------------------------------------------------
# PROBABILITY EFFECTS
# ------------------------------------------------------------

def test_probability_adjustment():
    engine = SeverityEngine()
    data = {"llm_score": 4, "probability": 0.8}
    # base = 4
    # expected = 4 * (0.5 + 0.5 * 0.8) = 4 * 0.9 = 3.6
    expected = 4 * (0.5 + 0.5 * 0.8)
    assert engine.compute(data) == pytest.approx(expected)


def test_probability_clamped_high():
    engine = SeverityEngine()
    data = {"llm_score": 4, "probability": 10}  # excessive probability
    p = 1.0
    expected = 4 * (0.5 + 0.5 * p)
    assert engine.compute(data) == pytest.approx(expected)


def test_probability_clamped_low():
    engine = SeverityEngine()
    data = {"llm_score": 4, "probability": -5}
    p = 0.0
    expected = 4 * (0.5 + 0.5 * p)
    assert engine.compute(data) == pytest.approx(expected)


# ------------------------------------------------------------
# IMPACT EFFECTS
# ------------------------------------------------------------

def test_impact_adjustment():
    engine = SeverityEngine()
    data = {"llm_score": 4, "impact": 3}
    # expected = 4 * (1 + 0.1 * 3) = 4 * 1.3 = 5.2 -> clamped to max_score=5
    assert engine.compute(data) == pytest.approx(5.0)


def test_impact_no_clamp_when_disabled():
    engine = SeverityEngine(clamp=False)
    data = {"llm_score": 4, "impact": 3}
    expected = 4 * (1 + 0.1 * 3)  # = 5.2
    assert engine.compute(data) == pytest.approx(expected)


# ------------------------------------------------------------
# COMBINED PROBABILITY + IMPACT
# ------------------------------------------------------------

def test_probability_and_impact_combined():
    engine = SeverityEngine()
    data = {"llm_score": 3, "probability": 0.5, "impact": 2}
    # base = 3
    p_factor = (0.5 + 0.5 * 0.5)     # = 0.75
    i_factor = (1 + 0.1 * 2)         # = 1.2
    expected = 3 * p_factor * i_factor
    expected_clamped = min(expected, engine.max_score)
    assert engine.compute(data) == pytest.approx(expected_clamped)


# ------------------------------------------------------------
# NUMERIC COERCION
# ------------------------------------------------------------

def test_numeric_string_coercion():
    engine = SeverityEngine()
    data = {"llm_score": "4.5", "impact": "2"}
    result = engine.compute(data)
    expected = 4.5 * (1 + 0.1 * 2)     # = 4.5 * 1.2 = 5.4 -> clamped to 5
    assert result == pytest.approx(5.0)


def test_invalid_numeric_values_are_ignored():
    engine = SeverityEngine()
    data = {"llm_score": "INVALID", "human_score": "BAD"}
    # Neither score is numeric -> midpoint fallback
    midpoint = (engine.min_score + engine.max_score) / 2
    assert engine.compute(data) == pytest.approx(midpoint)


# ------------------------------------------------------------
# CLAMPING BEHAVIOR
# ------------------------------------------------------------

def test_clamping_low():
    engine = SeverityEngine(min_score=1, max_score=5)
    data = {"llm_score": -10}
    assert engine.compute(data) == 1


def test_clamping_high():
    engine = SeverityEngine()
    data = {"llm_score": 999}
    assert engine.compute(data) == engine.max_score


def test_disable_clamping():
    engine = SeverityEngine(clamp=False)
    data = {"llm_score": 999}
    assert engine.compute(data) == pytest.approx(999.0)


# ------------------------------------------------------------
# WEIGHT VALIDATION
# ------------------------------------------------------------

def test_negative_weight_raises_error():
    with pytest.raises(ValueError):
        SeverityEngine(human_weight=-1)


def test_zero_total_weight_raises_error():
    with pytest.raises(ValueError):
        SeverityEngine(human_weight=0, llm_weight=0)


# ------------------------------------------------------------
# EDGE CASES
# ------------------------------------------------------------

def test_all_none_values_returns_midpoint():
    engine = SeverityEngine(min_score=1, max_score=5)
    data = {"llm_score": None, "human_score": None}
    assert engine.compute(data) == 3.0


def test_non_numeric_probability_and_impact_are_ignored():
    engine = SeverityEngine()
    data = {"llm_score": 4, "probability": "BAD", "impact": "WRONG"}
    # Both adjustments ignored -> raw score 4 clamped to 4
    assert engine.compute(data) == 4.0
