# LangChain Learning Labs

> 🚀 Bộ bài thực hành LangChain theo hướng học từng bước, từ foundation đến structured output, memory, RAG, tools và agentic patterns.

## 🎯 Mục tiêu

Repository này được tổ chức để:

- Học LangChain theo từng lab nhỏ, dễ chạy và dễ mở rộng
- Thực hành trực tiếp với Hugging Face model, prompt và LCEL
- Làm quen với structured output, parser và schema
- Chuẩn bị nền tảng cho agent, memory, RAG và guardrails

## 🗂️ Cấu trúc dự án

| Thư mục | Vai trò |
| --- | --- |
| `labs/` | Khu vực bài thực hành chính |
| `shared/` | Config, utils và helper dùng chung |
| `projects/` | Khu vực dành cho project/demo lớn hơn |
| `tests/` | Khu vực test |

## 📚 Hệ thống Lab

Các lab hiện tại đã được làm phẳng cấu trúc: mỗi lab chỉ còn một cấp file `.py` trong thư mục cha, giúp code dễ tìm và dễ chạy hơn.

- `lab01_foundation`
- `lab02_structured_output`
- `lab03_memory`
- `lab04_rag`
- `lab05_tools_agents`
- `lab06_guardrails_streaming`
- `lab07_agentic_patterns`

Xem tổng quan đầy đủ tại [labs/README.md](D:/AI_LABs/langchain-learning-labs/labs/README.md).

## ⚙️ Cài đặt

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nếu dùng GPU NVIDIA, nên đảm bảo bộ `torch / torchvision / torchaudio` được cài đồng bộ theo đúng CUDA runtime.

## ▶️ Chạy nhanh

```powershell
python -m labs.lab01_foundation.lcel_basic
python -m labs.lab01_foundation.batch_stream_retry
python -m labs.lab02_structured_output.json_output_parser
python -m labs.lab02_structured_output.routing_chain
```

## 📓 Google Colab

- [Open in Colab](https://colab.research.google.com/drive/1zXc0W-qR1r0n4Tu4KS7yD_T7KAfLwMIt?authuser=4#scrollTo=Jp4Y_gGBP_EW)

## 📝 Ghi chú

- Repo ưu tiên flow học tập và khả năng đọc code hơn là tối ưu production.
- Một số lab mới đang ở trạng thái placeholder để giữ cấu trúc đồng nhất trước khi triển khai nội dung chi tiết.
