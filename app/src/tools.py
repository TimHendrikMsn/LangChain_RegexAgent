from src.settings import Settings, settings, build_regex_settings
from src.schemas import  RunRegexArgs, BuildRegexArgs, BuildRegexResponse
from src.utils import load_yaml_prompt, flag_value_calculator, truncate_matches
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import re
import os
from typing import List, Literal, Optional, Dict

@tool("build_regex", args_schema=BuildRegexArgs)
def build_regex(question: str) -> BuildRegexResponse:
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
    llm_structured_output = llm.with_structured_output(BuildRegexResponse)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_prompt}"),
            ("user", "{input}"),
        ]
    )
    prompt_input = {
        "system_prompt": load_yaml_prompt(settings.build_regex_tool_prompt_path),
        "input": {"question": question},
    }
    chain = prompt | llm_structured_output
    resp = chain.invoke(prompt_input)

    resp.pattern = resp.pattern.strip().strip("`").strip()
    if resp.pattern.startswith(("r'", 'r"', "'", '"')) and resp.pattern.endswith(("'", '"')):
        resp.pattern = resp.pattern[2:-1] if resp.pattern.startswith("r") else resp.pattern[1:-1]
    return resp


@tool("run_regex", args_schema=RunRegexArgs)
def run_regex(
    pattern: str,
    match_type: Literal["all", "first", "last"] = "all",
    flags: list[Literal["I", "M", "S"]] = [],
    settings: Settings = settings,
) -> dict[str, str]:
    """
    Searches a document for matches to a regex pattern. Returns a match dictionary.
    Supports optional regex flags (I, M, S).
    """
    document = open(settings.document_path, "r", encoding="utf-8").read()
    flag_value = flag_value_calculator(flags)

    try:
        compiled = re.compile(pattern, flags=flag_value)
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

    if matches_needed:
        matches_needed, truncated = truncate_matches(matches_needed)
    else:
        truncated = False

    return {"matches": matches_needed, "count": count, "truncated_matches": truncated}

