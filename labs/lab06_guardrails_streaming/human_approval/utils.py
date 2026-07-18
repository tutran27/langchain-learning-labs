import json
from typing import Any

from labs.lab06_guardrails_streaming.human_approval.fake_db import (
    ORDERS,
    get_order_info,
    reset_demo_data,
)


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

def serialize_tool_result(result: Any) -> str:
    if isinstance(result, str):
        return result

    return json.dumps(
        result,
        ensure_ascii=False,
        default=str,
    )

def format_currency(value: int) -> str:
    return f"{value:,.0f} VNĐ".replace(",", ".")


def review_refund(tool_args:dict) -> tuple[str,dict]:
    """
    Đầu vào: Tham số tool issue_refund
    Trả về: Tuple (action, args)
    Action:
    "approve": Phê duyệt
    "reject": Từ chối
    "edit": Chỉnh sửa
        Người duyệt cũng có thể sửa amount và reason.
    """
    order_id=tool_args.get("order_id")
    amount=tool_args.get("amount")
    reason=tool_args.get("reason")
    
    order=get_order_info(order_id)
    evaluation=evaluate_refund(order_id)

    print("\n" + "=" * 60)
    print("YÊU CẦU PHÊ DUYỆT HOÀN TIỀN")
    print("=" * 60)

    print(f"Mã đơn:       {order_id}")

    if order:
        print(f"Khách hàng:   {order['customer_name']}")
        print(f"Sản phẩm:     {order['product']}")
        print(
            "Đã thanh toán:",
            format_currency(order["paid_amount"]),
        )

    print(f"Số tiền hoàn: {format_currency(amount)}")
    print(f"Lý do:        {reason}")
    print(f"Đủ điều kiện: {evaluation['eligible']}")
    print(f"Đánh giá:     {evaluation['reason']}")

    if evaluation["max_refund_amount"]:
        print(
            "Hoàn tối đa:  ",
            format_currency(
                evaluation["max_refund_amount"]
            ),
        )
    
    while True:
        decision=input(
            "Chọn [a]pprove, [r]eject hoặc [e]dit? [a/r/e] "
        ).strip().lower()
        if decision == "a":
            return "approve", tool_args
        elif decision == "r":
            return "reject", tool_args
        elif decision == "e":
            edited_args=dict(**tool_args)
            
            edited_amount=input(
                f"Số tiền mới [{amount}]"
            ).strip()

            if edited_amount:
                try:
                    edited_amount=int(edited_amount)
                    edited_args["amount"]=edited_amount
                except ValueError:
                    print("Số tiền phải là số nguyên\n")
            else:
                print("Giữ nguyên số tiền\n")

            edited_reason=input(f"Lý do mới [{reason}]").strip()

            if edited_reason:
                edited_args["reason"]=edited_reason
            
            print("======== Đã cập nhật thông tin chỉnh sửa =========")
            print(json.dumps(edited_args,ensure_ascii=False,indent=2))
            
            confirm = input(
                "Phê duyệt thông tin này? [y/N]: "
            ).strip().lower()

            if confirm == "y":
                return "approve", edited_args

            print("Chưa phê duyệt. Quay lại bước lựa chọn.")
            continue

        print("Lựa chọn không hợp lệ.")