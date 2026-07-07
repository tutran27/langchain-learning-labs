from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory

from labs.lab01_foundation.llm_model import LLMModel
from shared.utils import _langchain_to_hf_prompt, add_tokenize


STORE = {}


def build_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Bạn là một trợ lý AI. Hãy trả lời ngắn gọn, rõ ràng và có nhớ ngữ cảnh cuộc trò chuyện trước đó.",
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{query}"),
        ]
    )


def get_memory_session(session_id):
    if session_id not in STORE:
        STORE[session_id] = InMemoryChatMessageHistory()
    return STORE[session_id]


def load_llm_bundle():
    model_wrapper = LLMModel()
    llm=model_wrapper.hf_pipeline()
    tokenizer=model_wrapper.tokenizer
    return llm, tokenizer


def build_chain():
    llm, tokenizer = load_llm_bundle()
    prompt = build_prompt()

    chain = (
        prompt
        | RunnableLambda(lambda x: x.to_messages())
        | RunnableLambda(_langchain_to_hf_prompt)
        | RunnableLambda(lambda x: add_tokenize(x, tokenizer))
        | llm
    )

    return RunnableWithMessageHistory(
        chain,
        get_memory_session,
        input_messages_key="query",
        history_messages_key="history",
    )


def main():
    chain = build_chain()
    session_id = "demo-short-term-memory"

    print("=== Short-Term Memory Demo ===")
    print("Nhập `quit` để thoát.\n")

    while True:
        query = input("Bạn: ").strip()
        if not query:
            continue

        if query.lower() == "quit":
            print("Kết thúc phiên chat.")
            break

        response = chain.invoke(
            {"query": query},
            config={"configurable": {"session_id": session_id}},
        )
        print(f"AI: {response}\n")


if __name__ == "__main__":
    main()
