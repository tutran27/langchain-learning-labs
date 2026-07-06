from langchain_core.runnables import RunnableLambda

from labs.lab01_foundation.llm_model import LLMModel
from labs.lab01_foundation.prompt_template import (
    _build_chat_prompt_template,
)


def chain_lcel():
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
            )
        )
        | llm
    )
    print("Build chain successfully")
    return chain


if __name__ == "__main__":
    question = "Xin chào, Javie!"
    bot_name = "Javie"
    response = chain_lcel()
    response = response.invoke({"bot_name": bot_name, "question": question})
    print(response)
