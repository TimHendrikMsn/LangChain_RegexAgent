# settings.py
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Configuration for the AI Agent and supporting tools.
    Loads environment variables from `.env` or system environment.
    """
    # --- Model Settings ---
    model_name: str = Field(
        default="gpt-4.1-mini",
        description="Name of the model to use for the agent"
    )
    temperature: float = Field(
        default=0.1,
        description="Sampling temperature for model output"
    )
    max_tokens: int = Field(
        default=2000,
        description="Maximum number of tokens to generate in responses"
    )
    timeout: int = Field(
        default=30,
        description="Request timeout for the model in seconds"
    )

    # --- Paths ---
    system_prompt_path: str = Field(
        default="src/prompts/system_prompt.yaml",
        description="Path to the system prompt YAML file"
    )
    build_regex_tool_prompt_path: str = Field(
        default="src/prompts/build_regex_tool_prompt.yaml",
        description="Path to the build_regex tool prompt YAML file"
    )
    document_path: str = Field(
        default="data/document.txt",
        description="Path to the document to be processed"
    )
    chroma_path: str = Field(
        default="chroma",
        description="Path to the chroma database"
    )

    # --- Middleware Settings ---
    thread_limit: int = Field(
        default=10,
        description="Maximum tool calls across all runs in a thread"
    )
    run_limit: int = Field(
        default=6,
        description="Maximum tool calls per single invocation"
    )

    # --- RAG_settings ---
    chunk_size: int = Field(
        default=1000,
        description="Number of letters per chunk after splitting a document"
    )

    chunk_overlap: int = Field(
        default=100,
        description="Number of letters of overlap between chunk after splitting a document"
    )



# Instantiate global settings object
settings = Settings()
build_regex_settings = Settings(
    model_name="gpt-4.1-mini",
    temperature=0.5,
    max_tokens=20000,
)
test_settings = Settings(document_path="data/test_doc.txt")