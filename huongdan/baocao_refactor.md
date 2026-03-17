# BÁO CÁO CẬP NHẬT KIẾN TRÚC BACKEND (REFACTORING)

Kính gửi sếp, 

Hệ thống Backend (FastAPI - PostgreSQL) đã được **Refactor toàn diện** để đạt chuẩn công nghiệp (Production-ready). Dưới đây là các thay đổi và cải tiến chính:

## 1. Chuẩn Hóa Kiến Trúc Thư Mục (Modular Monolith)
Từ một file `app.py` khổng lồ chứa mọi logic, hệ thống đã được tách thành các module chuyên trách độc lập:
*   `app/main.py`: Entrypoint của ứng dụng, chỉ chứa Middleware và config router.
*   `app/api/v1/`: Nơi chứa URL endpoints (`search.py`, `filters.py`).
*   `app/models/`: Định nghĩa ORM Database (`project.py`).
*   `app/core/`: Quản lý cấu hình tĩnh (`config.py`).
*   `app/db/`: Quản lý Connection pool của PostgreSQL (`session.py`).
*   `scripts/`: Tách riêng các file dùng một lần như `seed_data.py`, `check_db.py`.

## 2. Quản Lý Configuration Bằng Môi Trường (`.env`)
*   Toàn bộ cấu hình nhạy cảm (như `DATABASE_URL`) đã được chuyển ra file `.env`.
*   Sử dụng thư viện `pydantic-settings` (chuẩn Pydantic v2) để validate các biến môi trường này khi khởi động. Không lo lỗi quên cấu hình URL Database trên server thật.

## 3. Chuyển Đổi Sang Alembic (Database Migrations)
*   **Loại bỏ `recreate_db.py`**: Web không còn rủi ro Drop toàn bộ dữ liệu khi khởi động nữa.
*   **Thêm `alembic/`**: Từ nay, mọi thay đổi cấu trúc Database (Thêm cột, Xóa bảng) sẽ được Alembic tự động generate thành file Migration có Timestamp, cho phép Upgrade/Downgrade an toàn tuyệt đối.

## 4. Tối Ưu Hóa Multi-stage Dockerfile
*   **Build Stage**: Sử dụng Image nặng để chứa `gcc` phục vụ quá trình biên dịch thư viện C-level như psycopg2 thành dạng `wheel`,
*   **Runtime Stage**: Base Image Python siêu nhẹ (Slim) sẽ chỉ việc copy file compiled từ Build stage sang mà không cần cài thêm gcc.
*   Kết quả: Image size giảm từ hàng GB xuống chỉ còn lượng cần thiết, build web tăng tốc cực nhanh.

## 5. Các Mảng Tạm Thời Loại Bỏ
*   Module AI Semantic Search (ChromaDB + SentenceTransformers) đã được comment/gỡ bỏ ra khỏi frontend, backend và requirements để tiết kiệm hàng GB RAM, nhường tài nguyên cho quá trình kiểm thử PostgreSQL Text Search trên Web.

Mọi chức năng API cũ vẫn hoạt động trơn tru sau khi chuyển File. Sếp có thể an tâm báo cáo hoặc deploy thẳng lên server!
