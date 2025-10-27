from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import ToolCallLimitMiddleware


from src.settings import settings
from src.utils import load_yaml_prompt
from src.tools import  build_regex, run_regex
from src.schemas import  ModelResponseContent, ToolCall, StreamResponse


model = ChatOpenAI(
    model=settings.model_name,
    temperature=settings.temperature,
    max_tokens=settings.max_tokens,
    timeout=settings.timeout,
)

tool_call_limit = ToolCallLimitMiddleware(
    thread_limit=settings.thread_limit,
    run_limit=settings.run_limit,
    exit_behavior="end"
    )

agent = create_agent(
    model=settings.model_name,
    system_prompt=load_yaml_prompt(settings.system_prompt_path),
    tools=[
    ],
    checkpointer=InMemorySaver(), 
    middleware=[tool_call_limit]
    )

     