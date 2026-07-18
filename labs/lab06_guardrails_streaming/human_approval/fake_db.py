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
    "ORD-1003": {
        "order_id": "ORD-1003",
        "customer_name": "Lê Minh Hoàng",
        "product": "Chuột gaming X1",
        "paid_amount": 550_000,
        "status": "delivered",
        "delivered_days_ago": 5,
        "refunded": False,
    },
    "ORD-1004": {
        "order_id": "ORD-1004",
        "customer_name": "Phạm Thu Huyền",
        "product": "Webcam HD",
        "paid_amount": 450_000,
        "status": "pending",
        "delivered_days_ago": 0,
        "refunded": False,
    },
}

ORDERS = deepcopy(BASE_ORDERS)
REFUND_LOG: list[dict[str, Any]] = []

def get_order_info(order_id: str) -> dict:
    """
    Lấy thông tin đơn hàng
    """
    for order in ORDERS.values():
        if order["order_id"] == order_id:
            return order
    return None
    
def reset_demo_data() -> None:
    """Đưa fake database về trạng thái ban đầu."""

    ORDERS.clear()
    ORDERS.update(deepcopy(BASE_ORDERS))
    REFUND_LOG.clear()