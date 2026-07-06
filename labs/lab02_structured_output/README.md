# Lab 02 · Structured Output

> 🧾 Làm việc với output có cấu trúc: từ text thô, JSON parser đến các workflow classification, extraction và routing.

## 🎯 Mục tiêu

- Parse output text cơ bản
- Parse JSON bằng schema
- Áp dụng structured output cho classification
- Trích xuất thông tin thành object có cấu trúc
- Route yêu cầu theo schema trước khi xử lý tiếp

## 📂 Nội dung hiện có

| File | Mô tả |
| --- | --- |
| `str_output_parser.py` | Parse output dạng text đơn giản |
| `json_output_parser.py` | Parse output JSON với `JsonOutputParser` và schema Pydantic |
| `classification_chain.py` | Phân loại yêu cầu theo category, sentiment và priority |
| `extraction_chain.py` | Trích xuất thông tin khách hàng từ yêu cầu tự nhiên |
| `multi_extraction_chain.py` | Trích xuất nhiều trường thông tin hơn trong một flow |
| `routing_chain.py` | Route yêu cầu theo schema trước khi sinh response |
| `prompt.py` | Prompt dùng chung cho routing |

## ▶️ Cách chạy

```powershell
python -m labs.lab02_structured_output.str_output_parser
python -m labs.lab02_structured_output.json_output_parser
python -m labs.lab02_structured_output.classification_chain
python -m labs.lab02_structured_output.extraction_chain
python -m labs.lab02_structured_output.routing_chain
```

## ⚠️ Lưu ý

- Structured output phụ thuộc nhiều vào việc prompt chèn đúng format instructions.
- Với model có reasoning, nên bóc phần response cuối trước khi parse JSON.
