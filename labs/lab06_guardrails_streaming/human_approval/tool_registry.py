from langchain.tools import tool
from langchain.agents import create_agent


from labs.lab06_guardrails_streaming.human_approval.utils import evaluate_refund
from labs.lab06_guardrails_streaming.human_approval.fake_db import ORDERS

@tool 
def get_order_info(order_id: str):
    """Lấy thông tin đơn hàng theo order_id.
    Đầu vào: order_id (chuỗi)
    Đầu ra: dict chứa thông tin đơn hàng hoặc error nếu không tìm thấy
    """
    for order in ORDERS.values():
        if order['order_id'] == order_id:
            return {
                'success': True,
                'order': order,
                }
    return {
        'success': False,
        'error': f'Không tìm thấy đơn hàng: {order_id}'
        }

@tool
def check_refund_eligible(order_id: str):
    """
    Kiểm tra đơn hàng có đủ điều kiện hoàn tiền hay không.
    Tool này chỉ kiểm tra và không thực hiện hoàn tiền.
    """
    evaluation = evaluate_refund(order_id)
    return {
        "order_id": order_id,
        "refund_reason": evaluation.get('reason'),
        **evaluation
    }

@tool
def issue_refund(
    order_id: str,
    amount: int,
    reason: str,
):
    """
    Thực hiện hoàn tiền cho đơn hàng.

    Đây là hành động nhạy cảm, chỉ được thực thi sau khi
    nhân viên đã kiểm tra và phê duyệt.
    """
    order_info = None
    for order in ORDERS.values():
        if order['order_id'] == order_id:
            order_info=order
            break

    if order_info is None:
        return{
            "success": False,
            "message":"Order not found"
        }
    evaluate=evaluate_refund(order_id)

    if not evaluate['eligible']:
        return {
            "success": False,
            "message": evaluate['reason']
        }
    if amount > evaluate['max_refund_amount']:
        return {
            "success": False,
            "message": f"Số tiền hoàn '{amount}' vượt quá '{evaluate['max_refund_amount']}'"
        }
    if amount <=0:
        return {
            "success": False,
            "message": "Số tiền hoàn phải lớn hơn 0"
        }
    
    order_info['refunded'] = True
    return {
        "success": True,
        "message": f"Đã hoàn tiền thành công cho đơn hàng {order_id} số tiền {amount}",
        }

TOOLS=[get_order_info,check_refund_eligible,issue_refund]
TOOLS_BY_NAME={tool.name: tool for tool in TOOLS}
SENSITIVE_TOOLS={"issue_refund"}

if __name__ == "__main__":
    import json

    info=get_order_info.invoke({'order_id':"ORD-1001"})
    print("=============== Thông tin đơn hàng =================\n")
    print(json.dumps(info,ensure_ascii=False,indent=2))

    print("\n=============== Kiểm tra điều kiện hoàn tiền ================\n")
    check=check_refund_eligible.invoke({'order_id':"ORD-1001"})
    print(json.dumps(check,ensure_ascii=False,indent=2))