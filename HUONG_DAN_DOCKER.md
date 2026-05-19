# 🐳 HƯỚNG DẪN CHẠY WEB BẰNG DOCKER (CHUẨN CHUYÊN NGHIỆP)

Dành cho những ai muốn chạy dự án chuẩn chỉ theo kiến trúc Enterprise (có đủ Database, Redis Cache, API và Frontend) mà không muốn cài lẻ tẻ từng phần mềm như Python hay Node.js vào máy.

## BƯỚC 1: CHUẨN BỊ VŨ KHÍ
1. Tải và cài đặt phần mềm **Docker Desktop** tại: `https://www.docker.com/products/docker-desktop/`
2. Cài xong, **mở Docker Desktop lên** và để nó chạy ngầm (thấy biểu tượng con cá voi ở góc phải màn hình là OK).

---

## BƯỚC 2: KHỞI ĐỘNG HỆ THỐNG (BẰNG 1 DÒNG LỆNH)
1. Mở thư mục gốc của dự án (nơi chứa file `docker-compose.yml`).
2. Nhấn chuột phải vào vùng trống trong thư mục, chọn **Open in Terminal** (hoặc mở CMD/PowerShell và dùng lệnh `cd` trỏ tới thư mục này).
3. Gõ chính xác câu lệnh màu nhiệm này và ấn Enter:

```bash
docker-compose up -d --build
```

👉 **Chuyện gì đang xảy ra?** 
- Docker sẽ tự động "xây" lên 4 tòa nhà: PostgreSQL (CSDL), Redis (Cache), FastAPI (Backend), và React (Frontend).
- *(Lần đầu tiên chạy có thể mất 3-5 phút để nó tải nguyên liệu từ trên mạng về, từ lần thứ 2 trở đi mất 2 giây).*

---

## BƯỚC 3: TRUY CẬP VÀ TRẢI NGHIỆM
Khi Terminal chạy xong mà không báo lỗi đỏ lòm, bạn mở trình duyệt lên:
- 🌐 **Trang chủ Web (Dành cho người dùng):** `http://localhost:5173`
- ⚙️ **Hệ thống API Backend (Dành cho Dev):** `http://localhost:8000/docs`

---

## BƯỚC 4: CÁCH DỌN DẸP & TẮT HỆ THỐNG
Khi nghiệm thu xong, để tắt web và giải phóng RAM cho máy tính, bạn quay lại màn hình Terminal lúc nãy và gõ:

```bash
docker-compose down
```

Hệ thống sẽ tự động tắt và dọn dẹp sạch sẽ toàn bộ các "tòa nhà" mà nó vừa xây. Quá pro! 😎
