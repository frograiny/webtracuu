DANH MỤC TỪ VIẾT TẮT

- API (Application Programming Interface): Giao diện lập trình ứng dụng.
- FTS (Full-Text Search): Tìm kiếm toàn văn.
- JWT (JSON Web Token): Tiêu chuẩn mở dùng để truyền tải thông tin an toàn dưới dạng JSON.
- SOA (Service-Oriented Architecture): Kiến trúc hướng dịch vụ.
- RBAC (Role-Based Access Control): Kiểm soát truy cập dựa trên vai trò.
- ERD (Entity-Relationship Diagram): Sơ đồ thực thể liên kết.
- RPS (Requests Per Second): Số lượng yêu cầu mỗi giây, thước đo tải của hệ thống.
- TSVECTOR: Kiểu dữ liệu trong PostgreSQL dùng để lưu trữ các từ vị (lexemes) phục vụ cho tìm kiếm toàn văn.
- GIN (Generalized Inverted Index): Cấu trúc chỉ mục đảo ngược, đặc biệt hiệu quả trong việc tìm kiếm văn bản.
- TTL (Time-To-Live): Thời gian tồn tại của dữ liệu trước khi bị xóa tự động (thường dùng trong bộ đệm Cache).
- NCKH: Nghiên cứu khoa học.
- VNU: Vietnam National University (Đại học Quốc gia).

---

CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI

1.1 Bối cảnh
Trong xu thế chuyển đổi số mạnh mẽ của nền giáo dục đại học, việc số hóa các tài liệu học thuật đang trở thành một yêu cầu mang tính bắt buộc. Tại các trường đại học lớn như Đại học Quốc gia (VNU), hàng năm có hàng ngàn đề tài nghiên cứu khoa học (NCKH), luận văn thạc sĩ, luận án tiến sĩ và khóa luận tốt nghiệp được bảo vệ thành công. Khối lượng tri thức này là vô giá, đóng vai trò nền tảng cho các thế hệ sinh viên và nghiên cứu sinh tiếp theo tham khảo và phát triển. 

Tuy nhiên, thực trạng hiện nay cho thấy việc quản lý và khai thác kho tàng dữ liệu này đang vấp phải nhiều rào cản nghiêm trọng. Dữ liệu thường bị phân tán ở các thư viện cục bộ của từng khoa, từng viện nghiên cứu trực thuộc mà không có sự liên thông. Việc chưa có một kho lưu trữ số hóa tập trung (Centralized Repository) dẫn đến tình trạng "ốc đảo dữ liệu". Sinh viên và giảng viên gặp vô vàn khó khăn khi muốn tra cứu một đề tài đã từng được thực hiện trước đây. Hậu quả là không hiếm các trường hợp đề tài nghiên cứu bị trùng lặp, gây lãng phí nghiêm trọng về thời gian, nhân lực và nguồn kinh phí tài trợ. Nhận thức được vấn đề này, nhu cầu về một hệ thống quản lý và tra cứu tập trung, có khả năng phục vụ hàng chục ngàn lượt truy cập cùng lúc đang trở nên cấp thiết hơn bao giờ hết.

1.2 Lý do chọn đề tài
Mặc dù trước đây đã có một số nỗ lực xây dựng các công cụ tra cứu nội bộ (được coi là các bản Prototype hoặc Lab project), nhưng khi đưa vào vận hành thực tế với khối lượng dữ liệu phình to, các hệ thống này đã bộc lộ những điểm yếu chí mạng về mặt kiến trúc và hiệu năng:

Thứ nhất, về thuật toán tra cứu: Hệ thống cũ đa phần sử dụng các câu lệnh truy vấn SQL truyền thống (cụ thể là toán tử `LIKE '%keyword%'`). Phương pháp này buộc cơ sở dữ liệu phải quét tuần tự qua toàn bộ các hàng (Table Scan) với độ phức tạp O(N). Khi số lượng đề tài lên tới con số hàng chục ngàn hoặc hàng triệu, một truy vấn tìm kiếm có thể mất đến vài giây hoặc thậm chí gây treo hệ thống. Thêm vào đó, thuật toán này hoàn toàn cứng nhắc, không hỗ trợ tìm kiếm mờ (Fuzzy Search), không nhận diện được lỗi gõ sai chính tả hay từ đồng nghĩa của người dùng.

Thứ hai, về kiến trúc hệ thống: Kiến trúc nguyên khối (Monolith) cũ thiếu đi khả năng mở rộng linh hoạt (Scalability). Trong những thời điểm cao điểm như "mùa bảo vệ luận văn" hoặc kỳ nộp đề xuất nghiên cứu, lượng truy cập (Traffic) tăng đột biến khiến máy chủ quá tải, dẫn đến tình trạng thắt cổ chai (Bottleneck) gây sập hệ thống (Downtime).

Thứ ba, về an toàn bảo mật: Việc quản lý phiên làm việc (Session) lỏng lẻo, thiếu cơ chế thu hồi quyền truy cập tức thời và không có giới hạn tần suất truy vấn (Rate Limiting) khiến hệ thống cũ trở thành mục tiêu dễ dàng cho các cuộc tấn công từ chối dịch vụ (DDoS) hoặc các bot cào dữ liệu (Web Scraping).

Từ những bất cập trên, việc chỉ đơn thuần vá lỗi (patching) hệ thống cũ là không khả thi. Dự án "Xây dựng Hệ thống VNU Research Repository - Enterprise Edition" được chọn nhằm đập bỏ hoàn toàn kiến trúc cũ, tái thiết kế và xây dựng lại từ đầu một hệ thống Backend cốt lõi hoàn toàn mới, áp dụng các kỹ thuật tiên tiến nhất để giải quyết triệt để bài toán về hiệu năng và bảo mật.

