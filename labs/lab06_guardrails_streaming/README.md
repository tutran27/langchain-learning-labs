# Lab 06 · Guardrails & Streaming

> 🛡️ Khu vực thực hành streaming output và guardrails cho ứng dụng LLM.

## 📂 Nội dung hiện có

| File | Trạng thái | Cách chạy |
| --- | --- | --- |
| `model_and_agent_streaming.py` | ✅ Đã có demo stream output từ model và agent, đồng thời in tiến trình gọi tool theo event stream | `python -m labs.lab06_guardrails_streaming.model_and_agent_streaming` |
| `tool_retry.py` | ✅ Đã có demo retry tool bằng `ToolRetryMiddleware` với lỗi tạm thời từ API giả lập | `python -m labs.lab06_guardrails_streaming.tool_retry` |

## 📌 Ghi chú

- `model_and_agent_streaming.py` phù hợp để quan sát sự khác nhau giữa `llm.stream(...)` và `agent.stream(...)`, cũng như cách đọc event `updates` và `messages`.
- `tool_retry.py` minh họa cách middleware tự retry khi tool ném `ConnectionError`, rất hữu ích cho các tool gọi API ngoài.
- Lab này hiện đã có code một phần. Các chủ đề như `PII guardrail`, `human approval` hay custom progress stream riêng vẫn chưa được bổ sung thành file độc lập.
