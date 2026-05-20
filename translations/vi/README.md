# AI Agents for Beginners

Đây là bản đọc tĩnh của khóa học AI Agents for Beginners, tập trung vào lý thuyết, mẫu thiết kế, kiến trúc và phương pháp triển khai AI agent.

Bản fork này được tối ưu để đọc và nghiên cứu:

- English là nguồn mặc định.
- Nội dung tiếng Việt nằm trong `translations/vi`.
- Website xuất bản được sinh ra từ HTML, CSS và JavaScript thuần.
- Notebook, script Python, mẫu C# và phần thiết lập runtime cục bộ được loại bỏ có chủ đích.

## Đọc khóa học

Các bài học được tổ chức độc lập. Bạn có thể bắt đầu từ phần giới thiệu hoặc đi thẳng vào chủ đề cần nghiên cứu.

| Bài | Chủ đề |
| --- | --- |
| 00 | [Định hướng khóa học](./00-course-setup/README.md) |
| 01 | [Giới thiệu về AI Agents và các trường hợp sử dụng](./01-intro-to-ai-agents/README.md) |
| 02 | [Khám phá các framework agentic](./02-explore-agentic-frameworks/README.md) |
| 03 | [Hiểu các mẫu thiết kế agentic](./03-agentic-design-patterns/README.md) |
| 04 | [Mẫu thiết kế sử dụng công cụ](./04-tool-use/README.md) |
| 05 | [Agentic RAG](./05-agentic-rag/README.md) |
| 06 | [Xây dựng AI agent đáng tin cậy](./06-building-trustworthy-agents/README.md) |
| 07 | [Mẫu thiết kế lập kế hoạch](./07-planning-design/README.md) |
| 08 | [Mẫu thiết kế đa agent](./08-multi-agent/README.md) |
| 09 | [Mẫu thiết kế siêu nhận thức](./09-metacognition/README.md) |
| 10 | [AI agent trong production](./10-ai-agents-production/README.md) |
| 11 | [Giao thức agentic: MCP, A2A và NLWeb](./11-agentic-protocols/README.md) |
| 12 | [Context engineering cho AI agent](./12-context-engineering/README.md) |
| 13 | [Quản lý bộ nhớ agentic](./13-agent-memory/README.md) |
| 14 | [Khám phá Microsoft Agent Framework](./14-microsoft-agent-framework/README.md) |
| 15 | [Xây dựng Computer Use Agents](./15-browser-use/README.md) |
| 18 | [Bảo mật AI agents](./18-securing-ai-agents/README.md) |

## Website tĩnh

GitHub Pages site được build từ Markdown bằng `tools/build_site.py`.

```bash
python tools/build_site.py
```

Output được ghi vào `_site/`:

- `/` chuyển về `/en/`.
- `/en/` là khóa học tiếng Anh.
- `/vi/` là khóa học tiếng Việt.

Website runtime không dùng React, Vue, MkDocs, Docusaurus, Jekyll hoặc frontend framework khác.

## Chính sách nội dung

Bản fork này phục vụ đọc lý thuyết. Khi đóng góp, hãy giữ đúng mục tiêu đó:

- Ưu tiên giải thích, sơ đồ, ví dụ khái niệm và hướng dẫn triển khai ở mức phương pháp.
- Không thêm notebook hoặc mẫu ứng dụng có thể chạy.
- Link nội bộ trong bài học nên trỏ tới các trang tài liệu có thể đọc được.
- Giữ điều hướng English và tiếng Việt đồng bộ khi thêm hoặc bỏ bài học.

## Ghi nhận

Repository này được fork từ khóa học Microsoft AI Agents for Beginners. Tài liệu gốc, nhãn hiệu và tài sản bên thứ ba vẫn tuân theo giấy phép và chính sách tương ứng.
