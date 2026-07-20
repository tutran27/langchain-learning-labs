
"""LangChain tool factories backed by CommerceStore."""

from __future__ import annotations

from collections.abc import Iterable

from langchain.tools import tool
from langchain_core.tools import BaseTool

from labs.lab07_agentic_patterns.common.domain import CommerceStore, to_json


def build_read_tools(
    store: CommerceStore,
) -> dict[str, BaseTool]:
    """Tạo toàn bộ read-only tools."""

    @tool
    def get_order(order_id: str) -> str:
        """Get full order details by order ID.

        Includes customer, items, payment status and tracking code.
        """

        return to_json(
            store.get_order(order_id)
        )

    @tool
    def get_order_items(order_id: str) -> str:
        """Get enriched line items from an order.

        Includes product name, category, price and delivered quantity.
        """

        return to_json(
            {
                "order_id": order_id,
                "items": store.get_order_items(order_id),
            }
        )

    @tool
    def get_shipping_status(
        tracking_code: str,
    ) -> str:
        """Get live shipping status, location and ETA."""

        return to_json(
            store.get_shipping_status(tracking_code)
        )

    @tool
    def estimate_delivery(
        tracking_code: str,
    ) -> str:
        """Estimate delivery date using the latest shipping record."""

        shipping_status = store.get_shipping_status(
            tracking_code
        )

        return to_json(
            {
                "tracking_code": tracking_code,
                "status": shipping_status["status"],
                "estimated_delivery": shipping_status["eta"],
            }
        )

    @tool
    def check_inventory(product_id: str) -> str:
        """Check available inventory for a product ID."""

        return to_json(
            store.check_inventory(product_id)
        )

    @tool
    def get_return_policy(category: str) -> str:
        """Get return conditions for a product category."""

        return to_json(
            store.get_return_policy(category)
        )

    @tool
    def get_payment_status(order_id: str) -> str:
        """Get payment status and charged amount."""

        return to_json(
            store.get_payment_status(order_id)
        )

    @tool
    def calculate_refund(
        order_id: str,
        product_ids: list[str],
    ) -> str:
        """Calculate maximum refundable amount.

        This tool only calculates a refund.
        It never transfers money.
        """

        return to_json(
            store.calculate_refund(
                order_id,
                product_ids,
            )
        )

    @tool
    def check_return_window(
        order_id: str,
        category: str,
    ) -> str:
        """Check whether an order is inside the return window."""

        return to_json(
            store.check_return_window(
                order_id,
                category,
            )
        )

    tools = [
        get_order,
        get_order_items,
        get_shipping_status,
        estimate_delivery,
        check_inventory,
        get_return_policy,
        get_payment_status,
        calculate_refund,
        check_return_window,
    ]

    return {
        current_tool.name: current_tool
        for current_tool in tools
    }


def select_tools(
    registry: dict[str, BaseTool],
    names: Iterable[str],
) -> list[BaseTool]:
    """Lấy một số tool theo tên."""

    selected_tools: list[BaseTool] = []

    for name in names:
        if name not in registry:
            raise KeyError(
                f"Unknown tool name: {name}"
            )

        selected_tools.append(
            registry[name]
        )

    return selected_tools

if __name__ == "__main__":
    store = CommerceStore()
    registry = build_read_tools(store)
    print(f"Built {len(registry)} tools")