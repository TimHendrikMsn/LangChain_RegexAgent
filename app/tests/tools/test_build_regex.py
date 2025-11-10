# tests/test_run_regex_tool.py
from src.tools.tools import build_regex, run_regex
from src.settings import test_settings


def test_invoke_case_insensitive_pattern():
    regex_tuple, flags_tuple = build_regex.invoke(
        {"question": "Match the word 'gloom' in a case-insensitive manner."}
    )
    regex, flags = regex_tuple[1], flags_tuple[1]
    assert isinstance(regex, str)
    assert "I" in flags
    result = run_regex.invoke(
        {
            "pattern": rf"{regex}",
            "match_type": "all",
            "flags": flags,
            "settings": test_settings,
        }
    )
    assert result["count"] == 3


def test_invoke_case_sensitive_pattern():
    regex_tuple, flags_tuple = build_regex.invoke(
        {"question": "Match the word 'gloom'. But only 'gloom' with a lowercase g."}
    )
    regex, flags = regex_tuple[1], flags_tuple[1]
    assert "I" not in flags
    assert isinstance(regex, str)
    result = run_regex.invoke(
        {
            "pattern": rf"{regex}",
            "match_type": "all",
            "flags": flags,
            "settings": test_settings,
        }
    )
    assert result["count"] == 2


def test_match_starting_with_gl():
    regex_tuple, flags_tuple = build_regex.invoke(
        {
            "question": "Create a regex pattern for all words starting with the prefix 'gl'."
        }
    )
    regex, flags = regex_tuple[1], flags_tuple[1]
    assert "I" in flags
    assert isinstance(regex, str)
    result = run_regex.invoke(
        {
            "pattern": rf"{regex}",
            "match_type": "all",
            "flags": flags,
            "settings": test_settings,
        }
    )
    assert result["count"] == 6


def test_invoke_multiple_word_context():
    regex_tuple, flags_tuple = build_regex.invoke(
        {
            "question": "Create a regex pattern for all sentences containing both the word gloom and the word gleam in any order"
        }
    )
    regex, flags = regex_tuple[1], flags_tuple[1]
    result = run_regex.invoke(
        {
            "pattern": rf"{regex}",
            "match_type": "all",
            "flags": flags,
            "settings": test_settings,
        }
    )
    assert "I" in flags
    assert result["count"] == 2
