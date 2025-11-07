from src.settings import Settings
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Optional, Type, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence


def init_llm(settings: Settings, response_schema: Optional[Type[BaseModel]] = None) -> ChatOpenAI:
    """
    Initialize a ChatOpenAI instance with the provided settings.
    If a Pydantic response schema is provided, returns the model configured for structured output based on that schema.
    """
    llm = ChatOpenAI(
        model=settings.model_name,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
    )
    if response_schema:
        return llm.with_structured_output(response_schema)
    return llm

def create_chain(llm: ChatOpenAI) -> RunnableSequence:
    """Creates a prompt chain that can be invoked."""
    prompt_schema = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_prompt}"),
            ("user", "{input}"),
        ]
    )
    chain = prompt_schema | llm
    return chain

def invoke_chain(chain: RunnableSequence, system_prompt: str, user_input: str):
    """Invokes the prompt chain with the provided system prompt and user input."""
    prompt_input = {
        "system_prompt": system_prompt,
        "input": {"question": user_input}
        }
    response = chain.invoke(prompt_input)
    return response
