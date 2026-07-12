from langchain.agents import create_agent
from langchain.agents.middleware import ToolRetryMiddleware
from langchain.tools import tool

from labs.lab01_foundation.llm_model import GroqLLMModel


attempt_state = {
    "count": 0,
}


@tool
def unstable_search(query: str) -> str:
    """Tìm kiếm dữ liệu từ API có thể tạm thời mất kết nối."""

    attempt_state["count"] += 1
    current_attempt = attempt_state["count"]

    print(f"[TOOL] Lần gọi thứ {current_attempt}")

    if current_attempt < 3:
        raise ConnectionError(
            f"API tạm thời không phản hồi ở lần {current_attempt}"
        )

    return f"Kết quả tìm kiếm thành công cho: {query}"

def build_agent():
    llm = GroqLLMModel().groq_chat()

    return create_agent(
    model=llm,
    tools=[unstable_search],
    middleware=[
        ToolRetryMiddleware(
            tools=["unstable_search"],
            max_retries=2,
            retry_on=(ConnectionError,),
            initial_delay=0.2,
            backoff_factor=1.0,
            jitter=False,
            on_failure="raise",
        )
    ],
    system_prompt=(
        "Bạn là trợ lý tìm kiếm. "
        "Bắt buộc gọi unstable_search đúng một lần "
        "để trả lời yêu cầu tìm kiếm."
    ),
)


def run(query: str) -> None:
    agent = build_agent()
    attempt_state["count"] = 0

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        }
    )

    print("\n========== FINAL ==========")
    print(result["messages"][-1].content)

    print(
        "\nTổng số lần thực thi tool:",
        attempt_state["count"],
    )


if __name__ == "__main__":
    run("Tìm thông tin về LangChain Agent.")