# 🎓 VNU Research Portal (Web Trác Cứu NCKH)

Dự án hệ thống trác cứu đề tài Nghiên cứu Khoa học (NCKH) của Đại học Quốc gia Hà Nội. Được thiết kế tối ưu cho việc tìm kiếm chính xác, bảo mật và khả năng mở rộng.

---

## 🛠️ Problem & Solution

### Vấn đề (Problem)
1. **Tìm kiếm tiếng Việt không hiệu quả:** Tìm kiếm SQL `LIKE` thông thường gặp khó khăn với dấu tiếng Việt và tìm kiếm theo cụm từ/từ khóa rời rạc.
2. **Quá tải CSDL:** Việc tính toán điểm độ liên quan (ranking) trực tiếp trên DB mỗi khi có request làm tiêu tốn tài nguyên.
3. **Bảo mật & Spam:** Các endpoint nhạy cảm dễ bị tấn công Brute-force hoặc bị cào dữ liệu (scraping) hàng loạt.

### Giải pháp (Solution)
1. **Token-level Scoring Pipeline:** Chuyển đổi query thành các token đã chuẩn hóa và tính điểm dựa trên vị trí xuất hiện (Title/Author).
2. **Multi-layer Caching:** Giảm độ trễ (latency) cho các truy vấn phổ biến bằng InMemory Cache.
3. **RBAC & Rate Limiting:** Phân quyền chặt chẽ dựa trên JWT và giới hạn tần suất gọi API (Throttling) ở mức IP.

---

## 🔍 Chi tiết thuật toán Tìm kiếm (Search Pipeline)

Hệ thống không sử dụng Vector Search (Embedding) để tránh phụ thuộc vào hạ tầng AI phức tạp, thay vào đó tập trung vào **Keyword-based Scoring** tối ưu cho dữ liệu văn bản ngắn (Tên đề tài).

### Luồng xử lý dữ liệu:
1. **Normalization:** Input `Query` → Lowercase → Loại bỏ dấu tiếng Việt → Loại bỏ ký tự đặc biệt.
2. **Tokenization:** Tách chuỗi thành danh sách các từ khóa đơn lẻ (keywords).
3. **Match Logic:** Sử dụng logic `AND` trên các cột đã chuẩn hóa (`title_normalized`, `author_normalized`). Tất cả các từ khóa trong query đều phải xuất hiện ít nhất một lần.
4. **Scoring Weights:**
   - **Title Match:** +3 điểm cho mỗi keyword xuất hiện trong tiêu đề.
   - **Author Match:** +1 điểm cho mỗi keyword xuất hiện trong tên tác giả.
   - **Exact Phrase Bonus:** +5 điểm nếu toàn bộ query xuất hiện chính xác như một cụm từ trong tiêu đề.
5. **Ranking & Sort:** Kết quả được sắp xếp theo: `Total Score (DESC)` → `Year (DESC)`.

---

## 🏗️ Kiến trúc hệ thống (Architecture)

### Sơ đồ luồng dữ liệu (Data Flow):
```text
[User Request] 
      ↓
[SlowAPI (Rate Limit)] → [Thành công] → [FastAPI Cache] → [Hit] → [Trả về kết quả]
      ↓                                    ↓
[Check Token (JWT)]                      [Miss]
      ↓                                    ↓
[API Layer (FastAPI)] ←─────────── [Service/Logic Layer]
                                           ↓
                                   [SQLAlchemy ORM]
                                           ↓
                                    [PostgreSQL DB]
```

### Phân tầng logic:
- **API Layer:** Định nghĩa các routes, schemas (Pydantic) và Dependency Injection.
- **Core Layer:** Chứa cấu hình bảo mật, RBAC (`get_current_admin`), và cấu hình Rate Limit.
- **Database Layer:** Quản lý SQLAlchemy Models và Migrations (Alembic).
- **Testing Layer:** Bộ test tích hợp sử dụng SQLite In-memory để đảm bảo CI/CD.

---

## 🔐 Bảo mật & Phân quyền (Security)

### Role-Based Access Control (RBAC):
| Role | Quyền hạn (Permissions) | Endpoints Bảo vệ |
| :--- | :--- | :--- |
| **Admin** | Toàn quyền CRUD | `/users`, `POST/PUT/DELETE /projects` |
| **Viewer** | Xem & Tìm kiếm | `GET /me`, `GET /search` |
| **Public** | Tìm kiếm (Bị giới hạn) | `GET /search` (Rate Limited) |

### Cơ chế bảo vệ:
- **JWT Scope:** Token chứa `user_id` và `role`. Hiệu lực trong 60 phút.
- **Rate Limit:** Áp dụng `Fixed Window` dựa trên IP của Client.
- **Env Validation:** Chặn khởi động ở chế độ `production` nếu dùng `SECRET_KEY` mặc định.

---

## ⚡ Cơ chế Caching

- **Công nghệ:** `fastapi-cache2` với `InMemoryBackend`.
- **Phạm vi:** Chỉ áp dụng cho endpoint `GET /search`.
- **Lợi ích:**
  - **Giảm Latency:** Các truy vấn trùng lặp không cần tính toán lại điểm Ranking.
  - **Giảm tải DB:** Tiết kiệm CPU cho PostgreSQL khi có lượng lớn người dùng cùng tìm một từ khóa (vd: "AI", "Blockchain").
- **TTL:** 300 giây (5 phút). Sau thời gian này, cache sẽ bị hủy để đảm bảo tính cập nhật của dữ liệu.

---

## 📐 Trade-offs & Design Decisions

1. **SQLite vs PostgreSQL cho Testing:** Sử dụng SQLite in-memory cho Unit Test giúp tốc độ chạy test cực nhanh (< 2 giây), nhưng cần lưu ý sự khác biệt nhỏ về syntax SQL giữa 2 hệ quản trị.
2. **In-memory Cache vs Redis:** Chọn In-memory để đơn giản hóa việc triển khai (không cần cài thêm server Redis). Tuy nhiên, cache sẽ bị mất khi khởi động lại backend và không chia sẻ được giữa các instance (nếu scale ngang).
3. **Keyword Scoring vs Vector Search:** Keyword scoring mang lại kết quả dự đoán được (predictable) và dễ debug hơn cho người dùng cuối khi tìm tên đề tài cụ thể, đồng thời giảm chi phí hạ tầng.

---

## 🚀 Hướng dẫn khởi chạy

*Vui lòng tham khảo file `start_project.bat` để khởi động nhanh hoặc đọc kỹ mục [Manual Setup](huongdan/cach_chay_project.md).*

---

**Last Updated:** 05/05/2026  
**Version:** 1.2.0 (Standardized Architecture)
