from typing import Optional

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field

from labs.lab01_foundation.llm_model import LLMModel
from shared.utils import (
    _langchain_to_hf_prompt,
    add_tokenize,
    beauty_json_output,
    extract_response,
)


class CustomerInfo(BaseModel):
    customer_name: Optional[str] = Field(description="Tên khách hàng nếu có")
    email: Optional[str] = Field(description="Email khách hàng nếu có")
    phone: Optional[str] = Field(description="Số điện thoại nếu có")
    appointment_date: Optional[str] = Field(description="Ngày hẹn dạng YYYY-MM-DD nếu có")
    appointment_time: Optional[str] = Field(description="Giờ hẹn dạng HH:MM nếu có")
    request_summary: str = Field(description="Tóm tắt yêu cầu của khách hàng")


def _output_parser():
    return JsonOutputParser(pydantic_object=CustomerInfo)


def _build_prompt(text, tokenizer, output_parser):
    system_prompt = """
    Bạn là một trợ lý AI của công ty PNV Tech chuyên dùng trích xuất thông tin từ yêu cầu của khách hàng.
    Nhiệm vụ của bạn là trích xuất thông tin theo các field cho trước và trả về đúng format JSON.
    Chỉ trả về duy nhất một JSON object hợp lệ.
    Không giải thích, không phân tích, không thêm ghi chú, không thêm markdown, không thêm văn bản ngoài JSON.
    Field nào không có thông tin hoặc thông tin không rõ ràng thì để chuỗi rỗng "".
    Không được tự suy diễn thêm thông tin ngoài nội dung đầu vào.
    Mục tiêu là phải đúng format.
    {format_instruction}
    """
    messages = [
        ("system", system_prompt),
        ("user", "{text}"),
    ]
    messages_chain = ChatPromptTemplate.from_messages(messages)
    prompt_format = messages_chain.format_prompt(
        text=text,
        format_instruction=output_parser.get_format_instructions(),
    )
    prompt_converted = _langchain_to_hf_prompt(prompt_format.to_messages())
    prompt_tokenized = add_tokenize(prompt_converted, tokenizer)
    return prompt_tokenized


def build_chain():
    model_wrapper = LLMModel()
    tokenizer = model_wrapper.tokenizer
    llm = model_wrapper.hf_pipeline()
    output_parser = _output_parser()
    chain = (
        RunnableLambda(lambda x: _build_prompt(x["text"], tokenizer, output_parser))
        | llm
        | RunnableLambda(extract_response)
        | output_parser
    )
    return chain


if __name__ == "__main__":
    text = """
    Khách hàng Nguyễn Văn A, email nguyenvana@gmail.com, số điện thoại 0987654321.
    Khách muốn đặt lịch tư vấn vào ngày 15/07/2026 lúc 9h sáng về dịch vụ chatbot.
    """

    chain = build_chain()
    result = chain.invoke({"text": text})
    beauty_json_output(result)
