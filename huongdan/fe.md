1. Phía Frontend (UI/UX Reskin - Làm lại giao diện)

Tạm bỏ giao diện Dashboard bo tròn hiện tại, chuyển sang form Cổng thông tin học thuật.

[ ] Xây dựng Layout chuẩn:

Topbar: Thanh ngang nhỏ trên cùng màu xám đậm/xanh đậm chứa Số điện thoại, Email, Link nội bộ.

Header: Background trắng. Trái là Logo + Tên khoa (2 dòng: Tiếng Việt in đậm, Tiếng Anh nhỏ hơn). Phải là thanh Navigation (NGHIÊN CỨU, TUYỂN DỤNG, ĐÀO TẠO...) viết IN HOA.

Main Content (Chia lưới 75-25): - Cột trái (75%): Khu vực chính để hiển thị Tiêu đề mục (VD: | NGHIÊN CỨU KHOA HỌC) và Thanh tìm kiếm.

Cột phải (25%): Sidebar chứa "BẢNG TIN KHOA" và "LIÊN KẾT".

[ ] Chỉnh sửa Component AdvancedSearchBar:

Chuyển góc bo tròn (rounded-2xl) thành góc vuông hoặc bo rất nhẹ (rounded-md, rounded-sm) để hợp với phong cách web nhà nước/đại học.

Viền mỏng, dùng màu xanh của trường làm màu chủ đạo (focus border).

Giữ nguyên các chức năng cốt lõi: Debounce, Dropdown phân loại (Đề tài/Luận văn/Khóa luận), và Mock API.

2. Phía Backend (API - Python/NodeJS)

(Giữ nguyên như kế hoạch cũ)

[ ] Cập nhật Database Schema: Thêm cột document_type và implementation_year.

[ ] Nâng cấp thuật toán Tìm kiếm: Dùng PostgreSQL + Extension pg_trgm để đánh Index (GIN).

[ ] Cập nhật Search API Endpoint: Nhận tham số ?q=từ_khóa&type=loại_tài_liệu và xử lý CORS.