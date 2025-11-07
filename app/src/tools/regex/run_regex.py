import re

def load_document(path: str) -> str:
    with open(path, "rb") as f:
        raw = f.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
        return re.sub(r'[\ud800-\udfff]', '', text)


def flag_value_calculator(flags: list[str]) -> int:
    """Return combined regex flag value from a list of flag characters."""
    flag_value = 0
    if flags:
        flag_map = {
            "I": re.IGNORECASE,
            "M": re.MULTILINE,
            "S": re.DOTALL,
            "X": re.VERBOSE,
        }
        for flag in flags:
            if flag in flag_map:
                flag_value |= flag_map[flag]
    return flag_value

def find_matches(pattern: str, flag_value: int, document) -> tuple[list[str], int]:
    """Find all regex matches in a document and return them with their count."""
    try:
        compiled = re.compile(pattern, flags=flag_value)
    except re.error as e:
        return {"error": f"Invalid regex pattern: {e}", "pattern": pattern}

    matches = [m.group(0) for m in compiled.finditer(document)]
    count = len(matches)
    return matches, count

def truncate_matches(matches: list[str]) -> tuple[list[str], bool]:
    """Truncate long matches and limit list length, returning updated matches and a flag."""
    truncated = False
    if len(matches) <= 15:
        return matches, truncated

    truncated_matches = []
    for match in matches:
        if isinstance(match, str) and len(match) > 100:
            truncated_matches.append(match[:100] + "...")
            truncated = True
        else:
            truncated_matches.append(match)
    matches = truncated_matches

    if len(matches) > 200:
        matches = matches[:200]
    
    return matches, truncated

