from pydantic import BaseModel, Field
from typing import Optional, Literal, Union
from src.settings import Settings

# Schemas for tool arguments
 
class RunRegexArgs(BaseModel):
    """Schema for the regex pattern."""
    pattern: str = Field(..., description="The regex pattern to be used for matching.")
    match_type: Literal["all", "first", "last"] = Field(
        "all",
        description="The type of match to perform. 'all' returns all matches, 'first'")
    settings: Settings

class BuildRegexArgs(BaseModel):
    question: str = Field(
        ...,
        description="Natural-language description of the pattern to match. "
                    "Include any constraints like anchors, groups, flags, etc."
    )
    flags_hint: Optional[str] = Field(
        default=None,
        description="Optional hint for flags (e.g., 'case-insensitive', 'multiline')."
    )

# Schema for agent responses
class ToolCall(BaseModel):
    type: Literal["tool_call"] = "tool_call"
    name: Literal["build_regex", "run_regex"]
    args: Union[BuildRegexArgs, RunRegexArgs]
    id: Optional[str] = None

class ModelResponseContent(BaseModel):
    type: str = "text"
    text: Optional[str] = None

class StreamResponse(BaseModel):
    step: str
    content: Optional[ModelResponseContent | ToolCall] = None