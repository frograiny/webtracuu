3.3.2 Luồng Đăng tài liệu và Phê duyệt (Publish & Approve Flow)
Luồng nghiệp vụ này liên quan đến 2 tác nhân là Tác giả (Sinh viên/Giảng viên) và Quản trị viên (Admin). Điểm phức tạp nhất của luồng này nằm ở việc duy trì "Tính nhất quán dữ liệu" (Data Consistency). Khi một đề tài mới được Admin phê duyệt (tức là thay đổi trạng thái trong CSDL), hệ thống bắt buộc phải thực hiện xóa (Invalidate) các kết quả tìm kiếm cũ đang nằm trong bộ đệm Redis. Nếu bỏ qua bước này, người dùng sẽ không thể tìm thấy đề tài vừa được duyệt cho đến khi Cache cũ tự hết hạn (có thể mất tới 1 giờ).

Sơ đồ Tuần tự dưới đây mô tả quá trình nộp và duyệt bài khép kín:

```mermaid
sequenceDiagram
    autonumber
    actor SV as Sinh viên (Tác giả)
    participant API as Backend API
    participant DB as PostgreSQL
    actor Admin as Quản trị viên
    participant Redis as Redis Cache

    %% Giai đoạn 1: Nộp bài
    rect rgb(240, 248, 255)
        Note over SV, DB: Giai đoạn 1: Tác giả nộp đề tài
        SV->>API: POST /api/v1/projects (Gửi Form + File PDF)
        activate API
        API->>API: Validate định dạng file (.pdf) & dung lượng (<50MB)
        API->>DB: INSERT INTO projects (status='PENDING')
        DB-->>API: Trả về Project ID
        API-->>SV: HTTP 201 Created (Nộp thành công, chờ duyệt)
        deactivate API
    end

    %% Giai đoạn 2: Admin duyệt bài
    rect rgb(255, 245, 238)
        Note over Admin, DB: Giai đoạn 2: Quản trị viên phê duyệt
        Admin->>API: GET /api/v1/projects?status=PENDING
        API-->>Admin: Trả về danh sách chờ duyệt
        
        Admin->>API: PUT /api/v1/projects/{id}/approve
        activate API
        API->>DB: UPDATE projects SET status='APPROVED'
        
        activate DB
        Note right of DB: DB Trigger tự động cập nhật<br/>cột search_vector cho FTS.
        DB-->>API: Update thành công
        deactivate DB
        
        Note over API, Redis: Bước cực kỳ quan trọng: Xóa Cache (Cache Invalidation)
        API->>Redis: Thực thi Background Task: Lệnh SCAN "search_cache:*"
        Redis-->>API: Trả về danh sách Keys liên quan
        API->>Redis: Lệnh DEL (Xóa toàn bộ các Keys cũ)
        
        API-->>Admin: HTTP 200 OK (Duyệt thành công)
        deactivate API
    end
```

Phân tích ngoại lệ:
- Tình huống: Tác giả nộp file vượt quá dung lượng cho phép.
- Xử lý: Frontend sẽ chặn ở phía Client, nhưng Backend cũng phải có lớp phòng thủ thứ hai. API sẽ kiểm tra `Content-Length` trong Header. Nếu > 50MB, lập tức ném lỗi HTTP 413 Payload Too Large và đóng luồng kết nối trước khi tải file vào bộ nhớ (RAM), giúp chống tấn công cạn kiệt tài nguyên.

3.3.3 Luồng Xác thực và Bảo mật (Auth & Security Flow)
Đây là luồng nghiệp vụ bảo vệ hệ thống. Khác với kiến trúc cũ lưu Session ID trong bộ nhớ máy chủ (gây khó khăn khi Scale-out nhiều máy chủ), hệ thống mới sử dụng JSON Web Token (JWT) kết hợp với danh sách đen (Blacklist) lưu trữ tập trung trên Redis.

Sơ đồ Tuần tự dưới đây mô tả quá trình cấp phát và thu hồi Token (Logout):

```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng
    participant API as Auth API
    participant DB as PostgreSQL (Users Table)
    participant Redis as Redis (Blacklist)

    %% Giai đoạn Login
    Note over User, DB: Luồng Đăng Nhập (Cấp phát Token)
    User->>API: POST /login (email, password)
    API->>DB: Truy vấn user theo email
    DB-->>API: Trả về Hashed_Password
    API->>API: So sánh bcrypt.verify(password, Hashed_Password)
    
    alt Sai mật khẩu
        API-->>User: HTTP 401 Unauthorized
    else Đúng mật khẩu
        API->>API: Sinh Access Token (15 phút) & Refresh Token (7 ngày)
        Note right of API: Token chứa UUID của User và chuỗi JTI (JWT ID) duy nhất
        API-->>User: Trả về cặp Token
    end

    %% Giai đoạn Logout
    Note over User, Redis: Luồng Đăng Xuất (Thu hồi Token tức thì)
    User->>API: POST /logout (Header: Bearer {Access_Token})
    API->>API: Giải mã Token, trích xuất chuỗi JTI và thời gian hết hạn (EXP)
    API->>Redis: SETEX blacklist:{jti} {thời_gian_còn_lại} "revoked"
    API-->>User: HTTP 200 OK (Đăng xuất thành công)

    %% Giai đoạn sau khi Logout
    Note over User, Redis: Người dùng cố tình dùng lại Token cũ đã Logout
    User->>API: GET /api/v1/protected-data (Header: Bearer {Access_Token_Cũ})
    API->>Redis: GET blacklist:{jti_cũ}
    Redis-->>API: Trả về chuỗi "revoked"
    API-->>User: HTTP 401 Unauthorized (Bị chặn ở tầng Middleware)
```

