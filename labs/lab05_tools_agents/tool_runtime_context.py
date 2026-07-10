from dataclasses import dataclass
from typing import Literal

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from labs.lab01_foundation.llm_model import GroqLLMModel

llm = GroqLLMModel().groq_chat()

# ============================================================
# Fake database
# ============================================================

ORDERS = {
    "user_001": [
        {
            "order_id": "ORD-101",
            "product": "Bàn phím cơ K8",
            "status": "Đang giao",
        },
        {
            "order_id": "ORD-102",
            "product": "Chuột gaming M3",
            "status": "Đang chuẩn bị",
        },
    ],
    "user_002": [
        {
            "order_id": "ORD-201",
            "product": "Tai nghe H5",
            "status": "Đã giao",
        }
    ],
}


# ============================================================
# Runtime context
# ============================================================

@dataclass
class AppContext:
    user_id: str
    role: Literal["customer", "admin"] = "customer"


# ============================================================
# Tools
# ============================================================

@tool
def get_my_latest_order(
    runtime: ToolRuntime[AppContext],
) -> dict:
    """Lấy đơn hàng gần nhất của người dùng hiện tại."""

    # user_id do backend truyền vào, không phải do LLM tạo.
    user_id = runtime.context.user_id

    orders = ORDERS.get(user_id, [])

    if not orders:
        return {
            "success": False,
            "message": "Người dùng hiện tại chưa có đơn hàng.",
        }

    return {
        "success": True,
        "user_id": user_id,
        "order": orders[-1],
    }


@tool
def get_order_status(
    order_id: str,
    runtime: ToolRuntime[AppContext],
) -> dict:
    """
    Kiểm tra trạng thái một đơn hàng thuộc về người dùng hiện tại.
    """

    user_id = runtime.context.user_id
    role = runtime.context.role

    # Admin được xem toàn bộ đơn hàng.
    if role == "admin":
        all_orders = [
            order
            for orders in ORDERS.values()
            for order in orders
        ]
    else:
        # Customer chỉ được xem đơn hàng của chính mình.
        all_orders = ORDERS.get(user_id, [])

    for order in all_orders:
        if order["order_id"] == order_id:
            return {
                "success": True,
                "order": order,
            }

    return {
        "success": False,
        "message": (
            f"Không tìm thấy đơn hàng {order_id} "
            "hoặc bạn không có quyền truy cập."
        ),
    }


# ============================================================
# Agent
# ============================================================

agent = create_agent(
    model=llm,
    tools=[
        get_my_latest_order,
        get_order_status,
    ],
    context_schema=AppContext,
    system_prompt=(
        "Bạn là trợ lý quản lý đơn hàng. "
        "Khi người dùng hỏi về đơn hàng cá nhân, "
        "bắt buộc sử dụng tool phù hợp. "
        "Không yêu cầu người dùng cung cấp user_id."
    ),
)


# ============================================================
# Test
# ============================================================

def run_for_user(
    user_id: str,
    query: str,
    role: Literal["customer", "admin"] = "customer",
) -> None:
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        },
        context=AppContext(
            user_id=user_id,
            role=role,
        ),
    )

    print(f"\nUser ID: {user_id}")
    print(f"Role: {role}")
    print("Kết quả:")
    print(result["messages"][-1].content)


def run_tool_runtime_context() -> None:
    query = "Đơn hàng gần nhất của tôi là gì?"

    # Cùng một câu hỏi nhưng runtime context khác nhau.
    run_for_user(
        user_id="user_001",
        query=query,
    )

    run_for_user(
        user_id="user_002",
        query=query,
    )

    # user_001 thử đọc đơn hàng của user_002.
    run_for_user(
        user_id="user_001",
        query="Kiểm tra trạng thái đơn hàng ORD-201.",
    )

    # Admin có thể đọc đơn hàng ORD-201.
    run_for_user(
        user_id="admin_001",
        role="admin",
        query="Kiểm tra trạng thái đơn hàng ORD-201.",
    )


if __name__ == "__main__":
    run_tool_runtime_context()
