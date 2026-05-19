CHƯƠNG 2. KHẢO SÁT VÀ PHÂN TÍCH YÊU CẦU

2.1 Mô tả bài toán
Bài toán đặt ra cho hệ thống VNU Research Repository là quản lý toàn bộ vòng đời của các tài liệu học thuật (nghiên cứu khoa học, khóa luận, luận văn) từ thời điểm sơ khởi khi tác giả (sinh viên/giảng viên) nộp đề xuất, trải qua quá trình kiểm duyệt khắt khe, cho đến khi được công bố chính thức và phục vụ tra cứu. Song song đó, bài toán cốt lõi và khó khăn nhất là làm sao cung cấp một "động cơ tìm kiếm" (Search Engine) đủ mạnh để người dùng có thể trích xuất chính xác thông tin họ cần giữa biển dữ liệu khổng lồ.

Cụ thể, quy trình nghiệp vụ hiện tại (As-Is) đang gặp phải các vấn đề:
- Tác giả nộp đề tài qua email hoặc bản cứng, gây khó khăn cho việc lưu trữ và theo dõi tiến độ phê duyệt.
- Quản trị viên phải tổng hợp thủ công vào các file Excel hoặc phần mềm quản lý nội bộ rời rạc, dễ dẫn đến sai sót hoặc thất lạc dữ liệu.
- Người dùng khi cần tra cứu một đề tài thường phải đến tận thư viện để tra cứu mục lục vật lý, hoặc sử dụng hệ thống tra cứu trực tuyến cũ rất chậm chạp. Hệ thống cũ chỉ tìm kiếm chính xác theo từng ký tự (Exact Match), nghĩa là nếu người dùng gõ sai một dấu nháy hoặc thiếu một chữ cái (ví dụ gõ "nghiên cuu" thay vì "nghiên cứu"), hệ thống sẽ trả về kết quả rỗng (Zero-result).

Quy trình nghiệp vụ mong muốn (To-Be) của hệ thống mới:
- Quy trình số hóa 100%: Mọi tài liệu đều được nộp, lưu trữ và kiểm duyệt trực tuyến trên một nền tảng duy nhất.
- Kiểm duyệt theo luồng (Workflow): Tài liệu nộp lên sẽ ở trạng thái "Chờ duyệt" (Pending). Quản trị viên sẽ nhận được thông báo, tiến hành xem xét và chuyển trạng thái sang "Đã duyệt" (Approved) hoặc "Từ chối" (Rejected) kèm lý do.
- Tra cứu thông minh: Người dùng chỉ cần nhập từ khóa (kể cả có lỗi đánh máy nhỏ), hệ thống sử dụng thuật toán phân tích ngôn ngữ tự nhiên cơ bản để tự động chuẩn hóa từ khóa, phân tích từ đồng nghĩa (ví dụ: "AI" tương đương "Trí tuệ nhân tạo") và trả về kết quả chỉ trong tích tắc. Kết quả được xếp hạng (Ranking) thông minh, ưu tiên các đề tài có từ khóa xuất hiện ở Tiêu đề hơn là ở Tóm tắt.
- Kiểm soát truy cập: Tôn trọng bản quyền tác giả, những người dùng chưa đăng nhập (Khách) chỉ được phép xem Tóm tắt (Abstract) và thông tin cơ bản. Để xem và tải toàn văn (Full-text PDF), người dùng bắt buộc phải đăng nhập bằng tài khoản nội bộ của trường.

2.2 Các tác nhân của hệ thống
Tác nhân (Actor) là những thực thể (con người hoặc hệ thống khác) có tương tác trực tiếp với hệ thống. Dựa trên phân tích nghiệp vụ, hệ thống VNU Research Repository xác định 3 nhóm tác nhân chính với các quyền hạn được phân cấp rõ ràng (RBAC):

1. Khách (Guest / Unauthenticated User):
- Đặc điểm: Là những người truy cập vào hệ thống nhưng chưa thực hiện thao tác đăng nhập, hoặc không có tài khoản nội bộ của nhà trường (ví dụ: các nhà nghiên cứu từ trường khác, doanh nghiệp, hoặc công chúng).
- Quyền hạn: Bị giới hạn nhiều nhất. Chỉ được phép sử dụng chức năng tìm kiếm cơ bản, lọc kết quả, và xem siêu dữ liệu (Metadata) của các đề tài đã được công bố công khai (Public). Không được phép tải file đính kèm hay xem nội dung toàn văn.

