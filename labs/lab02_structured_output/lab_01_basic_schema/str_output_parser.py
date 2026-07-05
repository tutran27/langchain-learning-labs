from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from labs.lab01_foundation.lab_01_chat_model.llm_model import LLMModel
from labs.lab01_foundation.lab_02_messages_and_prompts.prompt_template import _build_chat_prompt_template

def chain_lcel(bot_name: str, question: str):
    output_parser = StrOutputParser()
    
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
        | output_parser
    )
    print("Build chain successfully")

    print("Chain response...")
    result=chain.invoke({"bot_name": bot_name, "question": question})
    return result
    
if __name__ == "__main__":
    bot_name = "Javie"
    question = "Hãy cho tôi biết về cấu trúc của một function trong Python?"
    result = chain_lcel(bot_name, question)
    print("\n" + "=" * 50 + "\n")
    print(result)
    
