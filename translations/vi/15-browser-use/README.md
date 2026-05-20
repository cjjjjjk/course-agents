# Xây dựng Computer Use Agents (CUA)

Computer use agents có thể tương tác với website giống như con người: mở trình duyệt, quan sát trang và chọn hành động tiếp theo dựa trên những gì hiển thị. Bài học này tập trung vào kiến trúc của một agent tự động hóa trình duyệt dùng để tìm kiếm thông tin, trích xuất dữ liệu có cấu trúc và đưa ra quyết định nghiệp vụ.

Mẫu kiến trúc kết hợp Browser-Use cho điều hướng linh hoạt, Playwright và Chrome DevTools Protocol cho điều khiển trình duyệt, mô hình thị giác cho suy luận trên giao diện, và schema có cấu trúc để chuẩn hóa dữ liệu trích xuất.

## Giới thiệu

Bài học này bao gồm:

- Khi nào computer use agent phù hợp hơn tự động hóa chỉ dựa trên API.
- Cách kết hợp agent điều hướng với điều khiển trình duyệt tất định.
- Cách dùng mô hình thị giác và output có cấu trúc để trích xuất dữ liệu từ trang web động.
- Cách chọn giữa agent-first, actor-first và workflow hybrid.

## Mục tiêu học tập

Sau bài học này, bạn sẽ biết:

- Nhận diện nhiệm vụ trình duyệt phù hợp với computer use agent.
- Thiết kế workflow điều hướng trang web có thể xử lý UI động.
- Chuyển nội dung nhìn thấy trên trang thành dữ liệu có cấu trúc.
- Cân bằng giữa tính linh hoạt của agent và tính chính xác của actor.

## Tổng quan kiến trúc

Mẫu này dùng workflow tự động hóa trình duyệt dạng hybrid:

1. Trình duyệt được mở với khả năng điều khiển từ bên ngoài để agent và actor có thể dùng chung phiên làm việc.
2. Agent xử lý các tác vụ mở như tìm kiếm, đóng popup, đọc trạng thái UI và chọn bước tiếp theo.
3. Khi cấu trúc trang đã ổn định, actor hoặc logic tất định trích xuất các trường dữ liệu quan trọng.
4. Logic nghiệp vụ so sánh dữ liệu đã trích xuất và đưa ra kết quả cuối.

Cách tiếp cận này giữ được khả năng thích nghi của agent với giao diện động, đồng thời vẫn dùng điều khiển tất định cho các phần cần độ chính xác cao.

## Khi nào dùng Agent và Actor

| Tình huống | Dùng agent | Dùng actor |
| --- | --- | --- |
| Layout động | Phù hợp vì agent có thể thích nghi | Dễ hỏng nếu selector thay đổi |
| Cấu trúc đã biết | Chậm hơn cần thiết | Phù hợp vì nhanh và chính xác |
| Tìm phần tử bằng ngữ nghĩa | Phù hợp với ngôn ngữ tự nhiên | Khó nếu không có selector rõ |
| Kiểm soát thời gian | Kém dự đoán hơn | Kiểm soát wait và retry tốt hơn |
| Workflow nhiều trạng thái bất ngờ | Phù hợp | Cần nhiều nhánh xử lý thủ công |

## Thực hành thiết kế tốt

1. Bắt đầu bằng agent khi cần khám phá UI hoặc xử lý giao diện động.
2. Chuyển sang actor khi thao tác đã có cấu trúc rõ ràng.
3. Dùng schema có cấu trúc để dữ liệu trích xuất có thể kiểm chứng.
4. Thiết kế fallback cho popup, thay đổi layout và trạng thái tải chậm.
5. Tách rõ phần quan sát, phần hành động và phần ra quyết định.
