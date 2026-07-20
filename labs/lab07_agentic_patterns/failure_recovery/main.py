"""Lab 1: failure recovery.

Chạy:
    python -m labs.lab07_agentic_patterns.failure_recovery.main

"""

from __future__ import annotations

from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ToolCallLimitMiddleware,
    ToolRetryMiddleware,
    wrap_tool_call,
)
from langchain_core.messages import ToolMessage

from labs.lab07_agentic_patterns.common.agent_utils import print_trace
from labs.lab07_agentic_patterns.common.domain import (
    CommerceStore,
    InvalidRefundError,
    OrderNotFoundError,
    ProductNotFoundError,
    ShippingServiceUnavailable,
)
from labs.lab01_foundation.llm_model import GroqLLMModel
from labs.lab07_agentic_patterns.common.tools import (
    build_read_tools,
    select_tools,
)


NON_RETRYABLE_ERRORS = (
    OrderNotFoundError,
    ProductNotFoundError,
    InvalidRefundError,
    ValueError,
)


@wrap_tool_call
def convert_domain_errors(
    request: Any,
    handler: Any,
) -> Any:
    """Chuyển business error thành ToolMessage.

    Các lỗi deterministic như không tìm thấy đơn không nên retry.
    Agent sẽ nhận lỗi và tự tạo câu trả lời phù hợp.
    """

    try:
        return handler(request)

    except NON_RETRYABLE_ERRORS as error:
        tool_call = request.tool_call

        return ToolMessage(
            content=(
                "NON_RETRYABLE_BUSINESS_ERROR: "
                f"{type(error).__name__}: {error}. "
                "Không gọi lại cùng tool với cùng arguments."
            ),
            tool_call_id=tool_call["id"],
            name=tool_call["name"],
        )


def format_exhausted_shipping_error(
    error: Exception,
) -> str:
    """Message trả về agent khi đã retry hết."""

    return (
        "SHIPPING_SERVICE_UNAVAILABLE_AFTER_RETRIES: "
        f"{type(error).__name__}: {error}. "
        "Hãy thông báo rằng chưa thể xác minh trạng thái "
        "vận chuyển thời gian thực. Không được tự bịa status hoặc ETA."
    )


def build_agent(
    store: CommerceStore,
) -> Any:
    """Khởi tạo agent có retry và call limit."""

    llm = GroqLLMModel().groq_chat()

    registry = build_read_tools(store)

    tools = select_tools(
        registry,
        [
            "get_order",
            "get_shipping_status",
        ],
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "Bạn là trợ lý theo dõi đơn hàng.\n"
            "\n"
            "Quy trình bắt buộc:\n"
            "1. Dùng get_order để lấy tracking_code.\n"
            "2. Dùng get_shipping_status với tracking_code.\n"
            "\n"
            "Không tự suy đoán trạng thái hoặc ETA.\n"
            "Nếu nhận NON_RETRYABLE_BUSINESS_ERROR, "
            "không gọi lại cùng tool với cùng arguments.\n"
            "Nếu shipping service hết retry, hãy nói rõ "
            "chưa thể xác minh dữ liệu thời gian thực."
        ),
        middleware=[
            # Middleware đầu tiên là lớp ngoài cùng.
            convert_domain_errors,

            ToolRetryMiddleware(
                # Hai retry sau lần gọi đầu tiên:
                # tổng cộng tối đa ba lần.
                max_retries=2,

                # Chỉ áp dụng cho tool này.
                tools=[
                    "get_shipping_status",
                ],

                # Chỉ retry lỗi hạ tầng tạm thời.
                retry_on=(
                    ConnectionError,
                    TimeoutError,
                    ShippingServiceUnavailable,
                ),

                # Hết retry thì trả observation về model.
                on_failure=format_exhausted_shipping_error,

                # Demo sử dụng delay thấp.
                initial_delay=0.05,
                backoff_factor=1.0,
                max_delay=0.05,
                jitter=False,
            ),

            ToolCallLimitMiddleware(
                tool_name="get_shipping_status",
                run_limit=3,
                exit_behavior="continue",
            ),
        ],
    )

    return agent


def run_case(
    agent: Any,
    store: CommerceStore,
    title: str,
    query: str,
) -> None:
    """Chạy một test case."""

    print("\n" + "=" * 88)
    print(title)
    print("=" * 88)

    store.reset_runtime_state()

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

    print_trace(result)

    print(
        "\nShipping attempts:",
        store.shipping_attempts,
    )


def run_demo() -> None:
    store = CommerceStore()
    agent = build_agent(store)

    run_case(
        agent=agent,
        store=store,
        title=(
            "CASE 1 — Hai lỗi tạm thời, "
            "thành công ở lần thứ ba"
        ),
        query=(
            "Kiểm tra đơn ORD-1001 đang được giao tới đâu "
            "và dự kiến khi nào đến."
        ),
    )

    run_case(
        agent=agent,
        store=store,
        title=(
            "CASE 2 — Lỗi nghiệp vụ không được retry"
        ),
        query=(
            "Kiểm tra tình trạng giao hàng "
            "của đơn ORD-9999."
        ),
    )

    run_case(
        agent=agent,
        store=store,
        title=(
            "CASE 3 — Retry hết giới hạn "
            "nhưng agent không được bịa"
        ),
        query=(
            "Kiểm tra trạng thái vận chuyển "
            "của ORD-1002."
        ),
    )

    run_case(
        agent=agent,
        store=store,
        title=(
            "CASE 4 — ToolCallLimitMiddleware "
            "chặn gọi tool quá mức"
        ),
        query=(
            "Với ORD-1001, hãy gọi get_shipping_status "
            "năm lần liên tiếp để kiểm tra tính ổn định. "
            "Sau đó giải thích điều gì xảy ra khi vượt giới hạn."
        ),
    )


if __name__ == "__main__":
    run_demo()