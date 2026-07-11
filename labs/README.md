# Labs Overview

> 📘 Toàn bộ bài thực hành được chia theo chủ đề lớn, với cấu trúc file phẳng để dễ điều hướng và dễ chạy trực tiếp bằng `python -m`.

## 🧭 Lộ trình học gợi ý

1. `lab01_foundation`
2. `lab02_structured_output`
3. `lab03_memory`
4. `lab04_rag`
5. `lab05_tools_agents`
6. `lab06_guardrails_streaming`
7. `lab07_agentic_patterns`

## 🗂️ Danh sách lab

| Lab | Chủ đề | Trạng thái |
| --- | --- | --- |
| `lab01_foundation` | Model wrapper, prompt, LCEL, batch, stream, retry | ✅ Có code |
| `lab02_structured_output` | Parser, JSON schema, classification, extraction, routing | ✅ Có code |
| `lab03_memory` | Short-term memory, memory summarization, preference memory | 🟡 Có code một phần |
| `lab04_rag` | Retrieval-Augmented Generation | 🧩 Placeholder |
| `lab05_tools_agents` | Tool definition, agent creation, tool logging | ✅ Có code |
| `lab06_guardrails_streaming` | Guardrails và streaming | 🧩 Placeholder |
| `lab07_agentic_patterns` | Agentic patterns nâng cao | 🧩 Placeholder |

## ▶️ Ví dụ lệnh chạy

```powershell
python -m labs.lab01_foundation.llm_model
python -m labs.lab01_foundation.lcel_basic
python -m labs.lab02_structured_output.classification_chain
python -m labs.lab03_memory.short_term_memory
python -m labs.lab05_tools_agents.create_agent
```

## 📌 Ghi chú

- Các lab đã có code hiện đặt file trực tiếp trong thư mục lab cha.
- `lab05_tools_agents` đã được cập nhật lại README để phản ánh đúng các file đã có code như Pydantic tool schema, manual tool calling, multi-tool agent và runtime context.
- Những lab chưa hoàn thiện vẫn giữ placeholder rõ ràng để dễ mở rộng sau này.
