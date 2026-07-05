# LangChain Learning Labs

> 🚀 Bộ bài thực hành LangChain theo hướng học từng bước, từ nền tảng đến các workflow nâng cao như structured output, tools, memory, RAG và agentic patterns.

## 🎯 Mục tiêu

Repository này được xây dựng để:

- Học LangChain theo từng lab nhỏ, dễ chạy và dễ mở rộng
- Thực hành trực tiếp với Hugging Face model, prompt và LCEL
- Làm quen với structured output, parser và schema
- Chuẩn bị nền tảng cho các bài về agent, memory, RAG và guardrails

## 🗂️ Cấu trúc thư mục

| Thư mục | Vai trò |
| --- | --- |
| `labs/` | Khu vực bài thực hành chính, chia theo từng chủ đề |
| `shared/` | Các thành phần dùng chung như config, utility, helper |
| `projects/` | Khu vực dành cho project hoặc demo lớn hơn |
| `tests/` | Khu vực dành cho test |

## 📚 Hệ thống Lab

Hiện tại repo tập trung trước vào:

- `lab01_foundation`: model, prompt, LCEL, batch/stream/retry
- `lab02_structured_output`: string parser, JSON parser, classification

Các nhóm lab tiếp theo đã có khung README và sẽ được bổ sung dần:

- `lab03_tools_agents`
- `lab04_memory`
- `lab05_rag`
- `lab06_guardrails_streaming`
- `lab07_agentic_patterns`

Xem thêm tại: [labs/README.md](D:/AI_LABs/langchain-learning-labs/labs/README.md)

## ⚙️ Cài đặt

Từ root project:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nếu dùng GPU NVIDIA, nên đảm bảo bộ `torch / torchvision / torchaudio` được cài đồng bộ theo đúng CUDA runtime.

## ▶️ Chạy thử

```powershell
python -m labs.lab01_foundation.lab_03_chain_lcel.lcel_basic
python -m labs.lab01_foundation.lab_04_batch_stream_retry.batch_stream_retry
python -m labs.lab02_structured_output.lab_01_basic_schema.json_output_parser
```

## 📝 Ghi chú

- Repo hiện ưu tiên flow học tập và khả năng đọc code hơn là tối ưu production.
- Một số môi trường Windows + CUDA có thể cần tinh chỉnh thêm dependency để tránh xung đột thư viện native.
