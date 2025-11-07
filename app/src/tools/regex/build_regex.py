
def process_regex_pattern(regex: str) -> str:
    """Cleans a regex string by removing quotes, backticks, and raw-string prefixes."""
    regex = regex.strip().strip("`").strip()
    if regex.startswith(("r'", 'r"', "'", '"')) and regex.endswith(("'", '"')):
        regex = regex[2:-1] if regex.startswith("r") else regex[1:-1]
    return regex