2. Người dùng nội bộ (Sinh viên / Giảng viên - Authenticated User):
- Đặc điểm: Là các cá nhân đang học tập và công tác tại VNU, đã được cấp tài khoản định danh (thường tích hợp qua hệ thống SSO hoặc email @vnu.edu.vn). 
- Quyền hạn: Kế thừa toàn bộ quyền của Khách. Ngoài ra, họ được đặc quyền truy cập và tải xuống toàn văn các tài liệu nghiên cứu. Họ cũng đóng vai trò là "Tác giả" (Creator), có quyền nộp (Upload) các đề tài nghiên cứu mới của chính mình lên hệ thống, theo dõi trạng thái phê duyệt của đề tài đó, chỉnh sửa trước khi được duyệt, và lưu trữ (Bookmark) các tài liệu của người khác vào danh sách yêu thích.

3. Quản trị viên (Administrator / Moderator):
- Đặc điểm: Là các cán bộ quản lý thuộc thư viện, phòng đào tạo, hoặc phòng nghiên cứu khoa học. Họ là những người vận hành và chịu trách nhiệm về nội dung của hệ thống.
- Quyền hạn: Nắm giữ đặc quyền cao nhất (Superuser). Họ không nộp đề tài mà đóng vai trò "Người gác cổng". Quản trị viên có quyền xem xét mọi đề tài đang chờ duyệt để đưa ra quyết định phê duyệt hoặc từ chối. Họ cũng quản lý danh sách người dùng (khóa/mở khóa tài khoản khi có dấu hiệu lạm dụng), quản lý các danh mục từ khóa (Tags), danh mục lĩnh vực, và cấu hình từ điển đồng nghĩa cho Search Engine. Hơn nữa, họ có quyền truy cập vào bảng điều khiển (Dashboard) để xem các báo cáo thống kê về lưu lượng truy cập và hành vi tìm kiếm.

2.3 Yêu cầu chức năng
Dựa trên các tác nhân đã xác định, yêu cầu chức năng (những gì hệ thống bắt buộc phải làm được) được định nghĩa chi tiết.

2.3.1 Yêu cầu chức năng tổng quát
Ở mức độ cao nhất, hệ thống phải đáp ứng 4 khối chức năng tổng quát sau:
- Khối Quản lý Định danh & Phân quyền: Đảm bảo chỉ những người có thẩm quyền mới được truy cập vào dữ liệu nhạy cảm. Quản lý vòng đời của phiên làm việc một cách an toàn.
- Khối Quản lý Tài liệu NCKH: Số hóa quy trình từ khâu nộp bài, lưu trữ siêu dữ liệu, lưu trữ file vật lý, cho đến khâu kiểm duyệt và xuất bản.
- Khối Tra cứu & Tìm kiếm: Cung cấp giao diện và bộ máy tìm kiếm văn bản toàn diện, tốc độ cao, hỗ trợ đa dạng các bộ lọc.
- Khối Quản trị & Giám sát: Cung cấp công cụ cho Admin vận hành hệ thống và theo dõi sức khỏe của ứng dụng.

2.3.2 Yêu cầu chức năng theo module
Để phục vụ cho quá trình thiết kế kiến trúc Microservices/Modular sau này, các yêu cầu được chia nhỏ thành các Module độc lập:

1. Module Xác thực và Tài khoản (Auth & Identity Module):
- Cho phép người dùng đăng nhập bằng tên đăng nhập/email và mật khẩu.
- Cho phép người dùng đăng xuất (Hệ thống phải lập tức vô hiệu hóa token hiện tại, đưa vào Blacklist).
- Tự động làm mới phiên làm việc (Refresh Token) để người dùng không phải đăng nhập liên tục.
- Cho phép người dùng cập nhật thông tin cá nhân cơ bản và đổi mật khẩu.
- (Tính năng mở rộng): Hỗ trợ đăng nhập một lần (SSO) qua Google hoặc Microsoft.

2. Module Nghiên cứu khoa học (Research Management Module):
- Dành cho Tác giả:
  + Nộp thông tin đề tài mới (Tiêu đề, Tóm tắt, Tác giả phụ, Lĩnh vực).
  + Tải lên file PDF chứa nội dung toàn văn (có giới hạn dung lượng).
  + Chỉnh sửa thông tin đề tài (chỉ khi đang ở trạng thái Pending hoặc Rejected).
  + Xóa đề tài (nếu chưa được duyệt).
