from src.settings import Settings, settings, build_regex_settings
from src.schemas import  RunRegexArgs, BuildRegexArgs
from src.utils import load_yaml_prompt
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import re
import os
from typing import List, Literal, Optional, Dict

@tool("build_regex", args_schema=BuildRegexArgs)
def build_regex(question: str, flags_hint: Optional[str] = None) -> str:
    """
    Use an LLM to produce a Python-compatible regex pattern string ONLY.
    Returns the raw regex pattern (no code fences, no quotes).
    Optionally considers a flags hint but does not include flags syntax—just the pattern.
    """ 
    
    llm = ChatOpenAI(
        model=build_regex_settings.model_name,
        temperature=build_regex_settings.temperature,
        max_tokens=build_regex_settings.max_tokens,
        )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_prompt}"),
            ("human", "{input}"),
        ]
    )

    prompt_input = {
        "input": question if not flags_hint else f"{question}\nFlags hint: {flags_hint}",
        "system_prompt": load_yaml_prompt(settings.build_regex_tool_prompt_path)
    }

    chain = prompt | llm
    resp = chain.invoke(prompt_input)

    pattern = resp.content.strip().strip("`").strip()

    if pattern.startswith(("r'", 'r"', "'", '"')) and pattern.endswith(("'", '"')):
        pattern = pattern[2:-1] if pattern.startswith("r") else pattern[1:-1]
    return pattern


@tool("run_regex", args_schema=RunRegexArgs)
def run_regex(
    pattern: str,
    match_type: Literal["all", "first", "last"] = "all",
    settings: Settings = settings,
) -> dict[str, str]:
    """
    Searches a document for matches to a regex pattern. Returns a match dictionary.
    """
    document = open(settings.document_path, "r", encoding="utf-8").read()
    try:
        compiled = re.compile(pattern)
    except re.error as e:
        return {"error": f"Invalid regex pattern: {e}", "pattern": pattern}

    matches = [m.group(0) for m in compiled.finditer(document)]

    count = len(matches)

    if count == 0:
        matches_needed = None
    else:
        if match_type == "first":
            matches_needed = [matches[0]]
        elif match_type == "last":
            matches_needed = [matches[-1]]
        else:
            matches_needed = matches

    truncated = False
    if matches_needed:
        truncated_matches = []
        for match in matches_needed:
            if isinstance(match, str) and len(match) > 100:
                truncated_matches.append(match[:100] + "...")
                truncated = True
            else:
                truncated_matches.append(match)
        matches_needed = truncated_matches

    return {"matches": matches_needed, "count": count, "truncated_matches": truncated}

