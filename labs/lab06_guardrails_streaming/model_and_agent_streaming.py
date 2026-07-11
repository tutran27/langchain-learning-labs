from labs.lab05_tools_agents.basic_tools import (
    calculate_tool,
    get_weather,
    is_now,
    search_tool,
)
from labs.lab01_foundation.llm_model import GroqLLMModel

from langchain.agents import create_agent


def get_chunk_text(chunk) -> str:
    """Lấy text từ message chunk của nhiều provider khác nhau."""

    text = getattr(chunk, "text", "")
    if isinstance(text, str) and text:
        return text

    content = getattr(chunk, "content", "")
    if isinstance(content, str):
        return content
    return ""


def format_tool_args(args) -> str:
    if not args:
        return "{}"
    return ", ".join(f"{key}={value!r}" for key, value in args.items())


def stream_model(llm) -> None:
    print("\n========== MODEL STREAM ==========\n")

    for chunk in llm.stream("Giải thích streaming trong LangChain trong 3 câu."):
        text = get_chunk_text(chunk)
        if text:
            print(text, end="", flush=True)

    print()


def build_agent(llm):
    tools = [calculate_tool, search_tool, get_weather, is_now]
    system_prompt = """
    Bạn là trợ lý AI có quyền sử dụng công cụ.
    Chỉ gọi công cụ khi thực sự thiếu dữ liệu để trả lời.
    Sau khi đã nhận được kết quả từ công cụ, bạn phải dùng chính kết quả đó để trả lời người dùng bằng tiếng Việt.
    Không được gọi lại cùng một công cụ nếu kết quả hiện có đã đủ để trả lời.
    Nếu trong hội thoại đã có ToolMessage chứa dữ liệu cần thiết, hãy trả lời ngay câu cuối cùng ở dạng văn bản trong content, không tạo thêm tool_calls.
    """
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )


def stream_agent(llm) -> None:
    agent = build_agent(llm)
    query = "Cho tôi biết thời tiết Hà Nội bây giờ như thế nào."
    print("\n========== AGENT STREAM ==========\n")

    for event in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode=["updates", "messages"],
        version="v2",
    ):
        event_type = event.get("type")
        data = event.get("data")

        if event_type == "messages":
            message, _metadata = data
            text = get_chunk_text(message)

            tool_calls = getattr(message, "tool_calls", None) or []
            for tool_call in tool_calls:
                args = format_tool_args(tool_call.get("args"))
                print(f"[GỌI TOOL] {tool_call['name']}({args})")

            if getattr(message, "name", None) and text:
                print(f"[KẾT QUẢ TOOL] {message.name}: {text}")

        elif event_type == "updates":
            for node_name, node_data in data.items():
                messages = node_data.get("messages", [])
                if not messages:
                    continue

                last_message = messages[-1]
                text = get_chunk_text(last_message)
                if text:
                    print(f"[{node_name.upper()} XONG] {text}")


    print("\n========== AGENT STREAM END ==========\n")


if __name__ == "__main__":
    llm = GroqLLMModel().groq_chat()

    # stream_model(llm)

    stream_agent(llm)
