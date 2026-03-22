# Cấu Trúc Đề Ra và Các Lệnh Thao Tác

## 1. Cấu trúc tổng thể lý tưởng (Kiến trúc đề ra)
Dự án được thiết kế theo hướng modular hóa nhằm đảm bảo tính dễ bảo trì và khả năng mở rộng (Production-ready). Cấu trúc file và thư mục chuẩn bao gồm:

```text
webtruong/
├── backend/                # Chứa toàn bộ logic server (FastAPI)
│   ├── app/                # Package chính
│   │   ├── api/v1/         # Nơi chứa các Route/Endpoint API (search, filters,...)
│   │   ├── core/           # Cấu hình tĩnh và cấu hình môi trường (.env, config.py)
│   │   ├── db/             # Kết nối Database và Session (session.py)
│   │   ├── models/         # Định nghĩa các model ORM (SQLAlchemy)
│   │   └── main.py         # Entrypoint của ứng dụng, middleware và config router
│   ├── alembic/            # Thư mục quản lý các file migration của Database
│   ├── scripts/            # Các script chạy tiện ích (seed_data, check_db,...)
│   ├── requirements.txt    # Danh sách thư viện Python
│   └── Dockerfile          # Multi-stage build cho backend
├── frontend/               # Chứa toàn bộ logic giao diện
│   └── vnu-frontend/       # Pj React/Vite hiện tại
│       ├── src/            # Mã nguồn Components, Pages, Assets,...
│       ├── package.json    # Cấu hình dependency của Node
│       └── vite.config.ts  # Cấu hình module React/Vite
├── huongdan/               # Chứa các tài liệu hướng dẫn, báo cáo (như file này)
├── data/                   # Chứa dữ liệu Database cục bộ (ví dụ: DB Chroma) - Cần được ignore
├── docker-compose.yml      # Cấu hình chạy toàn bộ stack cục bộ qua Docker
└── README.md
```

## 2. Các Lệnh Thao Tác Thường Dùng (Commands)

### Nhóm lệnh Backend (Python/FastAPI)
- **Khởi động môi trường ảo và chạy server (Dev mode):**
  ```bash
  cd backend
  ..\venv\Scripts\activate  # (Môi trường Windows)
  uvicorn app.main:app --reload --port 8000
  ```
- **Xử lý Database Migration (Alembic):**
  ```bash
  alembic revision --autogenerate -m "Mô tả sự thay đổi database"
  alembic upgrade head
  ```
- **Seed dữ liệu mẫu vào DB:**
  ```bash
  python scripts/seed_data.py
  ```

### Nhóm lệnh Frontend (React/Vite)
- **Cài đặt thư viện và Khởi chạy server giao diện:**
  ```bash
  cd frontend/vnu-frontend
  npm install
  npm run dev
  ```

### Nhóm lệnh Docker (Chạy toàn bộ hệ thống)
- **Build và khởi chạy background:**
  ```bash
  docker-compose up --build -d
  ```
