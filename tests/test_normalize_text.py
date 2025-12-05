import pytest
from src.utils.normalize_text import normalize_text


# ------------------------------------------------------------
# BASIC TYPE + NONE HANDLING
# ------------------------------------------------------------

def test_none_returns_empty_string():
    assert normalize_text(None) == ""


def test_non_string_values_are_converted_to_string():
    assert normalize_text(123) == "123"
    assert normalize_text(True) == "true"
    assert normalize_text(4.5) == "4.5"


# ------------------------------------------------------------
# WHITESPACE + COLLAPSE BEHAVIOR
# ------------------------------------------------------------

def test_leading_and_trailing_whitespace_removed():
    assert normalize_text("   hello   ") == "hello"


def test_internal_whitespace_collapsed_by_default():
    assert normalize_text("a   b    c") == "a b c"


def test_disable_whitespace_collapse():
    assert normalize_text("a   b    c", collapse_whitespace=False) == "a   b    c"


# ------------------------------------------------------------
# LOWERCASE NORMALIZATION
# ------------------------------------------------------------

def test_default_lowercasing():
    assert normalize_text("HeLLo WorLD") == "hello world"


def test_preserve_case_keeps_original_case():
    assert normalize_text("HeLLo WorLD", preserve_case=True) == "HeLLo WorLD"


# ------------------------------------------------------------
# INVISIBLE + ZERO-WIDTH CHARACTERS
# ------------------------------------------------------------

def test_invisible_characters_are_removed():
    # \u200b is zero-width space
    value = "he\u200bllo"
    assert normalize_text(value) == "hello"


# ------------------------------------------------------------
# UNICODE NORMALIZATION (NFKC)
# ------------------------------------------------------------

def test_unicode_nfkc_normalization():
    # full-width characters -> normal
    full_width = "Ｈｅｌｌｏ　Ｗｏｒｌｄ"  # contains full-width forms and full-width space
    output = normalize_text(full_width)
    assert output == "hello world"  # lowercase & normalized


# ------------------------------------------------------------
# COMBINED COMPLEX CASES
# ------------------------------------------------------------

def test_complex_combination():
    value = "  Héllo\u200b   WORLD   "
    result = normalize_text(value)
    assert result == "hello world"  # unicode normalized, invisible removed, spaces collapsed, lowercased


def test_complex_preserve_case():
    value = "  Héllo\u200b   WORLD   "
    result = normalize_text(value, preserve_case=True)
    assert result == "Héllo WORLD"  # no lowercase applied
