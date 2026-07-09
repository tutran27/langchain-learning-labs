from labs.lab05_tools_agents.basic_tools import search_tool, format_print, add, subtract
from labs.lab01_foundation.llm_model import GroqLLMModel

from langchain.agents import create_agent


def build_agent():
    model_wrapper = GroqLLMModel()

    tools = [
        search_tool,
        add,
        subtract,
    ]

    system_prompt = """
You are a tool-using assistant.

Rules:
1. If a relevant tool exists, you MUST call the tool before answering.
2. Do NOT answer from your own knowledge when the request can be handled by a tool.
3. For arithmetic, you MUST use `add` or `subtract`.
4. For web search or factual lookup, you MUST use `search_tool`.
5. If the user explicitly asks to use a tool, you must call that tool.
6. Never skip a tool call just because you think you already know the answer.
7. Only give the final answer after receiving the tool result.
"""

    agent = create_agent(
        model=model_wrapper.groq_chat(),
        tools=tools,
        system_prompt=system_prompt,
    )
    return agent


def print_messages_log(messages):
    print("=================================")
    for index, message in enumerate(messages, start=1):
        print(f"[{index}] {message.__class__.__name__}")
        print(f"content: {message.content}")

        tool_calls = getattr(message, "tool_calls", None)
        if tool_calls:
            print(f"tool_calls: {tool_calls}")

        invalid_tool_calls = getattr(message, "invalid_tool_calls", None)
        if invalid_tool_calls:
            print(f"invalid_tool_calls: {invalid_tool_calls}")

        print("---------------------------------")
    print("=================================")


if __name__ == "__main__":
    agent = build_agent()

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Tìm thông tin của CR7 và cho tôi biết anh ấy sinh năm bao nhiêu?"
            }
        ]
    })

    print_messages_log(result.get("messages", []))
   
