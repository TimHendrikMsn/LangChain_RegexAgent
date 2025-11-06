import yaml
from pathlib import Path
import re

def load_yaml_prompt(file_path: str) -> str:
    """
    Loads a YAML file describing an agent prompt and returns a formatted string
    containing all sections (description, instructions, etc.).

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        str: Combined string representation suitable for use as a system prompt.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    lines = []
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            section_text = yaml.dump(value, sort_keys=False, allow_unicode=True)
            lines.append(f"## {key}\n{section_text}")
        else:
            lines.append(f"## {key}\n{value}")

    return "\n\n".join(lines)


def flag_value_calculator(flags: list[str]) -> int:
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

def truncate_matches(matches: list[str]) -> tuple[list[str], bool]:
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
    
    return matches, truncated