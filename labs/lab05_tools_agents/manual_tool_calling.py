import json

from labs.lab05_tools_agents.basic_tools import search_tool, calculate_tool, is_now, get_weather
from labs.lab01_foundation.llm_model import GroqLLMModel

from langchain.messages import HumanMessage, ToolMessage, SystemMessage


def main():
    llm_wrapper = GroqLLMModel()
    groq_model = llm_wrapper.groq_chat()

    tools = [
        search_tool,
        calculate_tool,
        is_now,
        get_weather
    ]
    # Tạo dict map tool name với tool instance
    tool_map = {tool.name: tool for tool in tools}
    print("=========== SHOW TOOL ============")
    for k, v in tool_map.items():
        print(f"Tool name: {k}")
        print(f"Tool: {v}")
    print("==================================")

    llm_with_tools = groq_model.bind_tools(tools)

    messages = [
        SystemMessage(
            content=(
                "Bạn là trợ lý AI có quyền sử dụng công cụ. "
                "Chỉ gọi công cụ khi thực sự thiếu dữ liệu để trả lời. "
                "Sau khi đã nhận được kết quả từ công cụ, bạn phải dùng chính kết quả đó để trả lời người dùng bằng tiếng Việt. "
                "Không được gọi lại cùng một công cụ nếu kết quả hiện có đã đủ để trả lời. "
                "Nếu trong hội thoại đã có ToolMessage chứa dữ liệu cần thiết, hãy trả lời ngay câu cuối cùng ở dạng văn bản trong content, không tạo thêm tool_calls."
            )
        ),
        HumanMessage(
            content="Thời tiết tại Hà Nội hiện tại thế nào?"
        ),
    ]
    # Invoke llm model
    ai_reponse = llm_with_tools.invoke(messages)
    print("=========== AI Reponse ===========")
    print(ai_reponse)
    print("==================================")

    # Add response to messages
    messages.append(ai_reponse)
    print("================== CHECK MESSAGES =============")
    for m in messages:
        print(f"{m.type}: {m.content}")   # AI trả về tool call, không phải content nên m.content = ''
    print("=============================================")

    # Get tool and arguments
    tool_calls = ai_reponse.additional_kwargs.get("tool_calls")
    for tool_call in tool_calls:
        tool_name = tool_call.get("function").get("name")
        tool_args = tool_call.get("function").get("arguments")
        id = tool_call.get("id")

        print("=========== GET TOOL AND ARGUMENTS ===========")
        print(f"Tool name: {tool_name}")
        print(f"Tool args: {tool_args}")
        print(f"Type of args: {type(tool_args)}")
        print(f"Tool id: {id}")

        tool_selected = tool_map.get(tool_name)
        if tool_selected is None:
            print(f"Tool '{tool_name}' not found")
            continue
        try:
            tool_result = tool_selected.invoke(json.loads(tool_args))
            print("=============== TOOL RESULT ===================")
            print(tool_result)
        except Exception as e:
            print(f"Error calling tool {tool_name}: {e}")
            continue

        # Add tool result to messages
        tool_result_msg = ToolMessage(tool_result,
                                      tool_call_id=id)
        messages.append(tool_result_msg)

    # Run tool again
    ai_reponse = llm_with_tools.invoke(messages)
    print("=========== Final Reponse ===========")
    print(ai_reponse)


if __name__ == "__main__":
    main()
