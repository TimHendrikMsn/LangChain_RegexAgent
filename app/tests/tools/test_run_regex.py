# tests/test_run_regex_tool.py
from src.settings import Settings
from src.tools import run_regex

test_settings = Settings(document_path="data/test_doc.txt")

def test_invoke_all_matches():
    result = run_regex.invoke({"pattern": r"\bgloom\b", "match_type": "all", "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 2
    assert result["matches"] == ["gloom"] * 2
    assert isinstance(result["truncated_matches"], bool)
    assert result["truncated_matches"] is False

def test_invoke_first_match():
    result = run_regex.invoke({"pattern": r"\bgloom\b", "match_type": "first", "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 2
    assert result["matches"] == ["gloom"] * 1
    assert isinstance(result["truncated_matches"], bool)
    assert result["truncated_matches"] is False

def test_invoke_last_match():
    result = run_regex.invoke({"pattern": r"\bgloom\b", "match_type": "last", "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 2
    assert result["matches"] == ["gloom"] * 1
    assert isinstance(result["truncated_matches"], bool)
    assert result["truncated_matches"] is False

def test_invoke_no_matches():
    result = run_regex.invoke({"pattern": r"\bnonexistent\b", "match_type": "all", "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 0
    assert result["matches"] is None
    assert isinstance(result["truncated_matches"], bool)
    assert result["truncated_matches"] is False

def test_invoke_truncated_match():
    result = run_regex.invoke({"pattern": r"[^.!?]*\btruncated\b[^.!?]*", "match_type": "all", "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 1
    assert result["matches"] == ["\nThis\nsplitted line has to be truncated because it is way too long and exceeds the maximum length al..."]
    assert isinstance(result["truncated_matches"], bool)
    assert result["truncated_matches"] is True


# Additional tests for more complex patterns
def test_all_matches_count_and_values():
    result = run_regex.invoke({"pattern": r"\bgl\w*", "match_type": "all", "settings": test_settings})
    assert result["count"] == 4
    assert result["matches"] == ["gloom", "gleam", "gloom", "gleam"]
    assert result["truncated_matches"] is False

def test_invoke_contextual_match():
    pattern = r"(?:\S+\s+){0,2}\bgloom\b(?:\s+\S+){0,2}"
    result = run_regex.invoke({"pattern": pattern, "match_type": "all", "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 2
    assert result["matches"] == [
        "lines mention gloom and gleam.",
        "The word gloom appears as"
    ]
    assert isinstance(result["truncated_matches"], bool)
    assert result["truncated_matches"] is False


def test_invoke_multiple_word_context():
    pattern = r"(?=[^.!?]*\bgloom\b)(?=[^.!?]*\bgleam\b)[^.!?]*"
    result = run_regex.invoke({"pattern": pattern, "match_type": "all", "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 2
    assert result["matches"] == [
        "\nSome lines mention gloom and gleam",
        "\nThe word gloom appears as often as gleam in this document"
    ]
    assert isinstance(result["truncated_matches"], bool)
    assert result["truncated_matches"] is False