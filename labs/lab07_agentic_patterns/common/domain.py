

import copy
import json
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any


class OrderNotFoundError(Exception):
    """Không tìm thấy đơn hàng."""


class ProductNotFoundError(Exception):
    """Không tìm thấy sản phẩm."""


class ShippingServiceUnavailable(Exception):
    """Lỗi tạm thời từ dịch vụ vận chuyển."""


class InvalidRefundError(Exception):
    """Yêu cầu hoàn tiền không hợp lệ."""

PRODUCTS: dict[str, dict[str, Any]] = {
    "P100": {
        "name": "Tai nghe Bluetooth",
        "category": "electronics",
        "price": 700_000,
    },
    "P200": {
        "name": "Chuột không dây",
        "category": "electronics",
        "price": 500_000,
    },
    "P300": {
        "name": "Bình giữ nhiệt",
        "category": "home",
        "price": 350_000,
    },
}


ORDERS: dict[str, dict[str, Any]] = {
    "ORD-1001": {
        "customer_id": "CUS-01",
        "status": "shipped",
        "tracking_code": "TRK-1001",
        "payment_status": "paid",
        "total": 1_200_000,
        "items": [
            {
                "product_id": "P100",
                "quantity": 1,
                "delivered_quantity": 1,
            },
            {
                "product_id": "P200",
                "quantity": 1,
                "delivered_quantity": 0,
            },
        ],
        "delivered_at": None,
    },
    "ORD-1002": {
        "customer_id": "CUS-02",
        "status": "shipped",
        "tracking_code": "TRK-1002",
        "payment_status": "paid",
        "total": 350_000,
        "items": [
            {
                "product_id": "P300",
                "quantity": 1,
                "delivered_quantity": 0,
            },
        ],
        "delivered_at": None,
    },
    "ORD-1003": {
        "customer_id": "CUS-03",
        "status": "delivered",
        "tracking_code": "TRK-1003",
        "payment_status": "paid",
        "total": 700_000,
        "items": [
            {
                "product_id": "P100",
                "quantity": 1,
                "delivered_quantity": 1,
            },
        ],
        "delivered_at": "2026-07-10",
    },
}


SHIPPING: dict[str, dict[str, Any]] = {
    "TRK-1001": {
        "status": "in_transit",
        "location": "Trung tâm phân loại Hà Nội",
        "eta": "2026-07-21",

        # Hai lần đầu lỗi, lần thứ ba thành công.
        "transient_failures_before_success": 2,
        "always_fail": False,
    },
    "TRK-1002": {
        "status": "unknown",
        "location": None,
        "eta": None,

        # Dịch vụ luôn lỗi.
        "transient_failures_before_success": 0,
        "always_fail": True,
    },
    "TRK-1003": {
        "status": "delivered",
        "location": "Đã giao cho người nhận",
        "eta": "2026-07-10",
        "transient_failures_before_success": 0,
        "always_fail": False,
    },
}


INVENTORY: dict[str, int] = {
    "P100": 12,
    "P200": 0,
    "P300": 5,
}


RETURN_POLICIES: dict[str, dict[str, Any]] = {
    "electronics": {
        "return_window_days": 14,
        "restocking_fee_percent": 0,
        "conditions": [
            "Sản phẩm còn đầy đủ phụ kiện",
            "Không có dấu hiệu hư hỏng do người dùng",
        ],
    },
    "home": {
        "return_window_days": 7,
        "restocking_fee_percent": 0,
        "conditions": [
            "Sản phẩm chưa qua sử dụng",
        ],
    },
}

@dataclass
class CommerceStore:
    """Database giả lập có thể reset sau từng test case."""

    orders: dict[str, dict[str, Any]] = field(
        default_factory=lambda: copy.deepcopy(ORDERS)
    )

    products: dict[str, dict[str, Any]] = field(
        default_factory=lambda: copy.deepcopy(PRODUCTS)
    )

    shipping: dict[str, dict[str, Any]] = field(
        default_factory=lambda: copy.deepcopy(SHIPPING)
    )

    inventory: dict[str, int] = field(
        default_factory=lambda: copy.deepcopy(INVENTORY)
    )

    return_policies: dict[str, dict[str, Any]] = field(
        default_factory=lambda: copy.deepcopy(RETURN_POLICIES)
    )

    shipping_attempts: dict[str, int] = field(
        default_factory=dict
    )

    refunds: list[dict[str, Any]] = field(
        default_factory=list
    )

    cancellations: list[dict[str, Any]] = field(
        default_factory=list
    )

    def reset_runtime_state(self) -> None:
        """Reset counter và các side effect."""

        self.shipping_attempts.clear()
        self.refunds.clear()
        self.cancellations.clear()
        self.orders = copy.deepcopy(ORDERS)

    def get_order(self, order_id:str)->dict[str,Any]:
        order = self.orders.get(order_id)
        if order is None:
            raise OrderNotFoundError(f"❌ Không tìm thấy đơn hàng: {order_id}")
        else:
            return {
                'order_id': order_id,
                **copy.deepcopy(order),
            }
        

if __name__ == "__main__":
    store = CommerceStore()
    print(store.get_order("ORD-1001"))
        