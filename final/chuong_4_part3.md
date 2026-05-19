4.6 Thiết kế API (API Specification)
Giao tiếp giữa Frontend (Client) và Backend (Server) được chuẩn hóa hoàn toàn thông qua RESTful API. Mọi yêu cầu trao đổi dữ liệu đều tuân thủ nguyên tắc phi trạng thái (Stateless), sử dụng định dạng JSON, và mã trạng thái (HTTP Status Codes) chuẩn mực.

Dưới đây là đặc tả chi tiết (tương đương chuẩn OpenAPI/Swagger) cho 3 API cốt lõi nhất của hệ thống:

**4.6.1 API Đăng nhập (Authentication)**
- **Method & Endpoint:** `POST /api/v1/auth/login`
- **Mô tả:** Xác thực thông tin người dùng và trả về cặp token (Access Token & Refresh Token).
- **Headers:** `Content-Type: application/json`
- **Request Body (JSON):**
```json
{
  "email": "giangvien@vnu.edu.vn",
  "password": "Password123!"
}
```
- **Response - Thành công (200 OK):**
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5...",
    "token_type": "Bearer",
    "expires_in": 900
  }
}
```
*Lưu ý:* `refresh_token` không được trả về trong Body mà được gài vào Header `Set-Cookie` với cờ `HttpOnly` và `Secure` để chống tấn công đánh cắp token bằng Javascript (XSS).
- **Response - Lỗi (401 Unauthorized):**
```json
{
  "error_code": "AUTH_001",
  "message": "Email hoặc mật khẩu không chính xác."
}
```

**4.6.2 API Tìm kiếm Đề tài (Advanced Search)**
- **Method & Endpoint:** `GET /api/v1/search`
- **Mô tả:** Tìm kiếm toàn văn các đề tài đã được duyệt. Có hỗ trợ phân trang và lọc theo năm/lĩnh vực.
- **Headers:** Trống (API Public).
- **Query Parameters:**
  - `q` (string, required): Từ khóa tìm kiếm.
  - `page` (int, optional): Trang hiện tại (Mặc định = 1).
  - `limit` (int, optional): Số kết quả/trang (Mặc định = 20, Tối đa = 50).
  - `category_id` (int, optional): Lọc theo lĩnh vực.
- **Response - Thành công (200 OK):**
```json
{
  "status": "success",
  "meta": {
    "total_results": 145,
    "current_page": 1,
    "total_pages": 8
  },
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Ứng dụng AI trong nhận diện hình ảnh",
      "author_names": "Nguyễn Văn A",
      "abstract": "Nghiên cứu này đề xuất mô hình AI...",
      "score": 0.89
    }
    // ... 19 kết quả khác
  ]
}
```

**4.6.3 API Nộp đề tài (Submit Project)**
- **Method & Endpoint:** `POST /api/v1/projects`
- **Mô tả:** API dành cho tác giả nộp siêu dữ liệu và file PDF lên hệ thống.
- **Headers:** 
  - `Authorization: Bearer <Access_Token>` (Bắt buộc)
  - `Content-Type: multipart/form-data`
- **Request Body (Form-Data):**
  - `title` (text): Tên đề tài.
  - `category_id` (int): ID lĩnh vực.
  - `abstract` (text): Tóm tắt.
  - `file` (file): File đính kèm định dạng .pdf (Max 50MB).
- **Response - Thành công (201 Created):**
```json
{
  "status": "success",
  "message": "Nộp đề tài thành công. Vui lòng chờ phê duyệt.",
  "data": {
    "project_id": "987fcdeb-51a2-43d7-9012-345678901234",
    "status": "PENDING"
  }
}
```

---

4.7 Thiết kế bảo mật (Security Architecture)
Để đạt tiêu chuẩn "Enterprise", hệ thống không chỉ cần chạy đúng mà phải an toàn trước các rủi ro mạng (OWASP Top 10).

1. Chống tấn công XSS và CSRF:
- Cross-Site Scripting (XSS): Frontend ReactJS mặc định trốn (escape) mọi ký tự HTML do người dùng nhập vào. Quan trọng hơn, Refresh Token (chìa khóa để lấy lại phiên đăng nhập) tuyệt đối không được lưu trong `localStorage`. Nó được Backend gài thẳng vào cookie của trình duyệt với cờ `HttpOnly` (Javascript không thể đọc được) và `SameSite=Strict` (chống CSRF).

2. CORS (Cross-Origin Resource Sharing):
Hệ thống Backend FastAPI được cấu hình chỉ chấp nhận các Request đến từ đúng tên miền của Frontend (Ví dụ: `https://repository.vnu.edu.vn`). Mọi Request lạ (như từ `localhost` của hacker) gửi đến đều bị chặn ở ngay tầng mạng bằng lỗi CORS.

3. Thuật toán Rate Limiting (Giới hạn tỷ lệ):
Bảo vệ Server khỏi các cuộc tấn công DDoS Layer 7.
- Thuật toán: Token Bucket (Thùng thẻ).
- Triển khai: Tại tầng Middleware của FastAPI, hệ thống sẽ bắt IP của người dùng và băm (Hash) với chuỗi User-Agent. Mã băm này tạo thành một khóa (Key) trong Redis. Mỗi lần gọi API, Redis sẽ đếm lùi số lượng "thẻ". Nếu hết thẻ (Vượt quá 100 req/min), Server không xử lý logic mà ném thẳng lỗi `HTTP 429 Too Many Requests`.

---

4.8 Thiết kế triển khai (Deployment & DevOps)
Môi trường triển khai áp dụng triệt để Containerization (Ảo hóa cấp độ HĐH) thông qua Docker. Việc này giúp đóng gói toàn bộ Code, thư viện Python, biến môi trường vào trong một hộp (Container) duy nhất, đảm bảo tính nhất quán giữa môi trường Dev và Production.

Tệp `docker-compose.yml` định nghĩa toàn bộ cụm máy chủ ảo. Dưới đây là trích xuất cấu trúc triển khai:

```yaml
version: '3.8'

services:
  # 1. Database Service (Lưu trữ lõi)
  postgres_db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pg_data:/var/lib/postgresql/data
    networks:
      - vnu_net

  # 2. Caching Service (Bộ nhớ đệm tốc độ cao)
  redis_cache:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    networks:
      - vnu_net

  # 3. Backend Service (FastAPI lõi)
  api_backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres_db
      - redis_cache
    environment:
      - DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@postgres_db:5432/vnu_repo
      - REDIS_URL=redis://redis_cache:6379/0
    networks:
      - vnu_net

  # 4. Observability (Giám sát hệ thống)
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - vnu_net

networks:
  vnu_net:
    driver: bridge

volumes:
  pg_data:
```

Sự phân tách mạng (Network Isolation): Theo file cấu hình trên, toàn bộ các dịch vụ như `postgres_db` và `redis_cache` đều không mở cổng (`ports`) ra ngoài Internet. Chúng chỉ giao tiếp nội bộ trong mạng ảo `vnu_net`. Duy nhất dịch vụ `api_backend` (qua Nginx) được phép mở cổng 8000 ra thế giới bên ngoài. Đây là nguyên tắc thiết kế tường lửa (Firewall) quan trọng nhất để bảo vệ Database khỏi tin tặc.
