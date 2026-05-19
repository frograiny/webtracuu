CHƯƠNG 4. THIẾT KẾ HỆ THỐNG

Đây là chương trọng tâm của báo cáo, trình bày chi tiết cách chuyển đổi từ các yêu cầu nghiệp vụ (Chương 2) và phân tích luồng (Chương 3) thành các bản vẽ kỹ thuật (Technical Blueprints). Các quyết định về kiến trúc và công nghệ được lựa chọn đều hướng tới việc thỏa mãn hai tiêu chí lớn nhất: Hiệu năng cao (High Performance) và Khả năng mở rộng (Scalability).

4.1 Kiến trúc tổng thể (System Architecture)
Hệ thống VNU Research Repository được thiết kế theo mô hình Kiến trúc hướng dịch vụ (Service-Oriented Architecture - SOA) kết hợp với các nguyên lý của Microservices ở tầng hạ tầng. Thay vì gộp chung giao diện (Frontend) và xử lý logic (Backend) vào một khối nguyên khối (Monolith), hệ thống phân tách hoàn toàn hai phần này, giao tiếp với nhau duy nhất thông qua RESTful API.

Sơ đồ Kiến trúc hạ tầng (Infrastructure Architecture) dưới đây minh họa các thành phần vật lý và logic của hệ thống:

```mermaid
graph TD
    %% Tầng Client
    subgraph "Tầng Trình diễn (Presentation Layer)"
        WebClient[Trình duyệt Web (ReactJS)]
        MobileApp[Ứng dụng Mobile]
    end

    %% Tầng Proxy & Load Balancer
    subgraph "Tầng Proxy (Edge Layer)"
        Nginx[Nginx Reverse Proxy / Load Balancer]
    end

    %% Tầng Ứng dụng Backend
    subgraph "Tầng Ứng dụng (Application Layer)"
        FastAPI_1[FastAPI Server - Instance 1]
        FastAPI_2[FastAPI Server - Instance 2]
        FastAPI_N[FastAPI Server - Instance N]
    end

    %% Tầng Dữ liệu
    subgraph "Tầng Dữ liệu (Data Layer)"
        Redis[(Redis Cache - In-memory)]
        Postgres[(PostgreSQL - FTS Engine)]
    end

    %% Tầng Giám sát
    subgraph "Tầng Giám sát (Observability Layer)"
        Prometheus[Prometheus Metric Scraper]
        Grafana[Grafana Dashboard]
    end

    %% Luồng kết nối
    WebClient -->|HTTPS / REST| Nginx
    MobileApp -->|HTTPS / REST| Nginx

    Nginx -->|Round Robin| FastAPI_1
    Nginx -->|Round Robin| FastAPI_2
    Nginx -->|Round Robin| FastAPI_N

    FastAPI_1 <-->|Read/Write/PubSub| Redis
    FastAPI_2 <-->|Read/Write/PubSub| Redis
    FastAPI_N <-->|Read/Write/PubSub| Redis

    FastAPI_1 <-->|SQL/ORM| Postgres
    FastAPI_2 <-->|SQL/ORM| Postgres
    FastAPI_N <-->|SQL/ORM| Postgres

    Prometheus -.->|Scrape /metrics| FastAPI_1
    Prometheus -.->|Scrape /metrics| FastAPI_2
    Grafana -.->|Query PromQL| Prometheus
```

Giải thích kiến trúc:
1. Reverse Proxy: Nginx đứng đầu tiên để nhận Request, đảm nhận việc giải mã SSL (SSL Termination) và phân tải (Load Balancing) thuật toán Round Robin xuống các máy chủ Backend, đồng thời phục vụ các tệp tĩnh (Static files) nếu có.
2. Horizontal Scaling: Các instance của FastAPI chạy song song (Stateless). Khi có đợt traffic lớn, hệ thống chỉ cần khởi tạo thêm các container FastAPI mới mà không làm gián đoạn dịch vụ.
3. Caching Layer: Redis đóng vai trò giảm tải 80% gánh nặng đọc dữ liệu cho PostgreSQL và quản lý Token Blacklist.
4. Database Layer: PostgreSQL đóng vai trò lưu trữ vĩnh viễn (Persistent Storage) và kiêm luôn vai trò Search Engine thông qua tính năng Full-Text Search.

---

4.2 Công nghệ sử dụng
Sự lựa chọn công nghệ cho dự án này không dựa trên xu hướng, mà dựa trên khả năng giải quyết trực tiếp các nút thắt (Bottlenecks) đã phân tích.

Bảng 4.1. Ma trận lựa chọn công nghệ (Tech Stack)

