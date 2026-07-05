# Labs Overview

> 📘 Bộ bài thực hành LangChain được tổ chức theo từng chủ đề, đi từ nền tảng đến các pattern ứng dụng nâng cao.

## 🎯 Mục tiêu

Thư mục `labs/` là khu vực thực hành chính của dự án, tập trung vào:

- Làm quen với mô hình ngôn ngữ, prompt và LCEL
- Làm việc với structured output
- Xây dựng agent, memory, RAG và guardrails
- Từng bước ghép các thành phần thành workflow hoàn chỉnh

## 🗂️ Danh sách Lab

| Lab | Chủ đề | Trạng thái |
| --- | --- | --- |
| `lab01_foundation` | Nền tảng LangChain, prompt, LCEL, batch/stream/retry | ✅ Đã có code |
| `lab02_structured_output` | String parser, JSON parser, classification output | ✅ Đã có code |
| `lab03_tools_agents` | Tools và agent | 🚧 Đang cập nhật |
| `lab04_memory` | Short-term và long-term memory | 🚧 Đang cập nhật |
| `lab05_rag` | Retrieval-Augmented Generation | 🚧 Đang cập nhật |
| `lab06_guardrails_streaming` | Guardrails và streaming | 🚧 Đang cập nhật |
| `lab07_agentic_patterns` | Các pattern agentic nâng cao | 🚧 Đang cập nhật |

## 📌 Gợi ý học

Thứ tự nên đi:

1. `lab01_foundation`
2. `lab02_structured_output`
3. `lab03_tools_agents`
4. `lab04_memory`
5. `lab05_rag`
6. `lab06_guardrails_streaming`
7. `lab07_agentic_patterns`

## 🧪 Cách chạy

Luôn đứng ở thư mục root của project:

```powershell
python -m labs.lab01_foundation.lab_03_chain_lcel.lcel_basic
python -m labs.lab02_structured_output.lab_01_basic_schema.json_output_parser
```

## 📝 Ghi chú

- Một số lab đang trong quá trình hoàn thiện nội dung và README chi tiết.
- Các ví dụ hiện tại ưu tiên tính dễ đọc và khả năng học từng bước hơn là tối ưu production.
