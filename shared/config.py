import os 
import torch

class Settings:
    HF_TOKEN = os.getenv("HF_TOKEN","")
    LLM_MODEL = "Qwen/Qwen3.5-4B"
    QUANT_TYPE = True
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    ENABLE_THINKING = True
    
    QDRANT_PATH="./storage/qdrant"
    COLLECTION_NAME="langchain_labs"
    
    EMBED_MODEL = "BAAI/bge-small-en-v1.5"
    DIM=384
    BATCH_SIZE=32
    MAX_SEQ_LEN=512

settings = Settings()

    
