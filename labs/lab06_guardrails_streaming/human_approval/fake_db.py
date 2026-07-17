from typing import Any
from copy import deepcopy

BASE_ORDERS = {
    "ORD-1001": {
        "order_id": "ORD-1001",
        "customer_name": "Nguyễn Văn An",
        "product": "Bàn phím cơ K8",
        "paid_amount": 1_250_000,
        "status": "delivered",
        "delivered_days_ago": 3,
        "refunded": False,
    },
    "ORD-1002": {
        "order_id": "ORD-1002",
        "customer_name": "Trần Thị Bình",
        "product": "Tai nghe H5",
        "paid_amount": 800_000,
        "status": "delivered",
        "delivered_days_ago": 20,
        "refunded": False,
    },
}

ORDERS = deepcopy(BASE_ORDERS)
REFUND_LOG: list[dict[str, Any]] = []


def reset_demo_data() -> None:
    """Đưa fake database về trạng thái ban đầu."""

    ORDERS.clear()
    ORDERS.update(deepcopy(BASE_ORDERS))
    REFUND_LOG.clear()