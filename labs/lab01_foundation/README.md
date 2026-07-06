# Lab 01 · Foundation

> 🧱 Nền tảng để làm quen với model, tokenizer, prompt, LCEL và các pattern chạy cơ bản trong LangChain.

## 🎯 Mục tiêu

- Khởi tạo LLM và tokenizer từ Hugging Face
- Chuẩn hóa prompt cho chat model
- Kết nối các bước bằng LCEL
- Thử các cách chạy như `invoke`, `batch`, `stream`, `retry`

## 📂 Nội dung hiện có

| File | Mô tả | Cách chạy |
| --- | --- |
| `llm_model.py` | Wrapper load model, tokenizer và Hugging Face pipeline | `python -m labs.lab01_foundation.llm_model` |
| `prompt_template.py` | Xây dựng prompt template và chat prompt template | `python -m labs.lab01_foundation.prompt_template` |
| `lcel_basic.py` | Chain cơ bản với `RunnableLambda` và LLM | `python -m labs.lab01_foundation.lcel_basic` |
| `batch_stream_retry.py` | Demo `batch`, `stream` và `retry` | `python -m labs.lab01_foundation.batch_stream_retry` |

## ✅ Trạng thái

Lab này đã có code nền để học và thử nghiệm trực tiếp.
