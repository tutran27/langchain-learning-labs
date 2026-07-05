from langchain_core.prompts import ChatPromptTemplate

from shared.utils import _langchain_to_hf_prompt, add_tokenize
from labs.lab01_foundation.lab_01_chat_model.llm_model import LLMModel


def _build_prompt_template(bot_name, question):
    prompt_template = """<|im_start|>user
    You are a helpful assistant. Your name is {bot_name}.
    You're a teacher for students in Viet Nam.
    You're explaining Python programming for students.

    Question: {question}

    Answer: <|im_end|>
    <|im_start|>assistant
    """
    template = ChatPromptTemplate.from_template(prompt_template)
    prompt = template.format_messages(
        bot_name=bot_name,
        question=question,
    )
    return prompt


def _build_chat_prompt_template(bot_name, question, tokenizer, output_parser=""):
    template = [
        (
            "system",
            "You are a helpful assistant. Your name is {bot_name}.\n{output_parser}",
        ),
        ("user", "{question}"),
    ]

    chat_prompt_template = ChatPromptTemplate.from_messages(template)
    prompt = chat_prompt_template.format_messages(
        bot_name=bot_name,
        question=question,
        output_parser=output_parser,
    )

    prompt_converted = _langchain_to_hf_prompt(prompt)
    tokenized_prompt = add_tokenize(prompt_converted, tokenizer)
    return tokenized_prompt


if __name__ == "__main__":
    context = "Ngữ cảnh được cung cấp"
    bot_name = "Javie"
    question = "Xin chào, bạn tên là gì?"

    llm = LLMModel()
    tokenizer = llm.tokenizer

    print("=" * 50)
    print("Prompt Template")
    print("=" * 50)
    prompt = _build_prompt_template(bot_name, question)
    print(prompt)

    print("=" * 50)
    print("Chat Prompt Template")
    print("=" * 50)
    chat_prompt_template = _build_chat_prompt_template(bot_name, question, tokenizer)
    print(chat_prompt_template)
