from src.settings import Settings, settings, build_regex_settings
from src.tools.schemas import  RunRegexArgs, BuildRegexArgs, BuildRegexResponse, RunRagArgs
from src.utils import load_yaml_prompt
from src.llm.llm import init_llm, create_chain, invoke_chain
from src.tools.rag.rag import load_database, most_relevant_k_chunks
from src.tools.regex.run_regex import  load_document, flag_value_calculator, truncate_matches, find_matches
from src.tools.regex.build_regex import process_regex_pattern
from langchain.tools import tool
from typing import Literal

@tool("build_regex", args_schema=BuildRegexArgs)
def build_regex(question: str) -> BuildRegexResponse:
    """
    Use an LLM to produce a Python-compatible regex pattern string ONLY.
    Returns the raw regex pattern (no code fences, no quotes).
    Optionally considers a flags hint but does not include flags syntax—just the pattern.
    """ 
    
    llm = init_llm(settings=build_regex_settings, response_schema=BuildRegexResponse)
    chain = create_chain(llm)
    response = invoke_chain(
        chain = chain,
        system_prompt=load_yaml_prompt(settings.build_regex_tool_prompt_path),
        user_input=question
    )
    response.pattern = process_regex_pattern(response.pattern)
    
    return response


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
    document = load_document(settings.document_path)
    flag_value = flag_value_calculator(flags)
    matches, count = find_matches(pattern, flag_value, document)
    
    if count == 0:
        return {"matches": None, "count": count, "truncated_matches": False}

    if match_type == "first":
        selected = matches[:1]
        truncated = False
    elif match_type == "last":
        selected = matches[-1:]
        truncated = False
    else:
        selected, truncated = truncate_matches(matches)
    return {"matches": selected, "count": count, "truncated_matches": truncated}


@tool("run_rag", args_schema=RunRagArgs)
def run_rag(query: str, k: int) -> str:
    """
    Executes a Retrieval-Augmented Generation (RAG) query using the configured retrieval and LLM settings.
    Takes a natural language question, retrieves the most relevant context from the document or vector store,
    and generates a synthesized, context-aware response.

    Returns a structured response containing the generated answer and optionally the retrieved context data.
    """
    db = load_database(path=settings.chroma_path)
    text = most_relevant_k_chunks(query, db, k)
    return text


    