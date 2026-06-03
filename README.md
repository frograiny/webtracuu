# VNU Research API - Enterprise Production

Hệ thống tra cứu Đề tài Nghiên cứu Khoa học chuẩn Enterprise, được thiết kế với kiến trúc chịu tải cao (High-performance), bảo mật mạnh mẽ và khả năng giám sát toàn diện (Observability).

## 🌟 Điểm Nhấn Kiến Trúc (Architecture Highlights)

### 1. High-Performance Search Engine
- **PostgreSQL Full-Text Search (FTS):** Sử dụng `TSVECTOR` và Index `GIN` thay vì `LIKE`, cho phép query cực nhanh trên hàng triệu bản ghi.
- **Fuzzy Matching:** Tích hợp `pg_trgm` (Trigram) để sửa lỗi chính tả người dùng.
- **Smart Ranking:** Áp dụng `ts_rank` kết hợp Field Boosting (Tiêu đề > Tác giả) và Từ điển đồng nghĩa (Synonyms) bằng Python.

### 2. Cache Invalidation Strategy
- **Redis Centralized Cache:** Mọi kết quả query phức tạp đều được lưu trên Redis.
- **Key Normalization:** Từ khóa tìm kiếm được lọc bỏ khoảng trắng thừa và viết thường để gom chung Cache Key, tăng tối đa Hit-rate.
- **Auto-Invalidation:** Background Tasks của FastAPI sẽ tự động xóa bộ đệm Redis ngay lập tức khi Admin thực hiện Thêm/Sửa/Xóa dữ liệu. Đảm bảo 100% Data Consistency.

### 3. Enterprise Auth Lifecycle & Security
- **Dual Token JWT:** Cung cấp cả Access Token (15 phút) và Refresh Token (7 ngày).
- **Redis Blacklist:** Khi người dùng Logout, Token ID (JTI) lập tức bị chặn trong Redis.
- **Smart Rate Limiting:** Hạn chế spam thông minh qua Token (cho Auth Users) và IP + User-Agent (cho Guest, chống lỗi chặn nhầm mạng NAT).

### 4. Observability & SRE Basics
- **Prometheus & Grafana:** Cung cấp endpoint `/metrics` đo đạc RPS, Latency và Error Rate.
- **Business Metrics:** Tích hợp bộ đếm giám sát tỉ lệ "Tìm kiếm không ra kết quả" (Search Success Rate).
- **Healthcheck:** Cấu hình Docker tự động ping endpoint `/health` để tự phục hồi khi có sự cố.

## 🛠️ Stack Công Nghệ
- **Backend:** FastAPI, SQLAlchemy, Alembic, Pydantic, Promtheus-Client
- **Database:** PostgreSQL (pg_trgm, unaccent extensions)
- **Cache & State:** Redis
- **Infrastructure:** Docker & Docker Compose
- **Monitoring:** Prometheus, Grafana

## 🚀 Hướng Dẫn Chạy (Quick Start)

### 1. Khởi động toàn bộ cụm dịch vụ (Stack)
Dự án được đóng gói trọn vẹn trong Docker. Chỉ với 1 lệnh, bạn sẽ dựng lên cả Backend, Frontend, DB, Redis và hệ thống Monitor:
```bash
docker-compose up -d --build
```

### 2. Chạy Migration (Rất quan trọng)
Vì hệ thống sử dụng các Extension đặc biệt của PostgreSQL, bạn BẮT BUỘC phải chạy Migration ngay sau khi DB lên:
```bash
docker exec -it vnu_research_backend alembic upgrade head
```

### 3. Chạy Seed Data (Dữ liệu mẫu)
```bash
docker exec -it vnu_research_backend python seed_data.py
```

### 4. Các đường dẫn truy cập
- **Web Frontend:** `http://localhost:5173`
- **Swagger API Docs:** `http://localhost:8000/docs`
- **Grafana (Monitoring):** `http://localhost:3000` (admin/admin)
- **Prometheus (Metrics):** `http://localhost:9090`

## 🧪 Công Cụ Load Test (Benchmark)
Dự án đi kèm một script `locustfile.py` để bạn tự mình ép tải hệ thống và quan sát qua Grafana.
1. Cài đặt Locust: `pip install locust`
2. Chạy: `locust`
3. Truy cập UI: `http://localhost:8089`
