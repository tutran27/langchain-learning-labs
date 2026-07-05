# Lab 01 · Foundation

> 🧱 Nền tảng để làm quen với model, tokenizer, prompt template, LCEL và các pattern chạy cơ bản trong LangChain.

## 🎯 Mục tiêu

Lab này giúp bạn nắm được các khối cơ bản nhất trước khi đi sang structured output, tools hay agent:

- Khởi tạo LLM và tokenizer từ Hugging Face
- Chuẩn hóa prompt cho chat model
- Kết nối các bước bằng LCEL
- Thử các cách chạy như `invoke`, `batch`, `stream`, `retry`

## 📂 Nội dung hiện có

| Bài | File chính | Mô tả |
| --- | --- | --- |
| `lab_01_chat_model` | `llm_model.py` | Wrapper load model, tokenizer và HuggingFace pipeline |
| `lab_02_messages_and_prompts` | `prompt_template.py` | Xây dựng prompt template và chat prompt template |
| `lab_03_chain_lcel` | `lcel_basic.py` | Chain cơ bản với `RunnableLambda` và LLM |
| `lab_04_batch_stream_retry` | `batch_stream_retry.py` | Demo `batch`, `stream` và `retry` |

## 🧠 Kiến thức chính

- `ChatPromptTemplate`
- `RunnableLambda`
- Hugging Face pipeline integration
- Chat template cho tokenizer
- `chain.invoke()`, `chain.batch()`, `chain.stream()`, `with_retry()`

## ▶️ Cách chạy

```powershell
python -m labs.lab01_foundation.lab_01_chat_model.llm_model
python -m labs.lab01_foundation.lab_02_messages_and_prompts.prompt_template
python -m labs.lab01_foundation.lab_03_chain_lcel.lcel_basic
python -m labs.lab01_foundation.lab_04_batch_stream_retry.batch_stream_retry
```

## ✅ Trạng thái

Lab này đã có code nền để học và thử nghiệm. Một số phần cấu hình môi trường GPU/transformers có thể cần tinh chỉnh thêm tùy máy.
