from pydantic import BaseModel
from typing import Optional, Literal, Union
from src.tools.schemas import BuildRegexArgs, RunRegexArgs, RunRagArgs

class ToolCall(BaseModel):
    type: Literal["tool_call"] = "tool_call"
    name: Literal["build_regex", "run_regex", "run_rag"]
    args: Union[BuildRegexArgs, RunRegexArgs, RunRagArgs]
    id: Optional[str] = None

class ModelResponseContent(BaseModel):
    type: str = "text"
    text: Optional[str] = None

class StreamResponse(BaseModel):
    step: str
    content: Optional[ModelResponseContent | ToolCall] = None