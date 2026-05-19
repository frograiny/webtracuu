CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ

Sau khi hoàn tất quá trình lập trình (Coding), hệ thống phải trải qua giai đoạn Kiểm thử (Testing) nghiêm ngặt để đảm bảo đáp ứng đúng và đủ các yêu cầu nghiệp vụ cũng như yêu cầu phi chức năng (hiệu năng, bảo mật) đã đề ra ở Chương 2.

5.1 Chiến lược kiểm thử
Dự án áp dụng mô hình Kim tự tháp kiểm thử (Testing Pyramid) bao gồm 3 cấp độ:
1. Unit Test (Kiểm thử mức đơn vị): Sử dụng thư viện `pytest` của Python để kiểm thử các hàm logic lõi độc lập, ví dụ hàm tính toán mã băm mật khẩu, hàm chuẩn hóa chuỗi tiếng Việt.
2. Integration Test (Kiểm thử tích hợp): Kiểm tra sự giao tiếp giữa FastAPI và Cơ sở dữ liệu/Redis. Mức này kiểm chứng xem việc "Duyệt đề tài" có thực sự kích hoạt lệnh "Xóa Cache" trên Redis hay không.
3. System Test & Load Test (Kiểm thử hệ thống và chịu tải): Sử dụng công cụ `JMeter` để bắn hàng ngàn Request giả lập cùng lúc nhằm đo lường khả năng chịu tải và kiểm chứng thuật toán Rate Limiting.

5.2 Một số ca kiểm thử tiêu biểu (Test Cases)
Dưới đây là trích xuất một số kịch bản kiểm thử (Test Cases) quan trọng nhất đã được thực thi.

**TC01: Kiểm thử Xác thực - Đăng nhập sai mật khẩu (Bảo mật)**
- **ID:** TC_AUTH_01
- **Mô tả:** Đảm bảo hệ thống từ chối quyền truy cập khi người dùng nhập sai mật khẩu và không rò rỉ thông tin (không báo lỗi "Email không tồn tại" để tránh hacker rà quét email).
- **Các bước thực hiện:**
  1. Gửi POST Request đến `/api/v1/auth/login`.
  2. Truyền JSON Body với Email hợp lệ nhưng Password cố tình điền sai.
- **Kết quả mong đợi:**
  - HTTP Status: 401 Unauthorized.
  - Thông báo: "Tài khoản hoặc mật khẩu không chính xác".
- **Trạng thái:** PASS (Đạt).

**TC02: Kiểm thử Tìm kiếm mờ - Fuzzy Search (Hiệu năng & Logic)**
- **ID:** TC_SEARCH_02
- **Mô tả:** Kiểm tra bộ máy tìm kiếm có khả năng chịu lỗi chính tả nhờ thuật toán Trigram Index hay không.
- **Các bước thực hiện:**
  1. Đảm bảo trong DB có một đề tài tên "Trí tuệ nhân tạo".
  2. Gửi GET Request tìm kiếm với từ khóa cố tình gõ sai một ký tự: `?q=Tri tue nhan taoo` (Dư chữ 'o').
- **Kết quả mong đợi:**
  - HTTP Status: 200 OK.
  - Kết quả trả về phải chứa đề tài "Trí tuệ nhân tạo" nhưng điểm xếp hạng (Relevance Score) thấp hơn so với khi gõ đúng hoàn toàn.
  - Thời gian trễ (Latency) < 100ms.
- **Trạng thái:** PASS (Đạt - Phản hồi trong 65ms).

**TC03: Kiểm thử Ràng buộc Dữ liệu - File đính kèm quá khổ (Validation)**
- **ID:** TC_UPLOAD_03
- **Mô tả:** Đảm bảo hệ thống chặn đứng các Request mang Payload quá lớn để tránh nghẽn băng thông.
- **Các bước thực hiện:**
  1. Đăng nhập với tư cách Tác giả lấy Token.
  2. Gửi POST Request nộp đề tài, đính kèm file PDF nặng 60MB (Vượt giới hạn 50MB).
- **Kết quả mong đợi:**
  - Kết nối bị ngắt ngay lập tức ở tầng Nginx/Middleware.
  - HTTP Status: 413 Payload Too Large.
  - File không được lưu vào ổ cứng Server.
- **Trạng thái:** PASS (Đạt).

**TC04: Kiểm thử Tính nhất quán Dữ liệu - Xóa Cache sau phê duyệt (Integration)**
- **ID:** TC_ADMIN_04
- **Mô tả:** Đảm bảo khi Admin duyệt bài, người dùng lập tức tìm thấy bài đó mà không bị vướng dữ liệu cũ trên Redis.
- **Các bước thực hiện:**
  1. Dùng User tìm từ khóa "Blockchain". Hệ thống trả về 5 kết quả (Dữ liệu bị lưu vào Cache Redis).
  2. Đăng nhập Admin, phê duyệt 1 đề tài mới cứng cũng có chữ "Blockchain".
  3. Dùng User tìm lại từ khóa "Blockchain" ngay lập tức.
