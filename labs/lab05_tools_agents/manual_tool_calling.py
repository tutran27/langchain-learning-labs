from labs.lab05_tools_agents.basic_tools import search_tool, calculate_tool, is_now, get_weather
from labs.lab01_foundation.llm_model import GroqLLMModel

from langchain.messages import HumanMessage, ToolMessage, SystemMessage

def main():
    llm_wrapper=GroqLLMModel()
    groq_model=llm_wrapper.groq_chat()
    

    tools=[
        search_tool,
        calculate_tool,
        is_now,
        get_weather
    ]
    # Tạo dict map tool name với tool instance
    tool_map={tool.name: tool for tool in tools}
    print("=========== SHOW TOOL ============")
    for k,v in tool_map.items():
        print(f"Tool name: {k}")
        print(f"Tool type: {type(v)}")
    print("==================================")

    llm_with_tools=groq_model.bind_tools(tools)
    
    messages = [
        SystemMessage(
            content=(
                "Bạn là trợ lý có thể sử dụng công cụ. "
                "Hãy gọi công cụ khi cần và trả lời bằng tiếng Việt."
            )
        ),
        HumanMessage(
            content="Thời tiết tại Hà Nội hiện tại thế nào?"
        ),
    ]
    ai_reponse=llm_with_tools.invoke(messages)
    print("=========== AI Reponse ===========")
    print(ai_reponse)
    print("==================================")

    # Get tool and arguments
    print("=========== GET TOOL AND ARGUMENTS ===========")
    tool_calls = ai_reponse.additional_kwargs.get("tool_calls")[0].get("function")
    tool_name=tool_calls.get("name")
    tool_args=tool_calls.get("arguments")
    print(f"Tool name: {tool_name}")
    print(f"Tool args: {tool_args}")
    print("==============================================")

    tool=tool_map.get(tool_name)
    
if __name__ == "__main__":
    main()
