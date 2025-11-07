from src.llm.agent import stream_agent_response


def main():
    while True:
        user_input = input("You:\t").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!\n")
            break
        thread_id = "interactive_thread"
        print("Model starts streaming...")
        for chunk in stream_agent_response(user_input, thread_id):
            if chunk.step == "model" and chunk.content.type == "text":
                print(f"\nAgent:\t{chunk.content.text}\n")
            elif chunk.content.type == "tool_call":
                print(f"\t- Tool Call:\n\t\t- Tool: {chunk.content.name}\n\t\t- Args: {chunk.content.args}\n")
            elif chunk.step == "tools":
                print(f"\t- Tool Response:\n\t\t- Content: {chunk.content.text}\n")
            else:
                print(f"\t- {chunk.step}:\n\t\t- Content: {chunk.content}\n")

if __name__ == "__main__":
    main()
