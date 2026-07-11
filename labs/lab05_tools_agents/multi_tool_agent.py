import sys
from typing import Literal

from langchain.agents import create_agent
from langchain.messages import AIMessage, ToolMessage
from langchain.tools import tool

from labs.lab01_foundation.llm_model import GroqLLMModel

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ============================================================
# Fake database
# ============================================================

PRODUCTS = {
    "bàn phím cơ k8": {
        "product_id": "KB-K8",
        "name": "Bàn phím cơ K8",
        "unit_price": 2_000_000,
        "weight_kg": 0.9,
    },
    "chuột gaming m3": {
        "product_id": "MS-M3",
        "name": "Chuột gaming M3",
        "unit_price": 800_000,
        "weight_kg": 0.3,
    },
}


def find_product(product_ref: str):
    product = PRODUCTS.get(product_ref.lower())
    if product is not None:
        return product

    product_ref = product_ref.lower()
    for product in PRODUCTS.values():
        if product["product_id"].lower() == product_ref:
            return product

    return None


@tool
def get_product_info(product_name: str):
    """Lấy thông tin sản phẩm theo tên sản phẩm."""
    product = PRODUCTS.get(product_name.lower())

    if product is None:
        return {
            "success": False,
            "error": f"Không tìm thấy sản phẩm: {product_name}",
        }

    return {
        "success": True,
        "product": product,
    }


@tool
def get_member_discount(
    product_id: str,
    member_level: Literal["bronze", "silver", "gold"],
):
    """Lấy mức giảm giá hội viên theo product_id và hạng thành viên."""
    product = find_product(product_id)

    if product is None:
        return {
            "success": False,
            "error": f"Không tìm thấy sản phẩm: {product_id}",
        }

    discount = {
        "bronze": 0.0,
        "silver": 0.1,
        "gold": 0.2,
    }
    return {
        "success": True,
        "discount": discount.get(member_level, 0.0),
        "member_level": member_level,
        "product_id": product["product_id"],
    }


@tool
def get_shipping_fee(
    product_id: str,
    shipping_method: Literal["nhanh", "tiết kiệm"],
    region: Literal["hanoi", "hcm", "danang"],
    quantity: int,
):
    """Lấy phí vận chuyển theo product_id, phương thức giao, khu vực và số lượng."""
    product = find_product(product_id)
    if product is None:
        return {
            "success": False,
            "error": f"Không tìm thấy sản phẩm: {product_id}",
        }

    shipping_fee_table = {
        "hanoi": {
            "nhanh": 20_000,
            "tiết kiệm": 10_000,
        },
        "hcm": {
            "nhanh": 30_000,
            "tiết kiệm": 20_000,
        },
        "danang": {
            "nhanh": 25_000,
            "tiết kiệm": 15_000,
        },
    }

    if quantity <= 0:
        return {
            "success": False,
            "error": "Số lượng phải lớn hơn 0",
        }

    weight = product["weight_kg"] * quantity
    base_fee = shipping_fee_table.get(region, {}).get(shipping_method, 50_000)
    weight_fee = weight * 5_000
    total_shipping_fee = base_fee + weight_fee

    return {
        "success": True,
        "shipping_fee": total_shipping_fee,
        "shipping_method": shipping_method,
        "region": region,
        "product_id": product["product_id"],
        "weight": weight,
    }


@tool
def calculate_final_total(
    product_id: str,
    member_level: Literal["bronze", "silver", "gold"],
    shipping_method: Literal["nhanh", "tiết kiệm"],
    region: Literal["hanoi", "hcm", "danang"],
    quantity: int,
):
    """Tính tổng tiền cuối cùng từ dữ liệu sản phẩm, hội viên và vận chuyển."""
    if quantity <= 0:
        return {
            "success": False,
            "error": "Số lượng phải lớn hơn 0",
        }

    product = find_product(product_id)
    if product is None:
        return {
            "success": False,
            "error": f"Không tìm thấy sản phẩm: {product_id}",
        }

    discount_result = get_member_discount.func(product["product_id"], member_level)
    if not discount_result["success"]:
        return discount_result

    shipping_result = get_shipping_fee.func(
        product["product_id"],
        shipping_method,
        region,
        quantity,
    )
    if not shipping_result["success"]:
        return shipping_result

    unit_price = product["unit_price"]
    discount_rate = discount_result["discount"]
    shipping_fee = shipping_result["shipping_fee"]
    total_price = unit_price * quantity
    total_price_after_discount = total_price * (1 - discount_rate)
    total_price_after_shipping = total_price_after_discount + shipping_fee

    return {
        "success": True,
        "product_id": product["product_id"],
        "unit_price": unit_price,
        "discount_rate": discount_rate,
        "shipping_fee": shipping_fee,
        "total_price": total_price,
        "total_price_after_discount": total_price_after_discount,
        "total_price_after_shipping": total_price_after_shipping,
    }