1.3 Mục tiêu đề tài

1.3.1 Mục tiêu tổng quát
Mục tiêu bao trùm của dự án là thiết kế, phát triển và triển khai một hệ thống API Backend hướng dịch vụ (SOA) vững chắc, đóng vai trò như một "Search Engine" (Động cơ tìm kiếm) chuyên biệt cho dữ liệu NCKH. Hệ thống phải đảm bảo các tiêu chí chuẩn Doanh nghiệp (Enterprise Production): tốc độ phản hồi siêu thực, tính sẵn sàng cao, bảo mật chặt chẽ và dễ dàng mở rộng hạ tầng trong tương lai.

1.3.2 Mục tiêu cụ thể
Để hiện thực hóa mục tiêu tổng quát, dự án đặt ra các chỉ tiêu đo lường kỹ thuật cụ thể như sau:
- Về hiệu năng tìm kiếm: Triển khai Full-Text Search (FTS) nâng cao, đảm bảo thời gian trễ (Latency) của mọi API tìm kiếm luôn dưới 100ms ở phân vị thứ 95 (P95), bất chấp quy mô dữ liệu.
- Về tính thông minh: Tích hợp công nghệ phân tích từ vựng (Lexer) và tìm kiếm Trigram, cho phép người dùng tìm thấy kết quả ngay cả khi gõ sai chính tả hoặc thiếu dấu (Fuzzy Search).
- Về khả năng chịu tải: Ứng dụng mô hình bộ đệm phân tán (Distributed Cache) qua Redis để giảm thiểu 80% tải đọc trực tiếp vào Cơ sở dữ liệu.
- Về độ khả dụng: Đạt chỉ số Uptime 99.9% thông qua việc Container hóa toàn bộ ứng dụng (Docker) và tích hợp cơ chế tự động khôi phục (Auto-healing healthchecks).
- Về bảo mật: Xây dựng cơ chế xác thực kép (Dual-Token JWT) kết hợp danh sách đen (Blacklist) stateful, cho phép thu hồi quyền truy cập ngay lập tức; đồng thời áp dụng thuật toán Token Bucket để chống Spam/DDoS.

1.4 Phạm vi hệ thống
Hệ thống VNU Research Repository (Enterprise Edition) tập trung chủ yếu vào việc cung cấp một lõi (Core) xử lý mạnh mẽ. Phạm vi của dự án bao gồm:
- Thiết kế và tối ưu hóa Cơ sở dữ liệu PostgreSQL cho các nghiệp vụ đặc thù về tra cứu văn bản.
- Xây dựng hệ thống RESTful API hoàn chỉnh cung cấp dữ liệu cho mọi nền tảng (Web, Mobile).
- Triển khai phân hệ xác thực và phân quyền (Auth & RBAC) cực kỳ nghiêm ngặt.
- Tích hợp lớp Giám sát hệ thống (Observability Layer) để đo lường tự động các chỉ số kỹ thuật và chỉ số nghiệp vụ.

Giới hạn dự án: Dự án này không đi sâu vào việc xây dựng giao diện người dùng (Frontend UI/UX) phức tạp, mà sẽ cung cấp một số giao diện cơ bản và tài liệu OpenAPI (Swagger) chuẩn mực để các team Frontend khác có thể dễ dàng đấu nối.

1.5 Phương pháp thực hiện
Dự án được thực hiện dựa trên phương pháp phát triển linh hoạt (Agile), chia nhỏ quá trình nâng cấp thành 4 giai đoạn (Phases) tái cấu trúc liên tục:
- Giai đoạn 1: Chuẩn hóa lại cấu trúc CSDL và di chuyển dữ liệu. Áp dụng GIN Index và TSVECTOR.
- Giai đoạn 2: Phát triển các API tìm kiếm bằng FastAPI và tích hợp luồng chuẩn hóa từ khóa.
- Giai đoạn 3: Tích hợp Redis để triển khai chiến lược Cache-Aside và Stateful JWT Blacklist.
- Giai đoạn 4: Đóng gói toàn bộ ứng dụng bằng Docker, thiết lập môi trường giám sát bằng Prometheus và Grafana, kiểm thử tải (Load Testing) và đóng gói bàn giao.

1.6 Cấu trúc báo cáo
Báo cáo này được trình bày một cách logic, đi từ khảo sát thực trạng đến thiết kế chi tiết, bao gồm 6 chương chính và phụ lục:
- Chương 1. Giới thiệu đề tài: Trình bày bối cảnh, lý do, mục tiêu và phạm vi của dự án.
- Chương 2. Khảo sát và phân tích yêu cầu: Nhận diện các tác nhân, phân tích yêu cầu chức năng và phi chức năng, đặc tả chi tiết các Use Case cốt lõi.
- Chương 3. Phân tích hệ thống: Mô tả kiến trúc module, các luồng nghiệp vụ chính và luồng xử lý dữ liệu.
- Chương 4. Thiết kế hệ thống: Cung cấp bản thiết kế chuyên sâu về Kiến trúc, CSDL (ERD, Data Dictionary), API, và các phân hệ bảo mật.
- Chương 5. Kiểm thử và đánh giá: Đưa ra chiến lược kiểm thử, danh sách các ca kiểm thử (Test Cases) tiêu biểu và kết quả đánh giá hệ thống.
- Chương 6. Kết luận và hướng phát triển: Tổng kết những thành quả đạt được và định hướng mở rộng hệ thống bằng AI hoặc Microservices trong tương lai.
- Phụ lục: Danh sách và mô tả tóm tắt toàn bộ các endpoints API của hệ thống.
