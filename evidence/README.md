# Evidence — Day 22: LLMOps & Prompt Versioning

## Liên kết và trạng thái nộp bài

- LangSmith project: https://smith.langchain.com/o/28779693-61c6-4f7a-bf0c-ca09109225e5/projects/p/38d7b5b4-3652-4e6f-b9ac-ab572cf7fd53?runview=traces
- `05_langsmith_project_traces.png`: dashboard ghi nhận 958 traces trong 7 ngày.
- Đã có đủ 7 file evidence không rỗng. Tuy nhiên, `02_prompt_hub.png` hiện chụp
  danh sách project; cần thay bằng ảnh trang Prompts hiển thị hai prompt
  `phong-rag-prompt-v1` và `phong-rag-prompt-v2` trước khi nộp.
- Bốn bước đã có kết quả chạy riêng; bước 04 đã chạy qua `run_all.py --step 4`.
  Chưa xác nhận một lần chạy API thật liên tục bằng `run_all.py` cho cả bốn bước.
- Repo cần tên theo mẫu `K4-L3-DAY22-HoVaTen-MSSV-LLMOpsPromptVersioning`.

## Kết quả RAGAS

Nguồn số liệu: `03_ragas_report.json`, được sao chép từ `data/ragas_report.json`.
Ảnh `03_ragas_scores.png` ghi lại bảng so sánh V1/V2 của lần chạy này.

| Metric | V1 | V2 | Kết quả |
|---|---:|---:|---|
| Faithfulness | 0.9505 | 0.9081 | V1 cao hơn |
| Answer relevancy | 0.9061 | 0.8928 | V1 cao hơn |
| Context recall | 1.0000 | 1.0000 | Bằng nhau |
| Context precision | 0.9439 | 0.9483 | V2 cao hơn |

Cả hai phiên bản đạt mục tiêu faithfulness ≥ 0.8. Trong lần đánh giá này,
V1 trả lời ngắn gọn có điểm faithfulness và answer relevancy cao hơn V2.
V2 có điểm context precision nhỉnh hơn, trong khi context recall bằng nhau.
Nếu ưu tiên câu trả lời ngắn và có căn cứ, các điểm hiện tại ủng hộ V1.

Các điểm không chứng minh rằng độ dài câu trả lời là nguyên nhân của khác biệt.
Hai phiên bản dùng cùng FAISS index và cấu hình retrieval, nên khác biệt nhỏ
ở các chỉ số retrieval cũng có thể đến từ phán đoán của LLM chấm điểm.
Script loại điểm thiếu/NaN khỏi trung bình và thông báo số mẫu hợp lệ trong terminal;
báo cáo JSON hiện không lưu số mẫu hợp lệ, nên cần đọc kèm log khi đánh giá độ đầy đủ.

`03_ragas_v1_scores.png` và `03_ragas_v1_summary.json` là bằng chứng của lần chạy
trước bị lỗi ở V2. Chúng không phải số liệu V1 của bảng so sánh cuối cùng.

## Guardrails

- `04_pii_demo_log.txt`: 6 trường hợp, gồm email, điện thoại, SSN, thẻ tín dụng,
  nhiều PII và văn bản sạch. Kiểm tra đầu ra xác nhận PII được che và văn bản sạch giữ nguyên.
- `04_json_demo_log.txt`: 5 trường hợp, gồm JSON hợp lệ, markdown fences,
  nháy đơn, dấu phẩy thừa và đầu vào không thể sửa. Mọi đầu ra đều parse được thành JSON;
  trường hợp cuối trả về đối tượng dự phòng với trường `error` và `raw`.

Các validator do bài lab tự triển khai. `OnFailAction.FIX` sử dụng
`FailResult(fix_value=...)` để thay thế đầu ra. Logic regex và sửa JSON ở đây
phục vụ các định dạng trong demo, chưa bao quát mọi loại PII hoặc JSON lỗi.
