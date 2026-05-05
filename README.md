# 🎓 VNU Research Portal (Web Trác Cứu NCKH)

Dự án cổng thông tin và tìm kiếm đề tài Nghiên cứu Khoa học (NCKH) dành cho Đại học Quốc gia Hà Nội. Hệ thống được xây dựng với kiến trúc hiện đại, tối ưu hóa cho tốc độ tìm kiếm và bảo mật.

## ✨ Tính năng nổi bật

### 🔍 Tìm kiếm Hybrid (Hybrid Search)
- **Thuật toán Token-level Scoring:** Tính điểm độ liên quan dựa trên tiêu đề và tác giả.
- **Chuẩn hóa tiếng Việt:** Hỗ trợ tìm kiếm cả có dấu và không dấu một cách chính xác.
- **Hiệu suất cao:** Sử dụng các cột đã được normalized và index trong PostgreSQL.

### 🛡️ Bảo mật & Quản trị
- **JWT Authentication:** Hệ thống đăng nhập an toàn với Access Token.
- **Phân quyền (RBAC):** Phân chia rõ ràng vai trò `Admin` (quản lý đề tài, user) và `Viewer` (xem thông tin).
- **Rate Limiting:** Chống tấn công Brute Force và Spam API (Giới hạn 5 req/min cho login, 30 req/min cho search).

### ⚡ Tối ưu hiệu năng
- **Caching:** Tích hợp `fastapi-cache2` (InMemoryBackend) giúp phản hồi kết quả tìm kiếm ngay lập tức cho các truy vấn phổ biến.
- **Pagination:** Toàn bộ các API danh sách (đề tài, người dùng) đều được phân trang để đảm bảo tốc độ khi dữ liệu lớn.

### 📝 Giám sát & Kiểm thử
- **Structured Logging:** Sử dụng `loguru` để quản lý log chuyên nghiệp, tự động lưu và xoay vòng file log theo ngày.
- **Automated Testing:** Bộ test hoàn chỉnh với `pytest`, giả lập Database trong bộ nhớ để đảm bảo code luôn chạy đúng.

---

## 🛠️ Công nghệ sử dụng

- **Backend:** FastAPI (Python), SQLAlchemy ORM, PostgreSQL.
- **Frontend:** React, TypeScript, Vite, TailwindCSS.
- **Infrastructure:** Docker, Docker Compose, SlowAPI, FastAPICache.

---

## 🚀 Hướng dẫn khởi chạy

### Cách 1: Chạy nhanh bằng file Batch (Windows)
Chỉ cần chạy file sau ở thư mục gốc:
```bash
start_project.bat
```
File này sẽ tự động khởi động cả Backend (cổng 8000) và Frontend (cổng 5173).

### Cách 2: Chạy thủ công

**1. Backend:**
```bash
cd backend
python -m venv venv
..\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**2. Frontend:**
```bash
cd frontend/vnu-frontend
npm install
npm run dev
```

---

## 🧪 Chạy Kiểm thử (Tests)

Hệ thống sử dụng `pytest` để kiểm tra logic backend:
```bash
cd backend
..\venv\Scripts\activate
python -m pytest tests/ -v
```

---

## 📁 Cấu trúc thư mục chính

```text
.
├── backend/
│   ├── app/                # Mã nguồn chính của API
│   │   ├── api/            # Các endpoint (v1)
│   │   ├── core/           # Cấu hình, bảo mật, rate limit
│   │   ├── models/         # Database models (SQLAlchemy)
│   │   └── schemas/        # Pydantic models (Validation)
│   ├── tests/              # Bộ Unit Test (Pytest)
│   ├── requirements.txt    # Thư viện Python
│   └── alembic/            # Quản lý migration database
├── frontend/
│   └── vnu-frontend/       # Mã nguồn React Application
├── logs/                   # Thư mục chứa log của hệ thống
├── start_project.bat       # Script khởi động nhanh
└── docker-compose.yml      # Cấu hình Docker toàn hệ thống
```

---

**Last Updated:** 05/05/2026  
**Status:** 🚀 Production-Ready Architecture
