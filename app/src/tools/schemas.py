from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from src.settings import Settings
 
class RunRegexArgs(BaseModel):
    """Schema for the regex pattern."""
    pattern: str = Field(..., description="The regex pattern to be used for matching.")
    match_type: Literal["all", "first", "last"] = Field(
        "all",
        description="The type of match to perform. 'all' returns all matches, 'first'")
    flags: List[Literal["I", "M", "S"]] = Field(
        default_factory=list,
        description=(
            "Optional list of regex flags to modify matching behavior. "
            "Available flags: IGNORECASE (I), MULTILINE (M), DOTALL (S)."
        )
    )
    settings: Optional[Settings] = None

class BuildRegexArgs(BaseModel):
    question: str = Field(
        ...,
        description="Natural-language description of the pattern to match. "
                    "Include any constraints like anchors, groups, flags, etc."
    )

class BuildRegexResponse(BaseModel):
    pattern: str = Field(..., description="The generated regex pattern string.")
    flags: List[Literal["I", "M", "S"]] = Field(
        default_factory=list,
        description=(
            "List of regex flags inferred from the question. "
            "Available flags: IGNORECASE (I), MULTILINE (M), DOTALL (S)."
        )
    )
class RunRagArgs(BaseModel):
    query: str = Field(
        ...,
        description="The user's natural language query to be answered using RAG.",
    )
    k: int = Field(..., ge=1, le=10, description="Number of top chunks to retrieve (1–10).")
