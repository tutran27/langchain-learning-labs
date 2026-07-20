

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
        "delivered_at": "2026-07-10",
    },
    "ORD-1003": {
        "customer_id": "CUS-03",
        "status": "prepair",
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
        """Lấy thông tin đơn hàng."""
        order = self.orders.get(order_id)
        if order is None:
            raise OrderNotFoundError(f"❌ Không tìm thấy đơn hàng: {order_id}")
        else:
            return {
                'order_id': order_id,
                **copy.deepcopy(order),
            }
        
    def get_order_info(self,order_id:str) -> dict[str,Any]:
        """Lấy line items và thông tin sản phẩm."""
        order = self.get_order(order_id)
        items = []
        for item in order['items']:
            product = self.products.get(item['product_id'])
            if product is None:
                raise ProductNotFoundError(f"❌ Không tìm thấy sản phẩm: {item['product_id']}")
            items.append({
                **item,
                **product
            })
        return {
            'order_id': order_id,
            'items': items,
        }

    def get_shipping_status(
        self,
        tracking_code: str,
    ) -> dict[str, Any]:
        """Mô phỏng API vận chuyển có thể lỗi tạm thời."""

        shipment = self.shipping.get(tracking_code)
        if shipment is None:
            raise ShippingServiceUnavailable(f"❌ Không tìm thấy mã vận chuyển: {tracking_code}")

        attempt = (self.shipping_attempts.get(tracking_code, 0) +1)
        self.shipping_attempts[tracking_code] = attempt
        print(f"[LOG] {self.shipping_attempts}")

        #Luôn lỗi
        if shipment['always_fail']:
            raise ShippingServiceUnavailable(f"❌ Lỗi tạm thời từ dịch vụ vận chuyển (lần {attempt}).")

        #Lỗi tạm thời x lần đầu
        if attempt <= shipment['transient_failures_before_success']:
            raise ShippingServiceUnavailable(f"❌ Lỗi tạm thời từ dịch vụ vận chuyển (lần {attempt}).")

        return {
            'tracking_code': tracking_code,
            'attempt': attempt,
            'status': shipment['status'],
            'location': shipment['location'],
            'eta': shipment['eta'],
        }

    def check_inventory(self, product_id: str):
        if product_id not in self.products:
            raise ProductNotFoundError(f"❌ Không tìm thấy sản phẩm: {product_id}")

        stock = self.inventory.get(product_id)
        if stock is None:
            raise ProductNotFoundError(f"❌ Không tìm thấy sản phẩm: {product_id}")
        return {
            'product_id': product_id,
            'name': self.products[product_id]['name'],
            'stock': stock,
        }
 
    def get_return_policy(self, product_id: str):
        if product_id not in self.products:
            raise ProductNotFoundError(f"❌ Không tìm thấy sản phẩm: {product_id}")
        category = self.products[product_id]['category']
        if category not in self.return_policies:
            return {
                "product_id": product_id,
                "category": category,
                "eligible": False,
                "reason": "Không có chính sách trả hàng cho danh mục này",
            }
        return {
            'product_id': product_id,
            'category': category,
            'eligible': True,
            
            'policy': self.return_policies[category],
        }
    
    def get_payment_status(self, order_id: str):
        """Mô phỏng việc check API thanh toán."""
        if order_id not in self.orders:
            raise OrderNotFoundError(f"❌ Không tìm thấy đơn hàng: {order_id}")
        
        return {
            'order_id': order_id,
            'status': self.orders[order_id]['payment_status'],
            'charge_amount':self.orders[order_id]['total'],
        }

    def calculate_refund(
        self,
        order_id: str,
        product_ids: list[str],
    ):
        """Chỉ tính tiền hoàn, không thực hiện chuyển tiền."""

        order = self.get_order(order_id)
        
        order_product_ids = {item['product_id'] for item in order['items']}
        
        for p_id in product_ids:
            if p_id not in order_product_ids:
                raise InvalidRefundError(f"❌ Sản phẩm {p_id} không thuộc order {order_id}")

        amount=sum(self.products[p_id]['price'] for p_id in product_ids)

        return {
            "order_id": order_id,
            "product_ids": product_ids,
            "maximum_refund_amount": amount,
            "currency": "VND",
            "calculation_basis": (
                f"Tổng giá ₫{amount:,.0f} cho {len(product_ids)} sản phẩm: {', '.join(product_ids)} "
                f"trong đơn {order_id}"
            ),
        }

    def check_return_window(
        self,
        order_id:str,
        category: str
    ) -> dict[str,Any]:
        """Kiểm tra thời hạn trả hàng."""
        order=self.get_order(order_id)
        policies=self.return_policies.get(category)
        if policies is None:
            raise InvalidRefundError(f"❌ Không có chính sách trả hàng cho danh mục: {category}")

        delivered_at=order['delivered_at']
        if delivered_at is None:
            return {
                "order_id":order_id,
                "within_window": True,
                "reason":"Đơn chưa được ghi nhận là đã giao; "
                         "quy trình giao thiếu có thể áp dụng."
            }

        return_days = policies['return_window_days']
        delivery_date=datetime.fromisoformat(delivered_at)
        deadline=delivery_date + timedelta(days=return_days)
        now = datetime.now()
        days_left = (deadline - now).days
        allow_return=days_left>=0

        print(f"[LOG] Delivery at: {delivery_date}")
        print(f"[LOG] Return days: {return_days}")
        print(f"[LOG] Deadline: {deadline}")
        print(f"[LOG] Now: {now}")
        print(f"[LOG] Days left: {days_left}")
        print(f"[LOG] Allow return: {allow_return}")

        return {
            "order_id": order_id,
            "within_window": allow_return,
            "delivered_at": delivered_at,
            "deadline": deadline.isoformat(),
        }     
    
    def issue_refund(
        self,
        order_id: str,
        amount: float,
        reason: str,
        actor_user_id: str = None,
    ) -> dict[str, Any]:
        if amount <=0:
            raise InvalidRefundError("Số tiền hoàn phải lớn hơn 0")

        order=self.get_order(order_id)
        
        if order.get('payment_status')!='paid':
            raise InvalidRefundError("Đơn hàng chưa được thanh toán")
            
        if amount > order['total']:
            raise InvalidRefundError("Số tiền hoàn lớn hơn tổng giá trị đơn hàng")
        
        refund_id=f"REF-{len(self.refunds)+1:04d}"

        record={
            'refund_id':refund_id,
            'order_id':order_id,
            'amount':amount,
            'reason':reason,
            'actor_user_id':actor_user_id,
            'status':'approved',
            'refunded_at':datetime.now().isoformat(),
        }

        print("[LOG] Refund Record:", record)
        self.refunds.append(record)

        order["payment_status"] = "refunded"

        return copy.deepcopy(record)

    def cancel_order(
        self,
        order_id:str,
        reason:str,
        actor_user_id: str = None,
    ) ->dict[str,Any]:
        """Hủy đơn hàng."""
        order=self.get_order(order_id)

        if order.get('status') in {'delivered','cancelled'}:
            raise InvalidRefundError("Không thể hủy đơn đã được giao hoặc đã hủy")
        
        order['status']='cancelled'

        record={
            'order_id':order_id,
            
            'reason':reason,
            'actor_user_id':actor_user_id,
            'refunded_at':datetime.now().isoformat(),
        }

        self.cancellations.append(record)

        return copy.deepcopy(record)

def to_json(data: Any) -> str:
    """Serialize kết quả tool sang JSON."""

    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
    )
