<div align="center">
  <h3>ĐẠI HỌC QUỐC GIA HÀ NỘI</h3>
  <h3>TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN</h3>
  <h4>KHOA TOÁN - CƠ - TIN HỌC</h4>
  <br>
  <!-- Thay đường link logo nếu bạn có file ảnh thật ở dưới máy -->
  <img src="https://upload.wikimedia.org/wikipedia/vi/2/2e/Logo_Tr%C6%B0%E1%BB%9Dng_%C4%90%E1%BA%A1i_h%E1%BB%8Dc_Khoa_h%E1%BB%8Dc_T%E1%BB%B1_nhi%C3%AAn%2C_%C4%90%E1%BA%A1i_h%E1%BB%8Dc_Qu%E1%BB%91c_gia_H%C3%A0_N%E1%BB%99i.svg" width="150" alt="Logo HUS">
  <br><br>
  <hr style="border: 1.5px solid black; width: 80%;">
  <br><br>
  <h1>Báo cáo cuối kì</h1>
  <h2>MÔN: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG</h2>
  <h3>Đề tài: Hệ thống VNU Research Repository</h3>
  <br><br>
</div>

<div style="margin-left: 20%; font-size: 18px;">
  <p><b>Giảng viên hướng dẫn:</b> PGS.TS. Lê Hồng Phương</p>
  <p><b>Nhóm sinh viên thực hiện:</b></p>
  <ul>
    <li>Đinh Trường An - MSSV: 22001535</li>
    <li>Phạm Hoàng Anh - MSSV: 2001542</li>
    <li>Nguyễn Cảnh Hoàng - MSSV: 220015</li>
  </ul>
</div>

<div align="center">
  <br><br><br><br>
  <p><b>Hà Nội, Năm 2026</b></p>
</div>

<div style="page-break-after: always;"></div>

---

# MỤC LỤC

**DANH MỤC TỪ VIẾT TẮT**
**DANH SÁCH HÌNH VẼ**

**CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI**
1.1 Bối cảnh
1.2 Lý do chọn đề tài
1.3 Mục tiêu đề tài
  1.3.1 Mục tiêu tổng quát
  1.3.2 Mục tiêu cụ thể
1.4 Phạm vi hệ thống
1.5 Phương pháp thực hiện
1.6 Cấu trúc báo cáo

**CHƯƠNG 2. KHẢO SÁT VÀ PHÂN TÍCH YÊU CẦU**
2.1 Mô tả bài toán
2.2 Các tác nhân của hệ thống
2.3 Yêu cầu chức năng
  2.3.1 Yêu cầu chức năng tổng quát
  2.3.2 Yêu cầu chức năng theo module
2.4 Các Use case chính
2.5 Sơ đồ Use Case tổng quát
  2.5.1 Phân hệ Tra cứu và Khai thác
  2.5.2 Phân hệ Quản lý Đề tài
  2.5.3 Phân hệ Quản trị Hệ thống
2.6 Đặc tả một số Use Case quan trọng
  2.6.1 Use Case: Tìm kiếm và lọc đề tài
  2.6.2 Use Case: Đăng nhập hệ thống
  2.6.3 Use Case: Nộp đề tài nghiên cứu mới
  2.6.4 Use Case: Phê duyệt đề tài

**CHƯƠNG 3. PHÂN TÍCH HỆ THỐNG**
3.1 Phân rã chức năng
3.2 Phân tích theo module
  3.2.1 Module Xác thực và Tài khoản
  3.2.2 Module Nghiên cứu khoa học
  3.2.3 Module Tìm kiếm Nâng cao
  3.2.4 Module Quản trị
3.3 Luồng nghiệp vụ chính
  3.3.1 Luồng Tìm kiếm và Khai thác dữ liệu
  3.3.2 Luồng Đăng tài liệu và Phê duyệt
  3.3.3 Luồng Xác thực và Bảo mật
3.4 Đầu vào, đầu ra và kho dữ liệu
3.5 Các ràng buộc nghiệp vụ

**CHƯƠNG 4. THIẾT KẾ HỆ THỐNG**
4.1 Kiến trúc tổng thể
4.2 Công nghệ sử dụng
4.3 Thiết kế kiến trúc backend
  4.3.1 Lớp Domain
  4.3.2 Lớp Ứng dụng (Application)
  4.3.3 Lớp Hạ tầng (Infrastructure)
4.4 Thiết kế module chức năng
4.5 Thiết kế Cơ sở dữ liệu
  4.5.1 Sơ đồ thực thể liên kết (ERD)
  4.5.2 Từ điển dữ liệu
  4.5.3 Thiết kế Chỉ mục (Indexing)
4.6 Thiết kế API
  4.6.1 API Đăng nhập
  4.6.2 API Tìm kiếm Đề tài
  4.6.3 API Nộp đề tài
4.7 Thiết kế bảo mật
4.8 Thiết kế triển khai

**CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ**
5.1 Chiến lược kiểm thử
5.2 Một số ca kiểm thử tiêu biểu
5.3 Đánh giá kết quả
5.4 Giao diện hệ thống

**CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN**
6.1 Kết luận
6.2 Hướng phát triển

<div style="page-break-after: always;"></div>

---

# DANH SÁCH HÌNH VẼ

- **Hình 2.1:** Sơ đồ Use Case tổng quát toàn hệ thống
- **Hình 3.1:** Sơ đồ phân rã chức năng (Mindmap)
- **Hình 3.2:** Sơ đồ Tuần tự (Sequence Diagram) Luồng Tìm kiếm Cache-Aside
- **Hình 3.3:** Sơ đồ Tuần tự Luồng Nộp bài và Phê duyệt (Xóa Cache)
- **Hình 3.4:** Sơ đồ Tuần tự Luồng Xác thực và Thu hồi Token Blacklist
- **Hình 4.1:** Sơ đồ Kiến trúc hạ tầng hệ thống (Infrastructure Architecture)
- **Hình 4.2:** Sơ đồ Thực thể liên kết Cơ sở dữ liệu (ERD)

<div style="page-break-after: always;"></div>
