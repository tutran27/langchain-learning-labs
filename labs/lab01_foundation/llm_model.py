import torch
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline,
)

from shared.config import settings

load_dotenv()


class HFLLMModel:
    def __init__(self):
        self.device = settings.DEVICE
        self.hf_token = settings.HF_TOKEN or None
        self.llm = None
        self.chat_llm = None

        self.tokenizer = AutoTokenizer.from_pretrained(
            settings.LLM_MODEL,
            use_fast=False,
            token=self.hf_token,
        )

        self.quantization_enabled = settings.QUANT_TYPE

        if self.quantization_enabled:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.LLM_MODEL,
                quantization_config=bnb_config,
                token=self.hf_token,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.LLM_MODEL,
                token=self.hf_token,
            )

    def hf_pipeline(self, llm_chat=False):
        if self.llm is None:
            model_pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                dtype=torch.bfloat16,
                device_map="auto",
                return_full_text=False,
                clean_up_tokenization_spaces=False,
                max_new_tokens=2048,
            )

            self.llm = HuggingFacePipeline(pipeline=model_pipeline)

        if llm_chat:
            if self.chat_llm is None:
                self.chat_llm = ChatHuggingFace(llm=self.llm)
            return self.chat_llm

        return self.llm

    def invoke(self, prompt):
        return self.hf_pipeline().invoke(prompt)


class GroqLLMModel:
    def __init__(self):
        self.groq_llm = None

    def groq_chat(self):
        if self.groq_llm is None:
            from langchain_groq import ChatGroq

            self.groq_llm = ChatGroq(
                model=settings.GROQ_MODEL,
                api_key=settings.GROQ_API_KEY,
            )

        return self.groq_llm

    def invoke(self, prompt):
        return self.groq_chat().invoke(prompt)


if __name__ == "__main__":
    model = HFLLMModel()
    print(model.invoke("Hi, how are you?"))
