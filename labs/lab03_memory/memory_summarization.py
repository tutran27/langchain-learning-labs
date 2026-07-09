from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda

from labs.lab01_foundation.llm_model import LLMModel
from shared.utils import _langchain_to_hf_prompt, add_tokenize, print_messages, to_text


def load_llm_bundle():
    model_wrapper = LLMModel()
    return model_wrapper.hf_pipeline(), model_wrapper.tokenizer


def build_llm_chain(prompt, llm, tokenizer, parser=None):
    chain = (
        prompt
        | RunnableLambda(lambda x: x.to_messages())
        | RunnableLambda(_langchain_to_hf_prompt)
        | RunnableLambda(add_tokenize)
        | llm
    )

    if parser is not None:
        chain = chain | parser

    return chain

def summarize_old_messages(llm, tokenizer, old_messages):
    parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
Bạn là hệ thống nén memory hội thoại.

Hãy tóm tắt thật ngắn gọn và chính xác:
- Tên người dùng
- Mục tiêu học
- Sở thích trả lời
- Các chủ đề đã nhắc đến

Chỉ giữ thông tin cần thiết để dùng lại.
Không thêm thông tin không có trong hội thoại.
""",
            ),
            (
                "human",
                """
Hội thoại cần tóm tắt:

{conversation}
""",
            ),
        ]
    )

    conversation = "\n".join(f"{message.type}: {message.content}" for message in old_messages)
    chain = build_llm_chain(prompt, llm, tokenizer, parser)
    return chain.invoke({"conversation": conversation})


def main(session_id):
    llm, tokenizer = load_llm_bundle()

    history = []
    summary = None

    while True:
        if len(history) >= 10:
            summary = summarize_old_messages(llm, tokenizer, history[-10:-4])
            recent_messages = history[-4:]

            print(f"\n=== Memory Summary ===")
            print(summary)

            history = [HumanMessage(content=f"Memory summary: {summary}")]+ recent_messages
        else:
            recent_messages = history[-4:]
            summary=[f"{msg.type}: {msg.content}" for msg in history]

        query=str(input("You: "))
        if query.lower() == "exit" or query.lower() == "quit":
            break

        prompt = ChatPromptTemplate.from_messages(
        [ 
            (
                "system",
                """
Bạn là trợ lý học tập AI.

Memory summary:
{summary}

Hãy dùng memory summary và các tin nhắn gần nhất để trả lời ngắn gọn, chính xác, đúng trọng tâm.
Ưu tiên dùng lại thông tin đã xuất hiện trước đó nếu câu hỏi có liên quan.
""",
            ),
            MessagesPlaceholder(variable_name="recent_messages"),
            ("human", "{input}"),
        ]
    )
        chain = build_llm_chain(prompt, llm, tokenizer)
        response = chain.invoke({"summary": summary, 
                                 "recent_messages": recent_messages, 
                                 "input": query})
        
        history.append(HumanMessage(content=query))
        history.append(AIMessage(content=response))
        print("🤖 AI: ", response)


if __name__ == "__main__":
    llm, tokenizer = load_llm_bundle()

    messages = [
        SystemMessage(content="Bạn là trợ lý học tập AI."),
        HumanMessage(content="Tên tôi là Thái."),
        AIMessage(content="Chào Thái, tôi sẽ hỗ trợ bạn học AI."),
        HumanMessage(content="Tôi đang ôn LangChain."),
        AIMessage(content="LangChain là framework để xây dựng ứng dụng LLM."),
        HumanMessage(content="Tôi muốn học tiếp Tool Calling."),
        AIMessage(content="Tool Calling giúp LLM gọi hàm hoặc API bên ngoài."),
        HumanMessage(content="Sau đó tôi muốn học LangGraph."),
        AIMessage(content="LangGraph giúp xây workflow/agent bằng graph state."),
        HumanMessage(content="Tôi thích câu trả lời có ví dụ code ngắn."),
        AIMessage(content="Đã hiểu, tôi sẽ ưu tiên ví dụ code ngắn."),
    ]

    summary = summarize_old_messages(llm, tokenizer, messages[-10:-4])
    recent_messages = messages[-4:]

    print("=== Recent Messages ===")
    print_messages(recent_messages)

    print("\n=== Memory Summary ===")
    print(summary)