SYSTEM_PROMPT = """
Bạn là trợ lý tính tiền đơn hàng.

Quy tắc bắt buộc, phải tuân thủ nghiêm ngặt:
1. Mỗi lượt phản hồi chỉ được gọi đúng 1 tool duy nhất.
2. Tuyệt đối không gọi nhiều tool trong cùng một message.
3. Tuyệt đối không gọi lại tool đã có kết quả hợp lệ trong ToolMessage, trừ khi người dùng yêu cầu làm mới dữ liệu.
4. Tuyệt đối không tự đoán product_id, đơn giá, giảm giá, phí ship hoặc kết quả tính toán.
5. Khi cần tính tổng tiền, bắt buộc gọi tool đúng thứ tự sau và không được bỏ bước:
   - get_product_info
   - get_member_discount
   - get_shipping_fee
   - calculate_final_total
6. Tool sau chỉ được dùng dữ liệu lấy ra từ ToolMessage hợp lệ gần nhất của tool trước.
7. Khi lấy dữ liệu từ ToolMessage, phải sao chép NGUYÊN VĂN giá trị thực tế từ JSON result.
   Ví dụ: nếu ToolMessage chứa "product_id": "KB-K8" thì tool call tiếp theo phải truyền đúng "KB-K8".
8. Tuyệt đối không được dùng placeholder hoặc giá trị đại diện trong bất kỳ tool call nào.
   Các giá trị bị cấm gồm: "[product_id]", "<product_id>", "product_id_here", "id_tu_buoc_truoc".
9. Nếu chưa có giá trị cụ thể trong ToolMessage thì không được gọi tool tiếp theo.
10. Trước khi gọi get_member_discount, get_shipping_fee hoặc calculate_final_total, phải tự kiểm tra:
    - product_id có phải là giá trị thật đọc được từ ToolMessage không
    - product_id có đúng nguyên văn như trong ToolMessage không
    - product_id có phải placeholder hay giá trị suy diễn không
11. Ở bước calculate_final_total, chỉ được truyền đúng 5 tham số:
    - product_id
    - member_level
    - shipping_method
    - region
    - quantity
12. Sau khi calculate_final_total trả kết quả thành công, phải dừng gọi tool ngay và trả lời người dùng bằng tiếng Việt trong content.
13. Nếu bất kỳ tool nào trả lỗi, phải dừng ngay, không gọi thêm tool, và giải thích lỗi cho người dùng.
14. Không được lặp lại chu trình tool nếu đã có đủ dữ liệu để trả lời.
"""


def build_agent():
    llm = GroqLLMModel().groq_chat()
    return create_agent(
        model=llm,
        tools=[
            get_product_info,
            get_member_discount,
            get_shipping_fee,
            calculate_final_total,
        ],
        system_prompt=SYSTEM_PROMPT,
    )


def format_tool_args(tool_args: dict) -> str:
    if not tool_args:
        return "{}"
    return ", ".join(f"{key}={value!r}" for key, value in tool_args.items())


def print_agent_trace(messages: list) -> list[str]:
    called_tools: list[str] = []

    print("\n========== AGENT TRACE ==========")

    for message in messages:
        if isinstance(message, AIMessage):
            if message.tool_calls:
                for index, tool_call in enumerate(message.tool_calls, start=1):
                    tool_name = tool_call["name"]
                    tool_args = tool_call.get("args", {})
                    called_tools.append(tool_name)

                    print(f"[CALL {index}] {tool_name}")
                    print(f"  Args: {format_tool_args(tool_args)}")
            elif message.content:
                print("[AI FINAL]")
                print(f"  {message.content}")

        elif isinstance(message, ToolMessage):
            print(f"[RESULT] {message.name}")
            print(f"  {message.content}")

    return called_tools


def run_multi_tool_agent():
    agent = build_agent()

    query = (
        "Tôi muốn mua 2 bàn phím cơ K8, "
        "tôi là thành viên gold và muốn giao đến Hà Nội. "
        "Hãy tính tổng số tiền cuối cùng tôi phải trả."
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        }
    )

    called_tools = print_agent_trace(result["messages"])

    print("\n========== FINAL ANSWER ==========")
    print(result["messages"][-1].content)

    validate_tool_calls(called_tools)


def validate_tool_calls(called_tools: list[str]) -> None:
    """
    Kiểm tra agent có thực sự gọi đủ các tool không.
    """

    required_tools = {
        "get_product_info",
        "get_member_discount",
        "get_shipping_fee",
        "calculate_final_total",
    }

    missing_tools = required_tools - set(called_tools)

    assert not missing_tools, (
        f"Agent chưa gọi đủ tool. Thiếu: {missing_tools}. "
        f"Thực tế đã gọi: {called_tools}"
    )

    assert called_tools[0] == "get_product_info", (
        "Tool đầu tiên phải là get_product_info."
    )

    assert called_tools[-1] == "calculate_final_total", (
        "Tool cuối cùng phải là calculate_final_total."
    )

    print("\nKiểm tra thành công: agent đã gọi đủ 4 tool.")


if __name__ == "__main__":
    run_multi_tool_agent()
