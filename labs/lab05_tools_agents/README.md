# Lab 05 · Tools & Agents

> 🛠️ Khu vực thực hành định nghĩa tool, quan sát log tool usage và xây dựng agent workflow cơ bản.

## 📂 Nội dung hiện có

| File | Trạng thái | Cách chạy |
| --- | --- | --- |
| `basic_tools.py` | ✅ Đã có search tool và arithmetic tool cơ bản | `python -m labs.lab05_tools_agents.basic_tools` |
| `tools_with_pydantic.py` | 🧩 Placeholder | `python -m labs.lab05_tools_agents.tools_with_pydantic` |
| `manual_tool_calling.py` | 🧩 Placeholder | `python -m labs.lab05_tools_agents.manual_tool_calling` |
| `create_agent.py` | ✅ Đã có agent demo dùng Groq model | `python -m labs.lab05_tools_agents.create_agent` |
| `multi_tool_agent.py` | 🧩 Placeholder | `python -m labs.lab05_tools_agents.multi_tool_agent` |
| `tool_runtime_context.py` | 🧩 Placeholder | `python -m labs.lab05_tools_agents.tool_runtime_context` |

## 🔍 Điểm đáng chú ý

- `basic_tools.py` hiện có các tool cơ bản như `search_tool`, `add`, `subtract`.
- `create_agent.py` đang dùng `GroqLLMModel` để test tool-calling theo hướng agent.
- Log trong `create_agent.py` đã được làm gọn hơn để dễ quan sát message flow, `tool_calls` và `invalid_tool_calls`.

## ⚠️ Lưu ý

- Tùy model và integration, agent có thể sinh “tool call dạng text” thay vì structured tool call thật.
- Nếu chạy các ví dụ search, bạn cần có `TAVILY_API_KEY`.
- Nếu chạy agent với Groq, bạn cần có `GROQ_API_KEY`.
