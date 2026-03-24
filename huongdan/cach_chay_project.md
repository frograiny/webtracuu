# Hướng Dẫn Chạy Dự Án NCKH

Dự án bao gồm 2 phần là Backend (Python/FastAPI) và Frontend (React/Vite). Để chạy toàn bộ dự án, bạn cần mở 2 cửa sổ Terminal (hoặc Command Prompt/PowerShell) riêng biệt.

## 1. Mở Cơ Sở Dữ Liệu (PostgreSQL)
Đảm bảo rằng service PostgreSQL trên máy tính đã được bật và Server đang chạy ở port `5432` với tài khoản/mật khẩu được cấu hình trong file `backend/.env`.

---

## 2. Chạy Backend (FastAPI)

1. Mở Terminal mới (Terminal 1), trỏ vào thư mục chứa code:
   ```bash
   cd d:\nghich\webtruong\backend
   ```
2. Kích hoạt môi trường ảo (Virtual Environment):
   ```bash
   # Nếu dùng Windows PowerShell:
   ..\venv\Scripts\activate
   ```
3. Khởi động Server:
   ```bash
   uvicorn app.main:app --port 8000 --reload
   ```
4. Kiểm tra Backend:
   Mở trình duyệt và truy cập: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Nếu hiện giao diện Swagger UI là thành công.

---

## 3. Chạy Frontend (React/Vite)

1. Mở Terminal mới (Terminal 2), trỏ vào thư mục frontend:
   ```bash
   cd d:\nghich\webtruong\frontend\vnu-frontend
   ```
2. Khởi động Web Server:
   ```bash
   npm run dev
   ```
3. Kiểm tra Frontend:
   Mở trình duyệt và truy cập: [http://localhost:5173](http://localhost:5173). Giao diện web tra cứu sẽ hiện ra.

---
