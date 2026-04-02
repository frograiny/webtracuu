# Hướng Dẫn Chạy Dự Án NCKH Local

Để khởi động toàn bộ hệ thống Web Tra Cứu, vui lòng thao tác theo các bước chuẩn dưới đây:

## 1. Mở Cửa Sổ Backend (Server API)
Mở một cửa sổ Terminal/Command Prompt mới và gõ lần lượt:
```bash
# 1. Di chuyển vào thư mục backend
cd d:\nghich\webtruong\backend

# 2. Kích hoạt môi trường ảo (Windows PowerShell)
..\venv\Scripts\activate

# 3. Chạy Server FastAPI
uvicorn app.main:app --port 8000 --reload
```
👉 Sau khi chạy thành công, mở trình duyệt để xem tệp API Docs tại: **http://127.0.0.1:8000/docs**

---

## 2. Mở Cửa Sổ Frontend (Giao diện Web React)
Mở thêm một cửa sổ Terminal/Command Prompt thứ hai và gõ:
```bash
# 1. Di chuyển vào thư mục frontend bên trong
cd d:\nghich\webtruong\frontend\vnu-frontend

# 2. Khởi động Vite Server
npm run dev
```
👉 Sau khi chạy thành công, mở trình duyệt để xem Web tại: **http://localhost:5173**

---
*(Lưu ý: Không được tắt 2 cửa sổ màu đen này trong suốt quá trình sử dụng web)*
