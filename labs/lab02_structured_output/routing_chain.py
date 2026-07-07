from typing import Literal

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field

from labs.lab01_foundation.llm_model import LLMModel
from labs.lab02_structured_output.prompt import (
    ROUTING_PROMPT,
    TASK_PROMPT,
)
from shared.utils import (
    _langchain_to_hf_prompt,
    add_tokenize,
    beauty_json_output,
    extract_response,
)


class RouteDecision(BaseModel):
    route: Literal[
        "qa",
        "summarization",
        "translation",
        "classification",
        "extraction",
        "unknown",
    ] = Field(description="Nhánh xử lý phù hợp")
    reason: str = Field(description="Lý do chọn route")


class Answering(BaseModel):
    question: str = Field(description="Câu hỏi gốc của người dùng")
    response: str = Field(description="Câu trả lời ")

# định nghĩa output parser cho route
def _route_parser():
    return JsonOutputParser(pydantic_object=RouteDecision)

# định nghĩa output parser cho answer
def _answer_parser():
    return JsonOutputParser(pydantic_object=Answering)

# format prompt theo router
def _build_prompt(system_prompt, text, tokenizer, output_parser):
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
    return add_tokenize(prompt_converted, tokenizer)

# lấy model và tokenizer
def _llm_bundle():
    model_wrapper = LLMModel()
    return model_wrapper.tokenizer, model_wrapper.hf_pipeline()

# build route chain
def build_route_chain(tokenizer, llm):
    print("[ROUTE] Building route chain...")
    output_parser = _route_parser()
    return (
        RunnableLambda(
            lambda x: _build_prompt(
                ROUTING_PROMPT,
                x["text"],
                tokenizer,
                output_parser,
            )
        )
        | llm
        | RunnableLambda(extract_response)
        | output_parser
    )


def response_chain(text, route_name, tokenizer, llm):
    print(f"[TASK] Building response chain for route: {route_name}")
    output_parser = _answer_parser()
    system_prompt = TASK_PROMPT.get(route_name, TASK_PROMPT["unknown"])
    chain = (
        RunnableLambda(
            lambda x: _build_prompt(
                system_prompt,
                x["text"],
                tokenizer,
                output_parser,
            )
        )
        | llm
        | RunnableLambda(extract_response)
        | output_parser
    )
    return chain.invoke({"text": text})


def build_chain():
    tokenizer, llm = _llm_bundle()
    route_chain = build_route_chain(tokenizer, llm)

    def _route_and_respond(payload):
        print("[STEP 1] Running route stage...")
        route_result = route_chain.invoke(payload)
        print(f"🤖[ROUTE] RESULT: {route_result}")
        print(f"🤖[ROUTE] Selected: {route_result['route']}")
        
        print("[STEP 2] Running response stage...")
        answer_result = response_chain(
            payload["text"],
            route_result["route"],
            tokenizer,
            llm,
        )
        print(f"🤖[ANSWER] RESULT: {answer_result}")
        print("[DONE] Completed routing workflow.")
        return {
            "route": route_result["route"],
            "reason": route_result["reason"],
            "result": answer_result,
        }

    return RunnableLambda(_route_and_respond)


if __name__ == "__main__":
    text = "Hãy dịch câu sau sang tiếng Anh: Tôi muốn đặt lịch demo sản phẩm vào ngày mai."

    chain = build_chain()
    result = chain.invoke({"text": text})
    beauty_json_output(result)
