# Tổng Kết Dự Án: VNU Research Repository (Enterprise Edition)

## 1. Bối cảnh
Dự án được khởi tạo như một hệ thống Web API phục vụ việc tra cứu đề tài nghiên cứu khoa học. Tuy nhiên, nó đã được tái cấu trúc toàn diện qua 4 Giai đoạn (Phases) để chuyển mình từ một dự án "Lab/Prototype" thành một hệ thống mang chuẩn mực **Enterprise Production**.

## 2. Kiến trúc Hệ Thống
Hệ thống sử dụng kiến trúc Microservices cơ bản vận hành qua Docker Compose:
- **Backend:** FastAPI (Python) - Đảm nhận logic nghiệp vụ, Rate Limiting, và API.
- **Frontend:** React + Vite - Cung cấp giao diện người dùng.
- **Database:** PostgreSQL - Lưu trữ dữ liệu và xử lý Full-Text Search.
- **Cache & Session:** Redis - Phân tán bộ đệm và quản lý Auth Blacklist.
- **Observability:** Prometheus & Grafana - Giám sát sức khỏe hệ thống (Metrics).

## 3. Các Tính Năng Kỹ Thuật Đột Phá
Thay vì sử dụng các vòng lặp `LIKE` chậm chạp hay in-memory cache gây thất thoát dữ liệu, hệ thống tự hào sở hữu các đặc tính của một hệ thống quy mô lớn:

### 3.1. Nghệ Thuật Tìm Kiếm (Search Engine)
- **PostgreSQL FTS (Full-Text Search):** Tận dụng kiểu dữ liệu `TSVECTOR` và toán tử `@@` kết hợp với index GIN để tốc độ tìm kiếm đạt O(log N).
- **Ranking (ts_rank) & Field Boosting:** Kết quả khớp Tiêu đề luôn được xếp hạng cao hơn Tác giả nhờ cơ chế đánh trọng số `setweight(A/C)`.
- **Fuzzy Search (pg_trgm):** Tích hợp thuật toán Trigram để vượt qua các lỗi gõ sai chính tả của người dùng.
- **Synonyms Rewrite:** Tự động dịch các từ khóa viết tắt ("AI" -> "Trí tuệ nhân tạo") ngay ở tầng Backend.

### 3.2. Chiến Lược Bộ Đệm (Cache Strategy)
- **Redis Distributed Cache:** Bộ đệm được lưu tập trung trên Redis, cho phép scale Backend thành nhiều instance mà không lo mất cache.
- **Smart Key Normalization:** Các từ khóa tìm kiếm (như " AI y học " và "ai y hoc") được chuẩn hóa về một định dạng duy nhất trước khi tra cứu cache, tối đa hóa Hit-rate.
- **Event-driven Invalidation:** Mỗi khi có thay đổi từ Admin (Thêm/Sửa/Xóa đề tài), hệ thống tự động bắn Background Task gõ cửa Redis để xóa ngay bộ đệm cũ, đảm bảo Data Consistency.

### 3.3. Bảo Mật & Xác Thực (Enterprise Auth)
- **Dual-Token Lifecycle:** Cấp phát đồng thời `Access Token` (sống ngắn) và `Refresh Token` (sống dài).
- **Revocation & Blacklist:** Khi người dùng Logout, hệ thống lập tức trích xuất JWT ID (JTI) ném vào danh sách đen của Redis, triệt tiêu mọi khả năng sử dụng lại Token cũ.
- **Smart Rate Limiting:** Sử dụng Token để đếm giới hạn cho người dùng đã đăng nhập, và phối hợp `IP + User-Agent` cho khách (Guest) để vượt qua rào cản NAT (Dùng chung mạng nội bộ).

### 3.4. Vận Hành & Giám Sát (Observability)
- **100% Visibility:** FastAPI liên tục bắn các chỉ số đo lường (RPS, Latency) ra `/metrics`. Prometheus thu thập dữ liệu và Grafana trực quan hóa chúng.
- **Business Metrics:** Không chỉ đo hệ thống, Grafana còn cho phép theo dõi `Search Success Rate` (Tỉ lệ tìm kiếm không ra kết quả).
- **Docker Healthcheck:** Docker liên tục ping endpoint `/health` mỗi 30 giây để đảm bảo Backend vẫn còn sống.

## 4. Kết Luận
VNU Research API không chỉ giải quyết bài toán nghiệp vụ tìm kiếm dữ liệu, mà còn đóng vai trò là một "bảo tàng" lưu trữ các best practices về System Design, Caching, và Security.
