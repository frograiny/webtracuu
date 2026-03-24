# Báo Cáo: Hành Trình Tiến Hóa Thuật Toán Tìm Kiếm Của Hệ Thống

Dưới đây là phần giải trình về quá trình nâng cấp và thay đổi thuật toán cốt lõi của thanh tìm kiếm, từ phiên bản sơ khai đến quyết định chốt hạ hiện tại.

## 1. Phiên Bản Cũ: Trigram Similarity (`func.similarity`)
**Hệ thống dùng gì:** PostgreSQL cung cấp một Extention mở rộng tên là `pg_trgm`, có khả năng băm nhỏ từ khóa thành các cụm 3 ký tự (ví dụ: `chế` -> `c`, `ch`, `hế`) để đo lường "độ giống nhau" nhằm tìm ra chữ gõ sai chính tả.
**Giải thích vì sao sai:** Khi đem code qua môi trường máy khác hoặc Server mới, Extension này không được cài đặt mặc định trong PostgreSQL, dẫn đến hệ thống bị sập (lỗi 500) do gọi trúng hàm `func.similarity` vốn không tồn tại sẵn.

## 2. Giải pháp Cứu Chữa: Substring Matching (`ILIKE`)
**Hệ thống dùng gì:** Sau khi bỏ `pg_trgm`, thuật toán được lùi về hàm mặc định nội tại `ILIKE` kết hợp với kỹ thuật giấu từ khóa Wildcard (`%keyword%`). 
**Giải thích vì sao đổi:** Giải pháp này tuy không sập hệ thống (chạy được ở mọi Database), nhưng nó quá "máy móc", bắt buộc người dùng phải nhập chính xác tuyệt đối chữ cái liền nhau (ví dụ gõ "chế tạo vật liệu" thì mới ra chứ gõ "vật liệu chế tạo" thì chịu). Do đó ta lại phải thay đổi.

## 3. CHỐT HẠ: PostgreSQL Full-Text Search (FTS)
**Hệ thống dùng gì:** Hiện tại hệ thống chính thức triển khai bộ công cụ tìm kiếm văn bản toàn văn (**Full-Text Search**) cài sẵn (built-in) của PostgreSQL thông qua cặp lện `to_tsvector` (biến văn bản thành vector từ vựng) và `plainto_tsquery` (chuyển câu truy vấn thành các từ khoá rời rạc).
**Giải thích lý do tối ưu:** Nó giải quyết được bài toán gõ nhiều từ (Gõ "chế tạo vật liệu" sẽ tìm cả chữ "chế", "tạo", "vật", "liệu" dù nó nằm đảo lộn trong tên). Đồng thời nó hỗ trợ cơ chế chấm điểm xếp hạng `ts_rank` đưa kết quả liên quan nhất lên đầu, mà KHÔNG NGUY HIỂM / KHÔNG YÊU CẦU cài đặt thêm Extension như `pg_trgm` lúc đầu.
