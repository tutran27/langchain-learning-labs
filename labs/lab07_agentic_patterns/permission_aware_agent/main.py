from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelRequest,
    ModelResponse,
    dynamic_prompt,
    wrap_model_call,
)
from langchain.tools import (
    ToolRuntime,
    tool,
)
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from labs.lab07_agentic_patterns.common.agent_utils import (
    print_trace,
    unwrap_state,
)
from labs.lab07_agentic_patterns.common.domain import (
    CommerceStore,
    to_json,
)
from labs.lab07_agentic_patterns.common.llm import get_llm
from labs.lab07_agentic_patterns.common.tools import (
    build_read_tools,
    select_tools,
)
Role = Literal[
    "support_agent",
    "supervisor",
    "admin",
]


@dataclass(frozen=True)
class UserContext:
    """Context được truyền khi invoke agent."""

    user_id: str
    role: Role
    region: str

ROLE_TOOLS: dict[Role, set[str]] = {
    "support_agent": {
        "get_order",
        "calculate_refund",
    },
    "supervisor": {
        "get_order",
        "calculate_refund",
        "issue_refund",
    },
    "admin": {
        "get_order",
        "calculate_refund",
        "issue_refund",
        "cancel_order",
    },
}


@dynamic_prompt
def role_aware_prompt(
    request: ModelRequest[UserContext],
) -> str:
    """Tạo system prompt dựa trên runtime context."""

    context = request.runtime.context

    role_rules = {
        "support_agent": (
            "Bạn chỉ được xem đơn và tính số tiền hoàn dự kiến. "
            "Bạn không có quyền thực hiện hoàn tiền hoặc hủy đơn."
        ),
        "supervisor": (
            "Bạn được xem đơn, tính hoàn tiền và đề xuất issue_refund. "
            "Mọi issue_refund phải chờ human approval. "
            "Bạn không được hủy đơn."
        ),
        "admin": (
            "Bạn được xem đơn, hoàn tiền và hủy đơn. "
            "issue_refund và cancel_order đều phải chờ human approval."
        ),
    }

    return (
        "Bạn là agent vận hành thương mại điện tử.\n"
        f"user_id={context.user_id}\n"
        f"role={context.role}\n"
        f"region={context.region}\n"
        "\n"
        f"{role_rules[context.role]}\n"
        "\n"
        "System prompt không phải lớp bảo mật cuối cùng. "
        "Tool sẽ kiểm tra quyền lại bằng Python.\n"
        "Nếu thiếu dữ liệu để tính refund, dùng get_order trước.\n"
        "Nếu human reject một hành động, không đề xuất lại "
        "cùng hành động trong lượt hiện tại."
    )

@wrap_model_call
def filter_tools_by_role(
    request: ModelRequest[UserContext],
    handler: Callable[
        [ModelRequest[UserContext]],
        ModelResponse,
    ],
) -> ModelResponse:
    """Chỉ đưa cho model những tool phù hợp với role."""

    context = request.runtime.context

    allowed_tool_names = ROLE_TOOLS[
        context.role
    ]

    filtered_tools = [
        current_tool
        for current_tool in request.tools
        if current_tool.name in allowed_tool_names
    ]

    new_request = request.override(
        tools=filtered_tools
    )

    return handler(new_request)