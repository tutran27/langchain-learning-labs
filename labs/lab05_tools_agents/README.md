# Lab 05 · Tools & Agents

> 🛠️ Khu vực thực hành định nghĩa tool, quan sát log tool usage và xây dựng agent workflow cơ bản.

## 📂 Nội dung hiện có

| File | Trạng thái | Cách chạy |
| --- | --- | --- |
| `basic_tools.py` | ✅ Đã có search tool và arithmetic tool cơ bản | `python -m labs.lab05_tools_agents.basic_tools` |
| `tools_with_pydantic.py` | ✅ Đã có demo `args_schema`, `Enum`, `Literal` và validate input bằng Pydantic | `python -m labs.lab05_tools_agents.tools_with_pydantic` |
| `manual_tool_calling.py` | ✅ Đã có demo bind tools, đọc `tool_calls`, gọi tool thủ công và ghép `ToolMessage` | `python -m labs.lab05_tools_agents.manual_tool_calling` |
| `create_agent.py` | ✅ Đã có agent demo dùng Groq model | `python -m labs.lab05_tools_agents.create_agent` |
| `multi_tool_agent.py` | ✅ Đã có agent nhiều bước để lấy thông tin sản phẩm, giảm giá, phí ship và tính tổng tiền | `python -m labs.lab05_tools_agents.multi_tool_agent` |
| `tool_runtime_context.py` | ✅ Đã có demo runtime context, phân quyền `customer`/`admin` và kiểm soát truy cập tool theo `user_id` | `python -m labs.lab05_tools_agents.tool_runtime_context` |

## 🔍 Điểm đáng chú ý

- `basic_tools.py` hiện có các tool cơ bản như `search_tool`, `add`, `subtract`.
- `tools_with_pydantic.py` minh họa cách ràng buộc dữ liệu đầu vào cho tool bằng `BaseModel`, `Field`, `Enum` và `model_validator`.
- `manual_tool_calling.py` phù hợp để quan sát rõ chu trình model sinh `tool_calls` rồi backend tự thực thi tool.
- `create_agent.py` đang dùng `GroqLLMModel` để test tool-calling theo hướng agent.
- `multi_tool_agent.py` minh họa orchestration nhiều tool theo thứ tự cố định và có kiểm tra lại chuỗi tool đã gọi.
- Log trong `create_agent.py` đã được làm gọn hơn để dễ quan sát message flow, `tool_calls` và `invalid_tool_calls`.
- `tool_runtime_context.py` minh họa cách truyền `user_id` và `role` từ backend vào `ToolRuntime`, giúp model không phải tự suy đoán danh tính người dùng.
- Với `tool_runtime_context.py`, nên siết `system_prompt` để model chọn đúng tool, chỉ bám theo dữ liệu tool trả về và không tự suy diễn khi `success=False`.

## ⚠️ Lưu ý

- Tùy model và integration, agent có thể sinh “tool call dạng text” thay vì structured tool call thật.
- Nếu chạy các ví dụ search, bạn cần có `TAVILY_API_KEY`.
- Nếu chạy agent với Groq, bạn cần có `GROQ_API_KEY`.
- Nếu câu trả lời cuối không khớp với dữ liệu giả lập, hãy kiểm tra payload của tool trước. Trong các bài demo phân quyền, lỗi thường nằm ở bước model diễn giải lại kết quả tool, không phải ở dữ liệu `runtime context`.
