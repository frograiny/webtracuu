# Báo Cáo Hiện Trạng Dự Án - Web Tra Cứu NCKH
*Cập nhật lần cuối: 02/04/2026*

## 1. Cấu Trúc Tổng Quan (Kiến Trúc Thay Đổi Mới)
Dự án đã được chia nhỏ cấu trúc để dễ quản lý, theo tiêu chuẩn mô hình hiện đại.
- **Backend (`/backend`)**: FastAPI + SQLAlchemy (Database PostgreSQL)
- **Frontend (`/frontend/vnu-frontend`)**: React + Vite + TypeScript (có cấu trúc Angular-style thư mục)
- **Database (`Docker`)**: PostgreSQL 15, quản lý qua `docker-compose.yml`
- **Tài Liệu Cục Bộ (`/huongdan`)**: Chứa toàn bộ báo cáo phân tích, changelog, script lỗi.

## 2. Các Tính Năng Đã Hoàn Thiện Tới Hiện Tại

### A. Hệ Thống Tìm Kiếm Thông Minh (AI Search đã tích hợp sâu)
Sự nâng cấp lớn nhất nằm ở thuật toán nhận diện chữ Tiếng Việt:
- **Trường hợp gõ Tiếng Việt CÓ DẤU (Full FTS):** Sử dụng `to_tsvector` có sẵn trong db để băm chữ và chấm điểm kết quả `ts_rank` tự lên trên, KHÔNG BỊ ERROR DEPENDENCY HAY SERVER YẾU.
- **Trường hợp gõ Tiếng Việt KHÔNG DẤU (Fallback Unaccent):** Vừa rồi tôi đã fix 1 bug khét tiếng về việc mất điểm search. Hiện hệ thống kết hợp `unicodedata` ở backend và `func.translate()` ở SQL giúp "vat lieu" hoàn toàn quét được "vật liệu" 100% không để sót. Hoàn toàn sạch và không cần extension.

### B. Môi trường Trình Diễn Bảo Mật (Demo WAF)
Dự án có chuẩn bị 1 cổng (endpoint) `/search-vulnerable` (lưu trong file `search.py`). Cổng này được CỐ TÌNH CẤU TRÚC SQL INJECTION thô. 
Mục đích:
- Để chứng minh trước bảo vệ (giữa kỳ/cuối kỳ) sự chênh lệch của AI WAF (khi AI WAF bật và tắt). 
- Khi tắt, nó phơi bày toàn bộ DB. Rất trực quan khi báo cáo bảo vệ.

### C. Quản Lý Khởi Động & Khôi Phục Database (Docker)
- Chỉ giữ lại Docker file cho Postgres (tối giản rủi ro conflict trên hệ điều hành), ứng dụng chạy Localhost qua `venv`.
- Cấu hình file `start_project.bat`: 1 Click lên toàn bộ hệ thống (`FastAPI` backend + `npm run dev` frontend).
- Đã test Connection `✅ Kết nối tới Docker Postgres THÀNH CÔNG!` → PostgreSQL đang kết nối hoàn toàn mượt mà tới DB `vnu_research_db`.

## 3. Tình Trạng Hiện Tại \& To-Do List Hướng Tới

**Trạng Thái:** 🟢 **ỔN ĐỊNH VÀ SN SÀNG BÁO CÁO.** Hệ thống Frontend liên kết Backend đã đồng bộ và thông suốt.

**Gợi ý các việc nếu muốn tiếp tục đi sâu:**
1. Mở lại tính năng *ChromaDB AI Semantic search* (nếu máy có RAM >= 16GB) nếu thầy yêu cầu mức phức tạp AI cao hơn.
2. Thiết kế thêm hệ thống Account + Phân Quyền Giảng Viên / Sinh Viên (nếu hệ thống tra cứu muốn thu phí / riêng tư).
3. Đẩy lên server ảo Docker trọn bộ ứng dụng.
