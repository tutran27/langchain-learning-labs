from labs.lab06_guardrails_streaming.human_approval.fake_db import ORDERS, reset_demo_data


def get_order_info(order_id: str) -> dict:
    """
    Lấy thông tin đơn hàng
    """
    for order in ORDERS.values():
        if order["order_id"] == order_id:
            return order
    return None

def evaluate_refund(order_id: str) -> dict:
    """
    Kiểm tra điều kiện hoàn tiền.

    Quy tắc demo:
    - Đơn hàng phải tồn tại.
    - Đơn đã được giao.
    - Chưa từng hoàn tiền.
    - Giao không quá 7 ngày.
    """
    order_info = get_order_info(order_id)
    if not order_info:
        return {
            "eligible": False,
            "reason": "Không tìm thấy đơn hàng.",
            "max_refund_amount": 0,
            }
    if order_info['refunded']:
        return {
            "eligible": False,
            "reason": "Đơn hàng đã được hoàn tiền.",
            "max_refund_amount": 0,
            }
    if order_info['status'] != 'delivered':
        return {
            "eligible": False,
            "reason": "Đơn hàng chưa được giao.",
            "max_refund_amount": 0,
            }
    if order_info['delivered_days_ago'] > 7:
        return {
            "eligible": False,
            "reason": "Đơn hàng đã giao quá 7 ngày.",
            "max_refund_amount": 0,
            }
    return {
        "eligible": True,
        "reason": "Đơn hàng đủ điều kiện hoàn tiền.",
        "max_refund_amount": order_info["paid_amount"],
        }