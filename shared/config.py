import os 
import torch
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY","")
    HF_TOKEN = os.getenv("HF_TOKEN","")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY","")
    LLM_MODEL = "Qwen/Qwen3-4B-Instruct-2507"
    GROQ_MODEL = "llama-3.1-8b-instant"
    QUANT_TYPE = True
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    ENABLE_THINKING = True
    
    QDRANT_PATH="./storage/qdrant"
    COLLECTION_NAME="langchain_labs"
    
    EMBED_MODEL = "BAAI/bge-small-en-v1.5"
    DIM=384
    BATCH_SIZE=32
    MAX_SEQ_LEN=512

    APP_ID=os.getenv("APP_ID")

settings = Settings()

    
