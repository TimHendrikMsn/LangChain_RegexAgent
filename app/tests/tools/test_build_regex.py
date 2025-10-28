# tests/test_run_regex_tool.py
from src.tools import build_regex, run_regex
from src.settings import Settings, test_settings



def test_invoke_case_insensitive_pattern():
    regex = build_regex.invoke({"question": "Match the word 'gloom' in a case-insensitive manner.", "flags_hint": "case-insensitive"})
    assert isinstance(regex, str)
    result = run_regex.invoke({"pattern": rf"{regex}", "match_type": "all", "settings": test_settings})
    assert result["count"] == 3

def test_invoke_case_sensitive_pattern():
    regex = build_regex.invoke({"question": "Match the word 'gloom'.", "flags_hint": "case-sensitive"})
    assert isinstance(regex, str)

    result = run_regex.invoke({"pattern": rf"{regex}", "match_type": "all", "settings": test_settings})
    assert result["count"] == 2

def test_match_starting_with_gl():
    regex = build_regex.invoke({"question": "Create a regex pattern for all words starting with the prefix 'gl'.", "flags_hint": "case-insensitive"})
    assert isinstance(regex, str)
    print(f"Generated regex: {regex}")
    result = run_regex.invoke({"pattern": rf"{regex}", "match_type": "all", "settings": test_settings})
    assert result["count"] == 6

def test_invoke_multiple_word_context():
    regex = build_regex.invoke({"question": "Create a regex pattern for all sentences containing both the word gloom and the word gleam in any order", "flags_hint": "case-insensitive"})
    result = run_regex.invoke({"pattern": regex, "match_type": "all", "settings": test_settings})

    assert result["count"] == 2
