from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field

from labs.lab01_foundation.lab_01_chat_model.llm_model import LLMModel
from labs.lab01_foundation.lab_02_messages_and_prompts.prompt_template import (
    _build_chat_prompt_template,
)
from shared.utils import beauty_json_output

class Answer(BaseModel):
    answer: str = Field(description="The answer to the question")
    confidence: float = Field(description="The confidence of the answer")


def _output_parser():
    return JsonOutputParser(pydantic_object=Answer)


def chain_lcel(bot_name: str, question: str):
    output_parser = _output_parser()

    print("Loading model...")
    model_wrapper = LLMModel()
    tokenizer = model_wrapper.tokenizer
    llm = model_wrapper.hf_pipeline()
    print("Load model successfully")

    print("Building chain...")
    chain = (
        RunnableLambda(
            lambda x: _build_chat_prompt_template(
                x["bot_name"],
                x["question"],
                tokenizer,
                output_parser.get_format_instructions(),
            )
        )
        | llm
        | output_parser
    )
    print("Build chain successfully")

    print("Chain response...")
    result = chain.invoke({"bot_name": bot_name, "question": question})
    return result


if __name__ == "__main__":
    bot_name = "Javie"
    question = (
        "Langchain là gì?"
    )
    result = chain_lcel(bot_name, question)
    beauty_json_output(result)
