import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from langchain_huggingface import HuggingFacePipeline

from shared.config import settings
from dotenv import load_dotenv

load_dotenv()

class LLMModel:
    def __init__(self):
        self.device = settings.DEVICE
        self.hf_token = settings.HF_TOKEN or None
        self.llm = None
        
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
                bnb_4bit_compute_dtype=torch.bfloat16
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

    def hf_pipeline(self):
        if self.llm is None:
            model_pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                dtype=torch.bfloat16,
                device_map="auto",
                return_full_text=False,
                clean_up_tokenization_spaces=False,
                max_new_tokens=512,
            )
            self.llm = HuggingFacePipeline(pipeline=model_pipeline)

        return self.llm

    def invoke(self, prompt):
        return self.hf_pipeline().invoke(prompt)
        
if __name__ == "__main__":
    model = LLMModel()
    print(model.invoke("Hi, how are you?"))
