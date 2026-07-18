from langchain.agents import create_agent
from langchain.messages import AIMessage,HumanMessage,SystemMessage, ToolMessage

from labs.lab01_foundation.llm_model import GroqLLMModel

from labs.lab06_guardrails_streaming.human_approval.fake_db import get_order_info, reset_demo_data
from labs.lab06_guardrails_streaming.human_approval.utils import (evaluate_refund, 
    review_refund,
    serialize_tool_result,
)

from labs.lab06_guardrails_streaming.human_approval.tool_registry import (
    TOOLS_BY_NAME,
    TOOLS,
    SENSITIVE_TOOLS,
    get_order_info,
    check_refund_eligible,
    issue_refund,
)

from labs.lab06_guardrails_streaming.human_approval.prompt import SYSTEM_PROMPT


def run_refund_agent(
    user_input: str,
    max_iterations: int = 6,
) -> str:
    llm = GroqLLMModel().groq_chat()
    model_with_tools=llm.bind_tools(tools=TOOLS)
    
    messages=[
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_input),
    ]

    rejected_tools: set[str] = set()

    for t in range(max_iterations):
        print(f"======== Iteration {t+1} ========\n")
        ai_message=model_with_tools.invoke(messages)
        messages.append(ai_message)
        print(f"🤖AI Message: {ai_message}\n")

        if not ai_message.tool_calls:
            return str(ai_message.content)

        tool_calls=ai_message.tool_calls
        print(f"🤖Tool Calls: {tool_calls}\n")

        for tc in tool_calls:
            name=tc.get("name")
            args=tc.get("args")
            id=tc.get("id")
            
            print("======= TOOL INFOMATION ========")
            print(f"Tên tool: {name}")
            print(f"Tham số: {args}")
            print(f"ID: {id}\n")
            selected_tool=TOOLS_BY_NAME.get(name)
            
            # 1. Tool không tồn tại
            if selected_tool is None:
                result = {
                    "success": False,
                    "message": (
                        f"Tool '{name}' không tồn tại."
                    ),
                }

            # 2. Tool bị con người từ chối
            elif name in rejected_tools:
                result = {
                    "success": False,
                    "status": "rejected_by_human",
                    "message": (
                        "Con người đã từ chối tool này. "
                        "Không được gọi lại."
                    ),
                }

            # 3. Tool nhạy cảm -> Yêu cầu phê duyệt
            elif name in SENSITIVE_TOOLS:
                action, args=review_refund(args)
                print("======= REVIEW REFUND =======")
                print(f"Hành động: {action}")
                print(f"Tham số: {args}\n")

                if action=="reject":
                    rejected_tools.add(name)
                    result={
                        "success":False,
                        "status":"rejected_by_human",
                        "message":"Đã từ chối yêu cầu"
                    }
                else:
                    try:
                        result=selected_tool.invoke(args)
                    except Exception as e:
                        result={
                            "success":False,
                            "message": f"❌ Lỗi khi gọi tool {name}: {str(e)}"
                        }

            # 4. Tool an toàn
            else:
                try:
                    result=selected_tool.invoke(args)
                except Exception as e:
                    result={
                        "success":False,
                        "message": f"❌ Lỗi khi gọi tool {name}: {str(e)}"
                    }

            print(f"[TOOL RESULT] {result}")
            messages.append(
                ToolMessage(
                    content=serialize_tool_result(result),
                    tool_call_id=id,
                )
            )
    return "Agent vượt quá số vòng xử lý cho phép."        
def run() -> None:
    reset_demo_data()

    query = (
        "Khách hàng yêu cầu hoàn toàn bộ tiền cho đơn "
        "ORD-1001 vì bàn phím bị lỗi ngay khi nhận hàng. "
        "Hãy kiểm tra và xử lý yêu cầu."
    )

    final_answer = run_refund_agent(query)

    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(final_answer)

    # print("\nREFUND LOG")
    # print(REFUND_LOG)


if __name__ == "__main__":
    run()