if __name__ == "__main__":
    import json 
    store = CommerceStore()

    print("\n\n=== 1. GET ORDER ===")
    order_data = store.get_order("ORD-1001")
    print(json.dumps(order_data,indent=2,ensure_ascii=False))

    print("\n\n=== 2. GET ORDER INFO ===")
    order_info = store.get_order_info("ORD-1001")
    print(json.dumps(order_info,indent=2,ensure_ascii=False))
        
    # Gọi 3 lần để thấy retry tự động
    print("\n\n=== 3. GET SHIPPING STATUS (3 CALLS WITH RETRIES) ===")
    for i in range(3):
        print(f"\n\n=== GET SHIPPING STATUS (CALL {i+1}) ===")
        try:
            status = store.get_shipping_status("TRK-1001")
            print(json.dumps(status,indent=2,ensure_ascii=False))
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
    
    print("\n\n=== 4. CHECK INVENTORY ===")
    inventory_data = store.check_inventory("P100")
    print(json.dumps(inventory_data,indent=2,ensure_ascii=False))

    print("\n\n=== 5. GET RETURN POLICY ===")
    return_policy = store.get_return_policy("P100")
    print(json.dumps(return_policy,indent=2,ensure_ascii=False))

    print("\n\n=== 6. GET PAYMENT STATUS ===")
    payment_status = store.get_payment_status("ORD-1001")
    print(json.dumps(payment_status,indent=2,ensure_ascii=False))

    print("\n\n=== 7. CALCULATE REFUND ===")
    refund = store.calculate_refund("ORD-1001", ["P100"])
    print(json.dumps(refund,indent=2,ensure_ascii=False))

    print("\n\n=== 8. CHECK RETURN WINDOW (NOT DELIVERED YET) ===")
    window_status=store.check_return_window("ORD-1001","electronics")
    print(json.dumps(window_status,indent=2,ensure_ascii=False))

    print("\n\n=== 9. CHECK RETURN WINDOW (DELIVERED) ===")
    window_status_not_delivered=store.check_return_window("ORD-1002","home")
    print(json.dumps(window_status_not_delivered,indent=2,ensure_ascii=False))
    
    print("\n\n=== 10. ISSUE REFUND ===")
    refund_record=store.issue_refund(
        order_id="ORD-1001",
        amount=1000000,
        reason="Sản phẩm bị lỗi, khách trả lại",
        actor_user_id="USER-001",
    )
    print(json.dumps(refund_record,indent=2,ensure_ascii=False))
    
    print("\n\n=== 11. CANCLE ORDER (NOT DELIVERED) ===")
    cancellation_record = store.cancel_order(
        order_id="ORD-1003",
        reason="Khách thay đổi ý định",
        actor_user_id="USER-001",
    )
    print(json.dumps(cancellation_record, indent=2, ensure_ascii=False))