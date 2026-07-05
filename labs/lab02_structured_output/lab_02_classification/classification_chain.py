from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from pydantic import BaseModel, Field

from labs.lab01_foundation.lab_01_chat_model.llm_model import LLMModel
from shared.utils import beauty_json_output, _langchain_to_hf_prompt, add_tokenize

from typing import Literal
from pydantic import BaseModel, Field


class TicketClassification(BaseModel):
    category: Literal["technical_support","billing","sales","general_question","other"] = Field(description="Loại yêu cầu của người dùng")
    sentiment: Literal["positive","neutral","negative"] = Field(description="Cảm xúc của người dùng")
    priority: Literal["low","medium","high"] = Field(description="Mức độ ưu tiên xử lý")
    reason: str = Field(description="Lý do ngắn gọn chọn category và priority")

def _output_parser():
    return JsonOutputParser(pydantic_object=TicketClassification)

def _build_prompt(question, tokenizer, format_instruction=""):
    messages = [
        ("system", """Bạn là một AI chuyên dùng phân loại thông tin theo các field nhất định. 
                    Nhiệm vụ của bạn là phân loại thông tin theo các field cho trước và trả về theo format json.
                    {format_instruction}
        """),
        ("user", """{question}"""),
    ]
    
    messages_chain = ChatPromptTemplate.from_messages(messages)
    prompt_format=messages_chain.format_prompt(
        question=question, 
        format_instruction=format_instruction
        )
    prompt_converted = _langchain_to_hf_prompt(prompt_format.to_messages())
    prompt_tokenized = add_tokenize(prompt_converted, tokenizer)
    return prompt_tokenized


def build_chain():
    model_wrapper = LLMModel()
    tokenizer = model_wrapper.tokenizer
    llm = model_wrapper.hf_pipeline()

    chain=RunnableLambda(
        lambda x: _build_prompt(x["question"], tokenizer, _output_parser().get_format_instructions())) | llm | _output_parser()

    return chain

if __name__ == "__main__":
    question = "Tôi muốn hỏi về giá sản phẩm của công ty?"
    chain = build_chain()
    result = chain.invoke({"question": question})
    beauty_json_output(result)