from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import (
    ToolCallLimitMiddleware,
    ContextEditingMiddleware,
    ClearToolUsesEdit,
)


from src.settings import settings
from src.utils import load_yaml_prompt
from src.tools.tools import build_regex, run_regex, run_rag
from src.llm.schemas import ModelResponseContent, ToolCall, StreamResponse


model = ChatOpenAI(
    model=settings.model_name,
    temperature=settings.temperature,
    max_tokens=settings.max_tokens,
    timeout=settings.timeout,
)

tool_call_limit = ToolCallLimitMiddleware(
    thread_limit=settings.thread_limit,
    run_limit=settings.run_limit,
    exit_behavior="end",
)
context_limit = ContextEditingMiddleware(
    edits=[ClearToolUsesEdit(trigger=200)],
)

agent = create_agent(
    model=model,
    system_prompt=load_yaml_prompt(settings.system_prompt_path),
    tools=[build_regex, run_regex, run_rag],
    checkpointer=InMemorySaver(),
    middleware=[tool_call_limit, context_limit],
)


def stream_agent_response(user_input: str, thread_id: str):
    try:
        for chunk in agent.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            stream_mode="updates",
            config={"thread_id": thread_id},
        ):
            for step, data in chunk.items():
                if "Middleware" in step:
                    if data and data.get("jump_to", None) == "end":
                        yield StreamResponse(
                            step=step,
                            content=ModelResponseContent(
                                type="text",
                                text="Tool call limits exceeded: Start a new thread.",
                            ),
                        )
                        return
                    continue

                content_blocks = data["messages"][-1].content_blocks
                if content_blocks and content_blocks[0]["type"] == "tool_call":
                    tool_call_data = content_blocks[0]
                    content = ToolCall(
                        type="tool_call",
                        name=tool_call_data.get("name"),
                        args=tool_call_data.get("args"),
                        id=tool_call_data.get("id"),
                    )
                else:
                    content = ModelResponseContent(
                        type="text",
                        text=content_blocks[0].get("text") if content_blocks else None,
                    )

                yield StreamResponse(step=step, content=content)

    except Exception as e:
        raise e
