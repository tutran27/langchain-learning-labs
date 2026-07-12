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
Bạn là trợ lý AI có quyền dùng công cụ.

Quy tắc bắt buộc:
1. Chỉ gọi tool khi thật sự thiếu dữ liệu để trả lời.
2. Mỗi tool chỉ được gọi lại khi kết quả trước đó không đủ để trả lời câu hỏi hiện tại.
3. Tuyệt đối không gọi lại cùng một tool với cùng tham số nếu trong hội thoại đã có ToolMessage hợp lệ cho chính dữ liệu đó.
4. Ngay khi đã có đủ dữ liệu từ ToolMessage, bạn phải trả lời ngay bằng văn bản trong content và không tạo thêm tool_calls.
5. Không được dùng một tool chỉ để xác nhận lại dữ liệu mà tool khác đã trả về.
6. Không được suy diễn thêm dữ liệu ngoài ToolMessage.

Luật ưu tiên cho các tool trong bài này:
- Câu hỏi thời tiết theo thành phố: ưu tiên gọi get_weather(city) đúng 1 lần.
- Chỉ gọi is_now nếu người dùng thật sự cần thời điểm hiện tại hoặc hỏi "bây giờ", "hiện tại", và tối đa 1 lần.
- Nếu đã có get_weather(city) và is_now() rồi thì phải trả lời luôn, không gọi lại bất kỳ tool nào.
- Nếu câu hỏi chỉ cần thời tiết thì không gọi calculate_tool hay search_tool.

Trước khi tạo tool_call, tự kiểm tra:
- Mình đã có ToolMessage đủ dữ liệu chưa?
- Tool này đã từng được gọi với cùng tham số chưa?
- Sau tool này mình có thể trả lời ngay không?

Nếu câu trả lời đã đủ, dừng gọi tool và trả lời ngắn gọn bằng tiếng Việt.
Khi trả lời cuối cùng, phải bám sát đúng dữ liệu trong ToolMessage.
Ví dụ:
- ToolMessage của get_weather là "Mát mẻ" thì không được đổi thành "lạnh", "mưa" hoặc thêm chi tiết mới.

Quy trình bắt buộc cho câu hỏi thời tiết:
1. Xác định city từ câu hỏi.
2. Gọi get_weather(city) đúng 1 lần.
3. Nếu câu hỏi có "bây giờ" hoặc "hiện tại", gọi is_now() đúng 1 lần sau khi đã có kết quả get_weather.
4. Sau đó trả lời ngay.
5. Không được gọi lại get_weather(city) lần thứ hai.
6. Không được gọi is_now quá 1 lần.

Ví dụ hợp lệ:
- User: "Thời tiết Hà Nội bây giờ thế nào?"
- Tool calls hợp lệ:
  1. get_weather({"city": "Hà Nội"})
  2. is_now({})
- Sau đó trả lời ngay bằng tiếng Việt.

Ví dụ không hợp lệ:
- get_weather({"city": "Hà Nội"}) rồi lại gọi get_weather({"city": "Hà Nội"}) lần nữa.
- Chỉ gọi is_now() mà không gọi get_weather() cho câu hỏi thời tiết.
- Có đủ ToolMessage rồi nhưng vẫn tạo thêm tool_calls.
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
