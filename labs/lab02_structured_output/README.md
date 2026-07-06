# Lab 02 · Structured Output

> 🧾 Làm việc với output có cấu trúc: từ text thô, JSON parser đến các workflow classification, extraction và routing.

## 🎯 Mục tiêu

- Parse output text cơ bản
- Parse JSON bằng schema
- Áp dụng structured output cho classification
- Trích xuất thông tin thành object có cấu trúc
- Route yêu cầu theo schema trước khi xử lý tiếp

## 📂 Nội dung hiện có

| File | Mô tả | Cách chạy |
| --- | --- |
| `str_output_parser.py` | Parse output dạng text đơn giản | `python -m labs.lab02_structured_output.str_output_parser` |
| `json_output_parser.py` | Parse output JSON với `JsonOutputParser` và schema Pydantic | `python -m labs.lab02_structured_output.json_output_parser` |
| `classification_chain.py` | Phân loại yêu cầu theo category, sentiment và priority | `python -m labs.lab02_structured_output.classification_chain` |
| `extraction_chain.py` | Trích xuất thông tin khách hàng từ yêu cầu tự nhiên | `python -m labs.lab02_structured_output.extraction_chain` |
| `multi_extraction_chain.py` | Trích xuất nhiều trường thông tin hơn trong một flow | `python -m labs.lab02_structured_output.multi_extraction_chain` |
| `routing_chain.py` | Route yêu cầu theo schema trước khi sinh response | `python -m labs.lab02_structured_output.routing_chain` |
| `prompt.py` | Prompt dùng chung cho routing | Không chạy trực tiếp |

## ⚠️ Lưu ý

- Structured output phụ thuộc nhiều vào việc prompt chèn đúng format instructions.
- Với model có reasoning, nên bóc phần response cuối trước khi parse JSON.
