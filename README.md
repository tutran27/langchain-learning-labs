# LangChain Learning Labs

> 🚀 Bộ bài thực hành LangChain theo lộ trình tăng dần, từ nền tảng cơ bản đến structured output, memory, RAG, tools và agentic patterns.

## 🎯 Mục tiêu

Repository này được tổ chức để:

- Học LangChain theo từng lab nhỏ, dễ chạy và dễ mở rộng.
- Thực hành trực tiếp với Hugging Face local model và Groq API model.
- Làm quen với prompt, LCEL, parser, schema và tool calling.
- Chuẩn bị nền tảng cho các bài nâng cao như memory, RAG, guardrails và agent workflow.

## 🗂️ Cấu trúc dự án

| Thư mục | Vai trò |
| --- | --- |
| `labs/` | Khu vực bài thực hành chính theo từng chủ đề |
| `shared/` | Config, utils và helper dùng chung |
| `projects/` | Khu vực cho mini project hoặc demo hoàn chỉnh hơn |
| `tests/` | Nơi đặt test hoặc smoke test khi cần |

## 🧭 Lộ trình học

- `lab01_foundation`
- `lab02_structured_output`
- `lab03_memory`
- `lab04_rag`
- `lab05_tools_agents`
- `lab06_guardrails_streaming`
- `lab07_agentic_patterns`

Xem chi tiết tại [labs/README.md](D:/AI_LABs/langchain-learning-labs/labs/README.md).

## ⚙️ Cài đặt

Khuyến nghị dùng môi trường `conda` tên `langchain` hoặc virtual environment riêng.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nếu bạn dùng `conda`:

```powershell
conda create -n langchain python=3.11 -y
conda activate langchain
pip install -r requirements.txt
```

## 🔐 Biến môi trường

File `.env` nên có các biến sau tùy theo bài lab bạn chạy:

- `HF_TOKEN`: token cho model Hugging Face gated hoặc private.
- `GROQ_API_KEY`: API key để gọi Groq.
- `TAVILY_API_KEY`: API key cho tool search.

## ▶️ Chạy nhanh

```powershell
python -m labs.lab01_foundation.prompt_template
python -m labs.lab01_foundation.lcel_basic
python -m labs.lab02_structured_output.json_output_parser
python -m labs.lab05_tools_agents.create_agent
```

## 📌 Ghi chú

- Repo ưu tiên tính học tập, dễ đọc và dễ thực nghiệm hơn là tối ưu production.
- Một số lab đã có code chạy được, một số lab vẫn đang ở trạng thái placeholder để hoàn thiện dần.
- Lab `create_agent` hiện đang dùng Groq model, trong khi các bài foundation chủ yếu minh họa luồng Hugging Face local.
