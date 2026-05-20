# Bảo mật AI Agents

Bảo mật agentic systems cần xem xét cả mô hình, công cụ, dữ liệu, quyền truy cập và chuỗi hành động mà agent có thể tạo ra. Bài học này tóm tắt các rủi ro chính và phương pháp thiết kế để giảm thiểu nguy cơ khi đưa AI agent vào môi trường thật.

## Mục tiêu học tập

Sau bài học này, bạn sẽ hiểu:

- Những bề mặt tấn công phổ biến trong hệ thống AI agent.
- Vì sao tool use, memory, retrieval và multi-agent workflow cần kiểm soát quyền rõ ràng.
- Cách thiết kế xác thực, ủy quyền, audit trail và giới hạn hành động.
- Cách dùng bằng chứng, chữ ký hoặc log bất biến để phát hiện dữ liệu bị thay đổi.

## Các rủi ro chính

| Rủi ro | Ý nghĩa | Hướng giảm thiểu |
| --- | --- | --- |
| Prompt injection | Nội dung bên ngoài cố gắng điều khiển agent làm sai mục tiêu | Tách instruction tin cậy và dữ liệu không tin cậy, kiểm tra tool call |
| Tool misuse | Agent gọi công cụ vượt quyền hoặc sai ngữ cảnh | Áp dụng least privilege, allowlist, approval gate |
| Data leakage | Agent tiết lộ dữ liệu nhạy cảm từ context, memory hoặc retrieval | Phân loại dữ liệu, masking, policy kiểm soát output |
| Tampering | Dữ liệu đầu vào, receipt, log hoặc kết quả bị chỉnh sửa | Dùng chữ ký, hash chain, audit log |
| Over-automation | Agent thực hiện hành động có tác động lớn mà thiếu kiểm soát | Human-in-the-loop cho hành động rủi ro cao |

## Nguyên tắc thiết kế

1. Xem mọi dữ liệu bên ngoài là không tin cậy cho đến khi được kiểm chứng.
2. Cấp quyền theo từng công cụ, từng môi trường và từng loại hành động.
3. Ghi lại quyết định quan trọng, tool call, input và output phục vụ audit.
4. Thêm cơ chế phê duyệt cho hành động có chi phí, rủi ro pháp lý hoặc tác động sản xuất.
5. Kiểm thử prompt injection, dữ liệu độc hại và tình huống tool failure trước khi triển khai.

## Liên hệ với các bài học khác

- [Building Trustworthy AI Agents](../06-building-trustworthy-agents/README.md)
- [AI Agents in Production](../10-ai-agents-production/README.md)
- [Context Engineering for AI Agents](../12-context-engineering/README.md)
