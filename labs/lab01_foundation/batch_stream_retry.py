from langchain_core.runnables import RunnableLambda

from labs.lab01_foundation.llm_model import LLMModel
from labs.lab01_foundation.prompt_template import (
    _build_chat_prompt_template,
)


def _print_section(title: str):
    print(f"\n{'=' * 12} {title} {'=' * 12}")


def build_chain():
    model_wrapper = LLMModel()
    tokenizer = model_wrapper.tokenizer
    llm = model_wrapper.hf_pipeline()

    prompt_step = RunnableLambda(
        lambda x: _build_chat_prompt_template(
            x["bot_name"],
            x["question"],
            tokenizer,
        )
    )

    return prompt_step | llm


def run_batch():
    chain = build_chain()
    inputs = [
        {"bot_name": "Javie", "question": "Python là gì?"},
        {"bot_name": "Javie", "question": "LCEL dùng để làm gì?"},
        {"bot_name": "Javie", "question": "Ví dụ về LangChain chain đơn giản."},
    ]

    responses = chain.batch(inputs, config={"max_concurrency": 2})
    for index, response in enumerate(responses, start=1):
        print(f"[batch {index}] {response}")


def run_stream():
    chain = build_chain()
    stream_input = {
        "bot_name": "Javie",
        "question": "Hãy giải thích ngắn gọn stream trong LangChain.",
    }

    for chunk in chain.stream(stream_input):
        print(chunk, end="", flush=True)
    print()


def run_retry():
    model_wrapper = LLMModel()
    tokenizer = model_wrapper.tokenizer
    llm = model_wrapper.hf_pipeline()

    state = {"attempt": 0}

    def flaky_step(data):
        state["attempt"] += 1
        print(f"Lần thử {state['attempt']}")

        if state["attempt"] < 3:
            raise ValueError("Temporary prompt formatting error")

        return data

    retry_chain = (
        RunnableLambda(flaky_step).with_retry(stop_after_attempt=3)
        | RunnableLambda(
            lambda x: _build_chat_prompt_template(
                x["bot_name"],
                x["question"],
                tokenizer,
            )
        )
        | llm
    )

    response = retry_chain.invoke(
        {
            "bot_name": "Javie",
            "question": "Hãy cho một ví dụ ngắn gọn về retry.",
        }
    )
    print(response)


if __name__ == "__main__":
    _print_section("Batch")
    run_batch()
    _print_section("Stream")
    run_stream()
    _print_section("Retry")
    run_retry()