| Thành phần | Công nghệ lựa chọn | Lý do lựa chọn (Trade-offs & Justification) |
|---|---|---|
| **Ngôn ngữ Backend** | Python 3.11+ | Hệ sinh thái thư viện AI/Data khổng lồ (chuẩn bị cho hướng phát triển AI sau này). Cú pháp ngắn gọn, dễ bảo trì. |
| **Web Framework** | FastAPI | Hỗ trợ lập trình bất đồng bộ (Asynchronous - `async/await`) mặc định, giúp xử lý đồng thời hàng ngàn Request (Concurrency) tốt hơn nhiều so với Django hay Flask. Tự động sinh tài liệu OpenAPI (Swagger). |
| **Cơ sở dữ liệu** | PostgreSQL 15+ | Khả năng hỗ trợ kiểu dữ liệu JSONB và tính năng TSVECTOR cho tìm kiếm văn bản cực kỳ mạnh mẽ. Là sự thay thế hoàn hảo cho Elasticsearch trong giai đoạn đầu, giúp giảm độ phức tạp vận hành. |
| **Bộ nhớ đệm (Cache)** | Redis 7+ | Tốc độ đọc/ghi dữ liệu trên RAM cực nhanh (độ trễ tính bằng microsecond). Hỗ trợ TTL (tự động xóa) và cấu trúc dữ liệu Set hữu ích cho Token Blacklist. |
| **Truy cập dữ liệu** | SQLAlchemy (AsyncORM) | ORM (Object-Relational Mapping) mạnh mẽ nhất của Python, giúp trừu tượng hóa các câu lệnh SQL thành đối tượng, hỗ trợ Async an toàn. |
| **Quản lý phiên** | PyJWT | Thư viện chuẩn để mã hóa và giải mã JSON Web Token. |
| **Đóng gói & Triển khai** | Docker & Docker Compose | Đảm bảo sự đồng nhất tuyệt đối giữa môi trường lập trình (Dev) và môi trường thật (Production). Tránh lỗi "It works on my machine". |
| **Giám sát (Monitoring)**| Prometheus + Grafana | Chuẩn công nghiệp cho việc thu thập Metrics (Prometheus) và vẽ biểu đồ trực quan (Grafana). Tương thích hoàn hảo với kiến trúc Microservices. |

---

4.3 Thiết kế kiến trúc backend (Backend Architecture Pattern)
Để đảm bảo mã nguồn (Codebase) không bị rối loạn khi dự án phình to, Backend của hệ thống áp dụng một biến thể của Kiến trúc Sạch (Clean Architecture), chia dự án thành 3 lớp (Layers) tách biệt hoàn toàn. Nguyên lý cốt lõi là: Các lớp bên ngoài phụ thuộc vào các lớp bên trong, lớp bên trong không biết gì về lớp bên ngoài (Dependency Rule).

4.3.1 Lớp Domain (Domain Layer)
- Vị trí: Nằm ở trung tâm kiến trúc.
- Vai trò: Chứa các định nghĩa thực thể (Entities) cốt lõi và các quy tắc nghiệp vụ (Business Rules) không bao giờ thay đổi dù Framework hay Database có đổi.
- Nội dung cụ thể: Bao gồm các lớp `User`, `Project`, `Category`. Chứa các hàm nghiệp vụ như kiểm tra tính hợp lệ của trạng thái dự án (không thể chuyển từ `REJECTED` sang `APPROVED` mà không qua `PENDING`). Lớp này hoàn toàn không chứa bất kỳ thư viện nào liên quan đến SQL hay HTTP.

4.3.2 Lớp Ứng dụng (Application Layer / Services)
- Vị trí: Bao bọc bên ngoài lớp Domain.
- Vai trò: Chứa các "Use Cases" (Trường hợp sử dụng) đã định nghĩa ở Chương 2. Lớp này đứng ra điều phối luồng dữ liệu (Orchestration).
- Nội dung cụ thể: Các lớp `AuthService`, `ProjectService`, `SearchService`. 
  Ví dụ: Khi gọi hàm `ProjectService.approve_project(id)`, hàm này sẽ gọi DB để cập nhật trạng thái, đồng thời gọi Redis để xóa Cache, và gọi Service Gửi Email. Lớp Application chịu trách nhiệm móc nối các nghiệp vụ này lại với nhau.

4.3.3 Lớp Hạ tầng (Infrastructure Layer & Presentation)
- Vị trí: Nằm ở ngoài cùng.
- Vai trò: Nơi giao tiếp với thế giới bên ngoài (HTTP, Database, Redis, File System).
- Nội dung cụ thể:
  - **Tầng Router/Controller (FastAPI):** Các file `routers/projects.py`. Chịu trách nhiệm nhận HTTP Request, trích xuất tham số, gọi hàm ở lớp Application, và trả về HTTP Response (JSON).
  - **Tầng Repository (Data Access):** Các file `repositories/project_repo.py`. Sử dụng SQLAlchemy để viết các câu lệnh truy vấn xuống PostgreSQL, và chuyển đổi dữ liệu thô từ Database thành các Object của lớp Domain.
  - **Tầng External:** Các đoạn code kết nối trực tiếp với Redis, hoặc các hàm thao tác lưu file PDF xuống ổ cứng.

Việc phân tách này giúp hệ thống dễ dàng thực hiện Unit Test. Khi muốn test nghiệp vụ trong `ProjectService`, lập trình viên chỉ cần tạo ra các Mock Object thay thế cho `Database Repository` mà không cần phải chạy một Database thật.