- Dành cho Quản trị viên:
  + Liệt kê danh sách các đề tài phân loại theo trạng thái (Pending, Approved, Rejected).
  + Phê duyệt hoặc từ chối đề tài (kèm theo ghi chú lý do từ chối để tác giả sửa lại).
  + Xóa vĩnh viễn hoặc ẩn (Soft-delete) một đề tài vi phạm dù đã được duyệt.

3. Module Tìm kiếm nâng cao (Advanced Search Engine Module):
- Tra cứu theo từ khóa tự do: Khớp từ khóa trên các trường Tiêu đề, Tác giả, và Tóm tắt.
- Tìm kiếm mờ (Fuzzy Search): Gợi ý và trả về kết quả đúng kể cả khi người dùng gõ sai chính tả (chênh lệch 1-2 ký tự).
- Lọc nâng cao (Facet Filtering): Cho phép kết hợp nhiều điều kiện lọc như: Lọc theo năm công bố, lọc theo trạng thái, lọc theo tác giả, lọc theo khoa/viện.
- Sắp xếp kết quả (Sorting): Sắp xếp theo độ liên quan (Relevance score - mặc định), theo thời gian mới nhất/cũ nhất, theo lượt xem.
- Phân trang (Pagination): Chia nhỏ kết quả tìm kiếm (ví dụ 20 kết quả/trang) để tối ưu hóa thời gian tải và giảm tải cho băng thông.

4. Module Quản trị hệ thống (System Admin Module):
- Quản lý danh mục: Thêm, sửa, xóa các Tags, Categories (Lĩnh vực nghiên cứu).
- Quản lý từ điển đồng nghĩa (Synonyms): Admin có thể định nghĩa "AI" = "Trí tuệ nhân tạo" để Search Engine hiểu được.
- Quản lý tài khoản: Xem danh sách toàn bộ người dùng, cấp quyền Admin cho người khác, khóa (Ban) tài khoản người dùng vi phạm.
- Thống kê (Analytics): Xem số lượng đề tài được đăng theo tháng, các từ khóa được tìm kiếm nhiều nhất (Trending), và các truy vấn không trả về kết quả (Zero-result queries) để cải thiện dữ liệu.

2.4 Các Use case chính
Từ các yêu cầu chức năng trên, hệ thống định nghĩa danh sách các Use Case (Trường hợp sử dụng) cốt lõi như sau. Các Use Case này sẽ được đặc tả chi tiết các bước thực hiện ở phần sau.

- Nhóm Use Case Tra cứu (Dành cho Khách & Người dùng):
  + UC01 - Tìm kiếm đề tài: Người dùng nhập từ khóa và nhận lại danh sách đề tài phù hợp.
  + UC02 - Lọc và phân loại: Kết hợp các tiêu chí (năm, lĩnh vực) để thu hẹp kết quả.
  + UC03 - Xem chi tiết đề tài: Đọc thông tin tóm tắt và siêu dữ liệu của một đề tài cụ thể.

- Nhóm Use Case Tài khoản & Cá nhân (Dành cho Người dùng đã xác thực):
  + UC04 - Đăng nhập / Đăng xuất: Tham gia và rời khỏi phiên làm việc an toàn.
  + UC05 - Tải tài liệu toàn văn: Xác thực quyền và tải file PDF.
  + UC06 - Lưu trữ đề tài (Bookmark): Đưa đề tài vào danh sách đọc sau.

- Nhóm Use Case Đăng tải (Dành cho Tác giả):
  + UC07 - Nộp đề tài mới: Khởi tạo dữ liệu và tải file lên hệ thống chờ duyệt.
  + UC08 - Quản lý đề tài cá nhân: Chỉnh sửa, theo dõi trạng thái các đề tài do mình nộp.

- Nhóm Use Case Quản trị (Dành cho Admin):
  + UC09 - Phê duyệt đề tài: Đánh giá và thay đổi trạng thái (Approved/Rejected) của tài liệu.
  + UC10 - Quản lý danh mục & Từ điển: Thao tác cấu hình hệ thống (Tags, Synonyms).
  + UC11 - Quản lý tài khoản người dùng: Cấp quyền, khóa tài khoản, reset mật khẩu.
  + UC12 - Xem báo cáo thống kê: Truy cập Dashboard để xem biểu đồ và số liệu hoạt động.
