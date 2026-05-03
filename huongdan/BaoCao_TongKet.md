# BÁO CÁO TỔNG KẾT DỰ ÁN
**Tên dự án:** Hệ thống Web Tra cứu Đề tài Nghiên cứu Khoa học (VNU Research API)
**Mục tiêu:** Xây dựng nền tảng tra cứu, quản lý và lưu trữ các đề tài NCKH dành cho giảng viên và sinh viên, tối ưu hóa tốc độ tìm kiếm văn bản Tiếng Việt.

---

## 1. Kiến trúc Hệ thống (System Architecture)

Dự án được xây dựng theo mô hình **Client-Server** hiện đại, phân tách rõ ràng giữa Frontend và Backend, hỗ trợ đóng gói và triển khai tự động qua Docker.

### 1.1. Backend (Lõi xử lý & API)
- **Framework chính:** `FastAPI` (Python) - Đảm bảo hiệu năng xử lý cao, hỗ trợ bất đồng bộ (Asynchronous) và tự động sinh tài liệu chuẩn OpenAPI (Swagger UI).
- **Cơ sở dữ liệu:** `PostgreSQL` (môi trường Production qua Docker) và `SQLite` (môi trường Local/Dev).
- **ORM & Quản lý Schema:** Sử dụng `SQLAlchemy` để giao tiếp với database an toàn, chống SQL Injection. Quản lý lịch sử thay đổi cấu trúc database bằng `Alembic`.
- **Bảo mật & Xác thực:** 
  - Đăng nhập, phân quyền bằng **JWT (JSON Web Token)**.
  - Mật khẩu người dùng được băm (hash) bảo mật bằng thuật toán **Bcrypt**.
  - Tích hợp CORS Policy hỗ trợ giao tiếp chéo domain an toàn.

### 1.2. Frontend (Giao diện người dùng)
- **Công nghệ lõi:** `React.js` kết hợp với `TypeScript` đảm bảo tính chặt chẽ về kiểu dữ liệu (Type-safety).
- **Build tool:** Sử dụng `Vite` giúp khởi động server dev cực nhanh và tối ưu dung lượng bản build.
- **Tương tác API:** Quản lý HTTP requests thông qua `Axios` với interceptor tự động gắn JWT Token vào mọi request.

### 1.3. Cơ sở hạ tầng (Infrastructure)
- **Containerization:** Toàn bộ hệ thống (Frontend, Backend, Database) được đóng gói bằng `Docker`. 
- Quản lý và liên kết các container thông qua `docker-compose.yml`, giúp việc khởi chạy dự án chỉ bằng 1 câu lệnh duy nhất.

---

## 2. Các Tính Năng Cốt Lõi Đã Hoàn Thiện

### 2.1. Thuật toán Tìm kiếm Tiếng Việt Nâng cao (Core Innovation)
Thuật toán tìm kiếm là điểm sáng lớn nhất của dự án, giải quyết được bài toán tìm kiếm Tiếng Việt phức tạp mà không phụ thuộc vào các extension nặng nề của hệ quản trị CSDL.

- **Cơ chế Tiền xử lý (Pre-computing & Normalization):**
  - Hệ thống tự động lắng nghe (Event Listener) mọi thao tác thêm/sửa dữ liệu để tự động tạo ra bản sao không dấu chữ thường (Ví dụ: "Trí tuệ nhân tạo" $\rightarrow$ "tri tue nhan tao").
  - Lưu vào 2 cột index: `title_normalized` và `author_normalized`. Việc này chuyển thao tác xử lý chuỗi nặng nề từ lúc *Tra cứu (Runtime)* sang lúc *Lưu trữ (Insert/Update)*, giúp giảm tải CPU database xuống mức tối thiểu.
  
- **Thuật toán Chấm điểm Đơn luồng (Single-pass Token Scoring):**
  - Tách từ khóa đầu vào thành các token.
  - Quét qua database **1 lần duy nhất** (thay vì 2 queries như mô hình FTS + Fallback truyền thống).
  - Áp dụng trọng số thông minh: Từ khóa xuất hiện ở Tiêu đề (+3 điểm), ở Tên Tác giả (+1 điểm). Khớp chính xác cả cụm từ (+5 điểm).
  - Tự động sắp xếp kết quả trả về theo Điểm liên quan (Relevance Score) giảm dần.
  - **Kết quả:** Xử lý triệt để bài toán tìm kiếm có dấu, không dấu, và sai chính tả nhẹ (Fuzzy search) với tốc độ $O(\log n)$.

