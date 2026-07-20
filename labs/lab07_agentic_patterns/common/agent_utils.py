
"""Utilities để đọc kết quả từ LangChain agent."""

from __future__ import annotations

from typing import Any

from langchain_core.messages import (
    AIMessage,
    ToolMessage,
)


def unwrap_state(result: Any) -> dict[str, Any]:
    """Hỗ trợ cả output dict thông thường và GraphOutput v2."""

    if hasattr(result, "value"):
        return result.value

    if isinstance(result, dict):
        return result

    raise TypeError(
        f"Unsupported agent result type: {type(result)!r}"
    )


def content_to_text(content: Any) -> str:
    """Chuyển message content thành text."""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []

        for block in content:
            if isinstance(block, str):
                parts.append(block)

            elif isinstance(block, dict):
                text = (
                    block.get("text")
                    or block.get("content")
                )

                if text:
                    parts.append(str(text))

        return "\n".join(parts)

    return str(content)


def last_ai_text(result_or_state: Any) -> str:
    """Lấy nội dung AIMessage cuối cùng."""

    if isinstance(result_or_state, dict):
        state = result_or_state
    else:
        state = unwrap_state(result_or_state)

    messages = state.get("messages", [])

    for message in reversed(messages):
        if isinstance(message, AIMessage):
            text = content_to_text(
                message.content
            ).strip()

            if text:
                return text

    return ""


def collect_tool_messages(
    result_or_state: Any,
) -> list[dict[str, str]]:
    """Thu thập ToolMessage theo thứ tự thực thi."""

    if isinstance(result_or_state, dict):
        state = result_or_state
    else:
        state = unwrap_state(result_or_state)

    observations: list[dict[str, str]] = []

    for message in state.get("messages", []):
        if isinstance(message, ToolMessage):
            observations.append(
                {
                    "name": message.name or "unknown_tool",
                    "content": content_to_text(
                        message.content
                    ),
                    "tool_call_id": message.tool_call_id,
                }
            )

    return observations


def print_trace(result_or_state: Any) -> None:
    """In toàn bộ agent trace để quan sát agent loop."""

    if isinstance(result_or_state, dict):
        state = result_or_state
    else:
        state = unwrap_state(result_or_state)

    for index, message in enumerate(
        state.get("messages", []),
        start=1,
    ):
        role = type(message).__name__
        name = getattr(message, "name", None)

        suffix = f" [{name}]" if name else ""

        print(
            f"\n--- {index}. {role}{suffix} ---"
        )

        if (
            isinstance(message, AIMessage)
            and message.tool_calls
        ):
            print("Tool calls:")

            for tool_call in message.tool_calls:
                print(
                    f"  - {tool_call['name']}"
                    f"({tool_call.get('args', {})})"
                )

        text = content_to_text(
            message.content
        ).strip()

        if text:
            print(text)