- **Kết quả mong đợi:**
  - Ở bước 3, hệ thống phải trả về 6 kết quả. (Nghĩa là API đã xóa thành công Cache cũ ở bước 2, buộc hệ thống phải quét lại DB lấy dữ liệu mới nhất).
- **Trạng thái:** PASS (Đạt).

5.3 Đánh giá kết quả
Dự án đã đáp ứng hoàn toàn các mục tiêu đề ra ở Chương 1:
- Hiệu năng (Performance): Tốc độ truy vấn FTS trung bình giảm từ >1200ms (của hệ thống Monolith cũ) xuống còn trung bình 45ms (Cache Miss) và <5ms (Cache Hit). 
- Khả năng mở rộng (Scalability): Hệ thống đã được Container hóa 100%. Quá trình triển khai lên các máy chủ mới chỉ mất chưa đến 5 phút chạy lệnh `docker-compose up`.
- Tính ổn định: Thuật toán Rate Limiting hoạt động chính xác, bảo vệ thành công DB trước các bài test DDoS mô phỏng bằng JMeter (bắn 500 requests/giây).

5.4 Giao diện hệ thống
Do hệ thống tập trung vào kiến trúc Backend API, giao diện trình diễn chính bao gồm:
1. OpenAPI (Swagger UI): Hệ thống cung cấp tài liệu API tương tác trực quan tại `/docs`. Tại đây, lập trình viên Frontend có thể đọc hiểu đặc tả, bấm nút "Try it out" để gọi thử API ngay trên trình duyệt mà không cần cài đặt phần mềm phụ trợ (như Postman).
2. Grafana Dashboard (Trang quản trị vận hành): Hiển thị biểu đồ theo thời gian thực về RAM, CPU của các Container, số lượng Request/giây (RPS), và cảnh báo (Alert) màu đỏ khi số lượng lỗi HTTP 500 vượt ngưỡng cho phép.

---

CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

6.1 Kết luận
Dự án "VNU Research Repository (Enterprise Edition)" đã thực hiện thành công việc tái cấu trúc toàn diện hệ thống quản lý học thuật. Việc mạnh dạn đập bỏ những truy vấn SQL truyền thống kỹ thuật thấp để chuyển sang kiến trúc Hướng dịch vụ (SOA) kết hợp bộ nhớ đệm phân tán (Redis) và Chỉ mục toàn văn (FTS) đã mang lại sự cải thiện hiệu năng mang tính đột phá. Hệ thống không chỉ giải quyết được "nỗi đau" về tốc độ tra cứu chậm chạp của sinh viên, mà còn cung cấp một nền tảng quản trị bảo mật cao, có quy trình nghiệp vụ rõ ràng cho cán bộ nhà trường.

6.2 Hướng phát triển
Dù đã đạt tiêu chuẩn đưa vào vận hành thực tế (Production-ready), hệ thống vẫn có tiềm năng mở rộng rất lớn trong tương lai:

1. Nâng cấp bộ máy Tìm kiếm bằng AI/NLP: 
Hiện tại hệ thống mới chỉ dừng ở mức tìm kiếm chuỗi (Lexical Search) bằng Trigram. Trong giai đoạn 2, có thể tích hợp mô hình Ngôn ngữ lớn (như BERT hoặc Sentence Transformers) để áp dụng Tìm kiếm theo ngữ nghĩa (Semantic Vector Search). Khi đó, người dùng gõ "học sâu" hệ thống vẫn tự động trả về các bài viết có chữ "deep learning".

2. Chuyển đổi sang Elasticsearch:
Nếu khối lượng đề tài nghiên cứu vượt qua con số 50 triệu bản ghi, việc chỉ dùng PostgreSQL có thể bắt đầu bộc lộ độ trễ. Khi đó, hệ thống sẽ được cấu hình công cụ Change Data Capture (CDC - như Debezium) để đồng bộ dữ liệu thời gian thực từ PostgreSQL sang một cụm Elasticsearch chuyên dụng. (Kiến trúc Clean Architecture hiện tại cho phép việc thay đổi Database này diễn ra mà không làm vỡ các module khác).

3. Triển khai lên Kubernetes (K8s):
Thay vì triển khai bằng Docker Compose tĩnh, toàn bộ hệ thống sẽ được đóng gói thành các Helm Charts để ném lên nền tảng đám mây (Cloud) như AWS hoặc Google Cloud. K8s sẽ tự động Scale (nhân bản thêm các Pod FastAPI) vào thời điểm sinh viên truy cập đông và thu hẹp lại vào ban đêm để tiết kiệm chi phí.
