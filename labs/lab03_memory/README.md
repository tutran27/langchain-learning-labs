# Lab 03 · Memory

> 🧠 Khu vực thực hành các pattern memory cho ứng dụng LLM, từ lưu lịch sử ngắn hạn đến tóm tắt hội thoại.

## 📂 Nội dung hiện có

| File | Trạng thái | Cách chạy |
| --- | --- | --- |
| `short_term_memory.py` | ✅ Đã có demo hội thoại có nhớ lịch sử | `python -m labs.lab03_memory.short_term_memory` |
| `memory_summarization.py` | 🟡 Đã có logic tóm tắt memory, cần tiếp tục hoàn thiện | `python -m labs.lab03_memory.memory_summarization` |
| `long_term_preferences.py` | 🧩 Placeholder | `python -m labs.lab03_memory.long_term_preferences` |

## 📝 Ghi chú

- `short_term_memory.py` đang dùng `RunnableWithMessageHistory` để mô phỏng hội thoại nhiều lượt.
- `memory_summarization.py` đã có hướng tiếp cận tóm tắt lịch sử hội thoại khi message dài dần.
- Lab này hiện ở trạng thái có code một phần, phù hợp để tiếp tục mở rộng thêm preference memory hoặc multi-user session.