### 2.2. Hệ thống Lọc Đa chiều (Advanced Filtering)
Người dùng có thể tra cứu kết hợp nhiều điều kiện cùng lúc:
- **Lĩnh vực (Field):** Công nghệ thông tin, Kinh tế, Tâm lý học...
- **Đối tượng (Target Audience):** Sinh viên, Giảng viên.
- **Năm thực hiện (Year):** Lọc theo mốc thời gian.
- **Loại tài liệu (Document Type):** Đề tài NCKH, Dự án, Sản phẩm...

### 2.3. Pydantic Response Schema & API Design
- Áp dụng thiết kế API chuẩn RESTful.
- Toàn bộ kết quả trả về được đi qua lớp lọc `Pydantic`. Điều này không chỉ giúp loại bỏ các dữ liệu rác (Data Leakage) mà còn tạo ra bộ tài liệu API tự động hoàn hảo, giúp team Frontend dễ dàng tích hợp.

### 2.4. Quản trị Người dùng (Auth System)
- Đăng ký, Đăng nhập với luồng cấp phát Access Token.
- Hỗ trợ Role-based (Admin, Viewer). User đầu tiên đăng ký hệ thống mặc định sẽ được cấp quyền Admin.

---

## 3. Quá trình Tối ưu và Refactor
Dự án đã trải qua quá trình tái cấu trúc (Refactor) mạnh mẽ để đạt được trạng thái hiện tại:
1. **Chuyển đổi kiến trúc thư mục:** Từ cấu trúc phẳng sang cấu trúc Module hóa (`app/api/`, `app/core/`, `app/models/`, `app/schemas/`), đạt tiêu chuẩn doanh nghiệp.
2. **Loại bỏ phụ thuộc Postgres Extension:** Thuật toán search ban đầu phụ thuộc vào `to_tsvector` và `pg_trgm` của Postgres khiến việc chạy trên Local (SQLite) gặp lỗi. Việc tạo cột `normalized` đã giải quyết triệt để sự khác biệt môi trường này.
3. **Thêm Endpoint Chi Tiết (`GET /{id}`):** Hoàn thiện mạch trải nghiệm (User Flow) từ bước tìm kiếm danh sách $\rightarrow$ Bấm xem chi tiết đề tài.
4. **Viết Script tự động (Automation):** Cung cấp các công cụ `seed_data.py` (tạo dữ liệu mẫu) và `backfill_normalized.py` (cập nhật hồi tố dữ liệu cũ) giúp việc bảo trì vô cùng thuận tiện.

---

## 4. Định hướng Phát triển Tương lai (Future Work)
Nếu tiếp tục mở rộng, hệ thống có thể phát triển thêm:
1. **Tích hợp ChromaDB & AI Semantic Search:** Thay vì tìm kiếm theo từ khóa (Keyword-based), tích hợp mô hình AI nhúng (Embedding) để tìm kiếm theo "Ngữ nghĩa".
2. **Dashboard Thống kê:** Xây dựng trang Admin Dashboard thống kê số lượng đề tài theo năm, theo khoa trực quan bằng biểu đồ (Chart.js / Recharts).
3. **Rate Limiting & Caching (Redis):** Áp dụng Redis để cache các kết quả tìm kiếm phổ biến, tăng tốc độ phản hồi và bảo vệ API khỏi tấn công spam.

---
**Kết luận:** 
Dự án "Web Tra cứu NCKH" hiện tại là một hệ thống toàn diện, ổn định, chạy mượt mà ở cả môi trường phát triển lẫn Production. Kiến trúc được thiết kế vững chắc, thuật toán tìm kiếm tối ưu sâu vào Tiếng Việt, sẵn sàng đáp ứng nhu cầu thực tế của nhà trường.
