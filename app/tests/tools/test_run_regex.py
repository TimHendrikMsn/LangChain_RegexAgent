# tests/test_run_regex_tool.py
from src.settings import Settings
from src.tools.tools import run_regex

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
    assert result["count"] == 20
    assert isinstance(result["truncated_matches"], bool)
    assert result["truncated_matches"] is True
    assert result["matches"][0] == "\nThis\nsplitted line has to be truncated because it is way too long and exceeds the maximum length al..."


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
    pattern = r"(?=.*\bgloom\b)(?=.*\bgleam\b).*?[.!?]"
    result = run_regex.invoke({"pattern": pattern, "match_type": "all", "flags": ["I"], "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 2
    assert result["matches"] == [
        'Some lines mention gloom and gleam.', 
        'The word gloom appears as often as gleam in this document.'
    ]
    assert isinstance(result["truncated_matches"], bool)
    assert result["truncated_matches"] is False


# Test regex with flags
def test_invoke_case_insensitive_flag():
    result = run_regex.invoke({"pattern": r"\bgloom\b", "match_type": "all", "flags": ["I"], "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 3
    assert result["matches"] == ["gloom", "Gloom", "gloom"]

    result_no_flag = run_regex.invoke({"pattern": r"\bgloom\b", "match_type": "all", "settings": test_settings})
    assert isinstance(result_no_flag, dict)
    assert result_no_flag["count"] == 2
    assert result_no_flag["matches"] == ["gloom", "gloom"]

def test_invoke_multiline_flag():
    result = run_regex.invoke({"pattern": r"^Some", "match_type": "all", "flags": ["M"], "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 1
    assert result["matches"] == ["Some"]

    result_no_flag = run_regex.invoke({"pattern": r"^Some", "match_type": "all", "settings": test_settings})
    assert isinstance(result_no_flag, dict)
    assert result_no_flag["count"] == 0
    assert result_no_flag["matches"] is None


def test_invoke_dotall_flag():
    result = run_regex.invoke({"pattern": r"This.splitted", "match_type": "all", "flags": ["S"], "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 1
    assert result["matches"] == ["This\nsplitted"]

    result_no_flag = run_regex.invoke({"pattern": r"This.splitted", "match_type": "all", "settings": test_settings})
    assert isinstance(result_no_flag, dict)
    assert result_no_flag["count"] == 0

    result_no_flag = run_regex.invoke({"pattern": r"This splitted", "match_type": "all", "settings": test_settings})
    assert isinstance(result_no_flag, dict)
    assert result_no_flag["count"] == 0

def test_invoke_multiple_flags():
    result = run_regex.invoke({"pattern": r"^This.*CONTAINS", "match_type": "all", "flags": ["I", "S"], "settings": test_settings})
    assert isinstance(result, dict)
    assert result["count"] == 1
    assert result["matches"] == ["This is a test document.\nIt contains"]

    result_no_flags = run_regex.invoke({"pattern": r"This.*CONTAINS", "match_type": "all", "settings": test_settings})
    assert isinstance(result_no_flags, dict)
    assert result_no_flags["count"] == 0
