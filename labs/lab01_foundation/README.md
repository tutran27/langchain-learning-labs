# Lab 01 · Foundation

> 🧱 Nền tảng để làm quen với model wrapper, tokenizer, prompt, LCEL và các pattern chạy cơ bản trong LangChain.

## 🎯 Mục tiêu

- Khởi tạo LLM từ Hugging Face local model.
- Chuẩn hóa prompt cho chat flow.
- Kết nối các bước xử lý bằng LCEL.
- Làm quen với `invoke`, `batch`, `stream` và `retry`.

## 📂 Nội dung hiện có

| File | Mô tả | Cách chạy |
| --- | --- | --- |
| `llm_model.py` | Wrapper cho Hugging Face local model và Groq chat model | `python -m labs.lab01_foundation.llm_model` |
| `prompt_template.py` | Demo `PromptTemplate` và `ChatPromptTemplate` | `python -m labs.lab01_foundation.prompt_template` |
| `lcel_basic.py` | Chain cơ bản với LCEL | `python -m labs.lab01_foundation.lcel_basic` |
| `batch_stream_retry.py` | Demo `batch`, `stream` và `retry` | `python -m labs.lab01_foundation.batch_stream_retry` |

## 🧩 Ghi chú về model wrapper

File `llm_model.py` hiện tách thành 2 class:

- `HFLLMModel`: dùng cho Hugging Face local pipeline.
- `GroqLLMModel`: dùng cho Groq API chat model.

Thiết kế này giúp các lab chọn đúng provider theo nhu cầu mà không phải tải local model khi chỉ cần gọi API.

## ✅ Trạng thái

Lab này đã có code nền ổn để làm điểm xuất phát cho các lab phía sau.
