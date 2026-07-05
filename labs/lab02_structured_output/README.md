# Lab 02 · Structured Output

> 🧾 Làm việc với output có cấu trúc: từ text thô, JSON parser đến các schema phục vụ phân loại thông tin.

## 🎯 Mục tiêu

Lab này tập trung vào việc buộc model trả về dữ liệu có format rõ ràng để dễ parse và dễ tích hợp vào workflow:

- Parse output text cơ bản
- Parse JSON bằng schema
- Áp dụng structured output cho bài toán classification

## 📂 Nội dung hiện có

| Bài | File chính | Mô tả |
| --- | --- | --- |
| `lab_01_basic_schema` | `str_output_parser.py` | Parse output dạng text đơn giản |
| `lab_01_basic_schema` | `json_output_parser.py` | Parse output JSON với `JsonOutputParser` và schema Pydantic |
| `lab_02_classification` | `classification_chain.py` | Phân loại ticket theo category, sentiment và priority |

## 🧠 Kiến thức chính

- `JsonOutputParser`
- Pydantic schema
- Format instructions cho model
- Structured classification pipeline

## ▶️ Cách chạy

```powershell
python -m labs.lab02_structured_output.lab_01_basic_schema.str_output_parser
python -m labs.lab02_structured_output.lab_01_basic_schema.json_output_parser
python -m labs.lab02_structured_output.lab_02_classification.classification_chain
```

## ⚠️ Lưu ý

- Structured output phụ thuộc nhiều vào việc prompt có chèn đúng `format instructions`.
- Nếu model không tuân thủ chặt JSON, parser có thể fail và cần tăng mức ràng buộc trong prompt.