---

3.4 Đầu vào, đầu ra và kho dữ liệu (I/O & Data Stores)
Mọi luồng dữ liệu di chuyển trong hệ thống đều được kiểm soát chặt chẽ thông qua các mô hình chuẩn.

Bảng 3.1. Ma trận luồng dữ liệu theo Module:

| Module / Phân hệ | Dữ liệu Đầu vào (Inputs) | Dữ liệu Đầu ra (Outputs) | Nơi lưu trữ (Data Store) |
|---|---|---|---|
| **Xác thực (Auth)** | Thông tin đăng nhập (Email, Password), Chuỗi Token cũ cần Refresh. | Cặp chuỗi JWT (Access/Refresh), Thông báo lỗi xác thực. | Bảng `users` (PostgreSQL), Bộ nhớ `Blacklist` (Redis). |
| **Tìm kiếm (Search)** | Chuỗi ký tự (Query parameters: `q`, `page`, `filters`). | Mảng JSON chứa danh sách tóm tắt đề tài, Số lượng trang (Total pages). | Cột `search_vector` trong bảng `projects` (PostgreSQL). |
| **Quản lý Đề tài (Projects)** | Biểu mẫu thông tin (Form Data: Title, Abstract), File nhị phân (.pdf). | Mã định danh đề tài (UUID), File PDF (Stream tải xuống). | Bảng `projects` (PostgreSQL), File System hoặc AWS S3. |
| **Quản trị (Admin)** | Lệnh thay đổi trạng thái (Approve/Reject), Lệnh xóa bộ đệm. | Thông báo trạng thái thực thi, Dữ liệu báo cáo thống kê dạng chuỗi thời gian (Time-series). | Cột `status` (PostgreSQL), Metrics Database (Prometheus). |

---

3.5 Các ràng buộc nghiệp vụ (Business Rules & Constraints)
Để đảm bảo hệ thống vận hành đúng với bối cảnh học thuật của nhà trường và ngăn chặn việc lạm dụng, các ràng buộc (Rules) cứng sau đây được lập trình sâu vào tầng lõi:

1. Ràng buộc về dữ liệu (Data Validation Rules):
- Mật khẩu người dùng: Phải có độ dài tối thiểu 8 ký tự, bao gồm ít nhất một chữ hoa, một chữ số và một ký tự đặc biệt (chống Brute-force).
- Dung lượng file đính kèm: Kích thước tối đa cho mỗi file PDF nghiên cứu là 50MB. Hệ thống không chấp nhận bất kỳ định dạng nào khác (như .doc, .docx) để tránh nguy cơ đính kèm mã độc (Macro virus) và đảm bảo tính đồng nhất khi người dùng tải xuống.

2. Ràng buộc về phiên làm việc (Session Lifecycle):
- Tuổi thọ Access Token (Thời gian sống): Bắt buộc hết hạn sau 15 phút. Người dùng không được phép chỉnh sửa cấu hình này.
- Thu hồi tuyệt đối (Absolute Revocation): Ngay khi nhận được lệnh Logout, hệ thống bắt buộc phải đẩy ID của token đó vào Redis Blacklist trong thời gian < 10ms. Không có ngoại lệ.

3. Ràng buộc giới hạn lưu lượng (Smart Rate Limiting Rules):
Hệ thống sử dụng thuật toán Token Bucket (Thùng chứa thẻ) để kiểm soát số lượng truy vấn, chống lại các đợt cào dữ liệu (Crawling) làm sập DB.
- Đối với Người dùng đã đăng nhập (Authenticated): Dùng `User_ID` làm khóa nhận diện. Giới hạn: 100 Requests / 1 Phút.
- Đối với Khách (Guest): Hệ thống không có `User_ID`, nên sẽ tạo mã băm từ `IP Address` kết hợp với `User-Agent` của trình duyệt. Việc này giúp phân biệt các khách khác nhau dù họ dùng chung một mạng nội bộ (NAT). Giới hạn: 30 Requests / 1 Phút. Vi phạm sẽ bị trả về mã lỗi HTTP 429 Too Many Requests.
