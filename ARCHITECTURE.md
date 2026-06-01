# System Architecture: VNU Research API

Tài liệu này quy định các nguyên tắc thiết kế cốt lõi (Design), quy tắc bắt buộc (Rules) và các giới hạn hệ thống (Constraints) để đảm bảo toàn bộ team phát triển đồng nhất về tư duy khi làm việc trên dự án này.

---

## 1. System Design (Thiết Kế Hệ Thống)

Hệ thống tuân theo mô hình **Service-Oriented Architecture (SOA)** tinh gọn, tập trung vào hiệu năng (Performance) và khả năng quan sát (Observability).

### 1.1. Component Architecture
- **API Layer (FastAPI):** Đóng vai trò là Gateway duy nhất xử lý HTTP Requests, Auth, Rate Limiting và Routing. Chạy qua ASGI Uvicorn.
- **Data Layer (PostgreSQL):** Không chỉ lưu trữ Relational Data, mà còn đảm nhận vai trò **Search Engine** (qua extension `pg_trgm` và kiểu dữ liệu `TSVECTOR`).
- **State & Cache Layer (Redis):** Xử lý 2 luồng dữ liệu phân tán:
  1. *Distributed Cache:* Lưu kết quả tìm kiếm để giảm tải DB.
  2. *Security State:* Lưu JWT Blacklist khi người dùng đăng xuất.
- **Observability Layer (Prometheus + Grafana):** Hoạt động độc lập bằng cơ chế `pull-based` (Scrape endpoint `/metrics`), không làm nghẽn luồng xử lý chính của API.

### 1.2. Key Workflows
- **Luồng Tìm Kiếm (Search Flow):** User Query → Normalize & Rewrite (Python) → Cache Check (Redis) → Cache Miss → Postgres FTS (`@@`) + Trigram (`similarity()`) → Điểm số (Ranking) → Trả về → Ghi Metrics.
- **Luồng Xác Thực (Auth Flow):**
  - **Login:** Trả về Access Token (15m) + Refresh Token (7d).
  - **Refresh:** Validate Refresh Token → Không nằm trong Blacklist → Cấp Access Token mới.
  - **Logout:** Đẩy Token ID (JTI) vào Redis Blacklist với TTL bằng thời hạn còn lại.

---

## 2. Core Rules (Quy Tắc Phát Triển)

Để giữ cho hệ thống "Sạch" và "Nhanh", mọi kỹ sư phải tuân thủ các quy tắc sau:

### 2.1. Database & Search Rules
- **KHÔNG dùng `LIKE` hoặc `ILIKE` cho Search:** Bắt buộc phải sử dụng `search_vector` (FTS) hoặc `similarity()` (Trigram) khi tra cứu text.
- **Đồng bộ hóa dữ liệu (Consistency):** Không viết Background Job để Re-index dữ liệu. Việc tính toán `search_vector` phải luôn được khai báo ở mức Schema Migration bằng kiểu `GENERATED ALWAYS AS (...) STORED`.
- **Luôn đánh Index:** Các cột dùng để filter thường xuyên (VD: `year`, `target_audience`) phải có B-Tree Index. Cột `search_vector` bắt buộc dùng GIN Index.

### 2.2. Caching Rules
- **Nguyên tắc "No Stale Data":** Mọi API thực hiện `POST/PUT/DELETE` tác động đến bảng `ResearchProject` đều BẮT BUỘC phải gọi `FastAPICache.clear(namespace="projects")` thông qua `BackgroundTasks`.
- **Normalize Cache Keys:** Phải normalize param (strip khoảng trắng, lower case) thông qua `custom_key_builder` trước khi lookup cache để tránh rác Redis.

### 2.3. Security & Ops Rules
- **Mặc định Rate Limit:** Mọi public endpoint đều phải gắn decorator `@limiter.limit`. Tách biệt Key: Dùng JWT Sub cho người dùng có Auth, và kết hợp `IP + User-Agent` cho Guest.
- **Không bao giờ "nuốt" Metrics:** Mọi luồng API quan trọng đều phải cập nhật Prometheus Counter/Histogram. (VD: Cần biết bao nhiêu lượt search thất bại).

---

## 3. System Constraints (Giới Hạn Hệ Thống)

### 3.1. Development & Testing
- **SQLite Limitation:** Vì dự án phụ thuộc nặng nề vào các hàm đặc thù của Postgres (như `to_tsquery`, `setweight`), việc chạy Unit Test trực tiếp trên SQLite in-memory sẽ bị *Crash*. **Constraint:** Trong Unit Test, các luồng DB liên quan đến FTS phải được `Mock`, hoặc phải chạy E2E test trên môi trường Docker có Postgres.

### 3.2. Scaling
- **Vertical DB Scaling:** Hiện tại Search Engine và Primary DB nằm chung trên một node Postgres. Khi lượng Data và Request tăng đột biến, FTS (tốn CPU) có thể làm chậm luồng Ghi (Write). **Khuyến nghị tương lai:** Cần đẩy luồng FTS sang Elasticsearch nếu vượt ngưỡng 10,000 CCU.
- **Horizontal API Scaling:** FastAPI hoàn toàn Stateless (State đẩy về Redis). Việc Scale-out API node là không có giới hạn.

### 3.3. Infrastructure Complexity
- **Omitted Reverse Proxy:** Ở giai đoạn hiện tại, Nginx/Traefik được cố tình loại bỏ khỏi cấu trúc local để giảm độ phức tạp vận hành (Complexity). Khi đưa lên Cloud thực tế, hệ thống BẮT BUỘC phải đứng sau một API Gateway hoặc Load Balancer có HTTPS Termination.
