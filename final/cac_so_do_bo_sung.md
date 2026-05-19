# DANH SÁCH CÁC SƠ ĐỒ BỔ SUNG
*(Bạn copy từng block mã dưới đây để paste vào các chương tương ứng)*

---
## CHƯƠNG 2

### Hình 2.2: Sơ đồ use case cho phân hệ Tra cứu và Khai thác
```mermaid
flowchart LR
    Khach((Khách))
    User((Người dùng))
    
    subgraph "Phân hệ Tra cứu"
        direction TB
        UC1([Nhập từ khóa tìm kiếm])
        UC2([Lọc kết quả nâng cao])
        UC3([Xem chi tiết Metadata])
        UC4([Xem toàn văn Online])
        UC5([Tải xuống file PDF])
    end
    
    Khach --> UC1
    Khach --> UC2
    Khach --> UC3
    
    User -.->|Kế thừa| Khach
    User --> UC4
    User --> UC5
```

### Hình 2.3: Sơ đồ use case cho phân hệ Quản lý Đề tài
```mermaid
flowchart LR
    TacGia((Tác giả))
    
    subgraph "Phân hệ Quản lý Đề tài"
        UC1([Nộp đề tài mới])
        UC2([Chỉnh sửa đề tài bị từ chối])
        UC3([Xóa đề tài nháp])
        UC4([Theo dõi trạng thái kiểm duyệt])
    end
    
    TacGia --> UC1
    TacGia --> UC2
    TacGia --> UC3
    TacGia --> UC4
```

### Hình 2.4: Sơ đồ use case cho phân hệ Quản trị hệ thống
```mermaid
flowchart LR
    Admin((Quản trị viên))
    
    subgraph "Phân hệ Quản trị"
        UC1([Xem danh sách chờ duyệt])
        UC2([Phê duyệt đề tài])
        UC3([Từ chối đề tài kèm lý do])
        UC4([Khóa tài khoản vi phạm])
        UC5([Cập nhật từ điển Synonyms])
        UC6([Xuất báo cáo thống kê])
    end
    
    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
```

---
## CHƯƠNG 3

### Hình 3.4: Biểu đồ hoạt động (Activity Diagram) luồng Đăng và duyệt bài
```mermaid
stateDiagram-v2
    [*] --> NhapThongTin : Tác giả bắt đầu
    NhapThongTin --> UploadFile : Điền Form
    UploadFile --> KiemTraFile : Gửi Request
    
    state KiemTraFile {
        [*] --> CheckSize
        CheckSize --> CheckFormat
    }
    
    KiemTraFile --> DRAFT : Lưu nháp
    DRAFT --> PENDING : Submit
    PENDING --> XemXet : Admin nhận thông báo
    
    state XemXet {
        [*] --> DocPDF
        DocPDF --> KiemTraDaoVan
    }
    
    XemXet --> APPROVED : Hợp lệ
    XemXet --> REJECTED : Không hợp lệ
    
    REJECTED --> NhapThongTin : Yêu cầu sửa
    APPROVED --> XoaCache : Kích hoạt Event
    XoaCache --> [*] : Hoàn tất xuất bản
```

### Hình 3.2: Biểu đồ hoạt động (Activity Diagram) luồng Tìm kiếm
```mermaid
stateDiagram-v2
    [*] --> NhapTuKhoa
    NhapTuKhoa --> ChuanHoa
    ChuanHoa --> CheckCache
    
    state CheckCache {
        [*] --> GoiRedis
        GoiRedis --> CacheHit : Tìm thấy
        GoiRedis --> CacheMiss : Không thấy
    }
    
    CheckCache --> TraVeKq : Cache Hit
    CheckCache --> QueryDB : Cache Miss
    
    state QueryDB {
        [*] --> FTS_Operator
        FTS_Operator --> TinhDiemRank
        TinhDiemRank --> Sort
    }
    
    QueryDB --> LuuCacheMoi
    LuuCacheMoi --> TraVeKq
    TraVeKq --> [*]
```

### Hình 3.6: Biểu đồ hoạt động luồng Quản trị và phân quyền
```mermaid
stateDiagram-v2
    [*] --> RequestDen
    RequestDen --> Middleware
    
    state Middleware {
        [*] --> CheckHeader
        CheckHeader --> KhongCoToken : Báo lỗi 401
        CheckHeader --> GiaiMaJWT : Có Token
        GiaiMaJWT --> CheckBlacklist
    }
    
    Middleware --> TuChoi : Nằm trong Blacklist
    Middleware --> CheckRole : Hợp lệ
    
    CheckRole --> Pass : Role == Admin
    CheckRole --> CamTruyCap : Role != Admin (Báo lỗi 403)
    
    Pass --> XuLyLogic
    XuLyLogic --> [*]
```

---
## CHƯƠNG 4

### Hình 4.2: Luồng tương tác giữa Frontend, Backend và Hạ tầng
```mermaid
graph LR
    UI[Frontend React] -->|JSON/HTTP| API(FastAPI Gateway)
    API -->|DI| Service[Business Services]
    Service -->|Hit| Cache[(Redis)]
    Service -->|Miss| ORM[SQLAlchemy]
    ORM --> DB[(Postgres FTS)]
```

### Hình 4.3: Sơ đồ Package (Clean Architecture)
```mermaid
graph TD
    subgraph "Infrastructure Layer"
        FastAPIRouter[Routers / Endpoints]
        PostgresRepo[Database Repositories]
        RedisClient[Cache Client]
    end
    
    subgraph "Application Layer"
        AuthService[Auth Service]
        ProjectService[Project Service]
        SearchService[Search Service]
    end
    
    subgraph "Domain Layer"
        UserEntity[User Model]
        ProjectEntity[Project Model]
        CoreRules[Business Validation]
    end
    
    FastAPIRouter --> AuthService
    FastAPIRouter --> ProjectService
    PostgresRepo --> ProjectEntity
    AuthService --> UserEntity
    ProjectService --> ProjectEntity
```

### Hình 4.4: Sơ đồ Component Backend theo các module nghiệp vụ
```mermaid
graph TD
    Gateway((API Gateway)) --> Auth[Module Xác thực]
    Gateway --> Search[Module Tìm kiếm]
    Gateway --> Proj[Module Đề tài]
    Gateway --> Admin[Module Quản trị]
    
    Auth -.-> DB[(DB)]
    Proj -.-> DB
    Search -.-> DB
    Admin -.-> DB
```

### Hình 4.6: Sequence diagram cho luồng Refresh Token
```mermaid
sequenceDiagram
    participant User
    participant API
    participant DB
    
    Note over User: Access Token hết hạn
    User->>API: GET /protected (Mang Access Token cũ)
    API-->>User: 401 Token Expired
    
    User->>API: POST /refresh (Mang Refresh Token qua Cookie)
    API->>DB: Check Refresh Token hợp lệ?
    DB-->>API: OK
    API->>API: Generate New Access Token
    API-->>User: 200 OK (Cấp lại Token mới)
    User->>API: GET /protected (Mang Token mới)
    API-->>User: 200 Data
```

### Hình 4.7: Component diagram cho module Tìm kiếm khoa học
```mermaid
graph TD
    Input[Query Parameters] --> Normalizer[Text Normalizer]
    Normalizer --> Cache[Redis Cache Provider]
    Cache -->|Miss| FTS[Postgres FTS Engine]
    FTS --> Trigram[pg_trgm Extension]
    Trigram --> Ranker[TS_Rank Algorithm]
    Ranker --> Paginator[Pagination Manager]
    Paginator --> Output[JSON Response]
```

### Hình 4.9: Sơ đồ luồng lưu trữ tệp
```mermaid
graph LR
    Client((Client)) -->|Upload chunk| API[FastAPI Upload Handler]
    API --> Validator[Size & Format Check]
    Validator -->|Stream| LocalFS[Local File System]
    Validator -.->|Tương lai| S3[AWS S3 Storage]
    LocalFS --> DBRecord[Lưu file_path vào DB]
```

### Hình 4.10: Mô hình dữ liệu logic rút gọn
```mermaid
erDiagram
    NGUOI_DUNG ||--o{ DE_TAI : "Nộp"
    LINH_VUC ||--o{ DE_TAI : "Phân loại"
    DE_TAI ||--o{ LOG_TIM_KIEM : "Sinh ra"
```

### Hình 4.12: Sơ đồ phân nhóm API theo module
```mermaid
graph TD
    API[Root: /api/v1]
    API --> Auth[/auth]
    API --> Projects[/projects]
    API --> Search[/search]
    API --> Admin[/admin]
    
    Auth --> L1[POST /login]
    Auth --> L2[POST /logout]
    
    Projects --> P1[GET /]
    Projects --> P2[POST /]
    
    Search --> S1[GET /?q=]
```

### Hình 4.13: Sơ đồ bảo mật nhiều tầng
```mermaid
graph TD
    Internet((Internet)) --> WAF[Cloudflare / WAF]
    WAF --> Nginx[Nginx - Rate Limit & SSL]
    Nginx --> FastApiMW[FastAPI CORS & JWT Middleware]
    FastApiMW --> Service[Business Logic]
    Service --> DBFirewall[Internal Network Firewall]
    DBFirewall --> DB[(PostgreSQL)]
```

### Hình 4.14: Sơ đồ triển khai Local bằng Docker Compose
```mermaid
graph TD
    subgraph "Host OS (Windows/Linux)"
        subgraph "Docker Engine"
            Nginx[Container: Nginx Proxy]
            App[Container: FastAPI App]
            DB[Container: PostgreSQL 15]
            Redis[Container: Redis 7]
        end
        Nginx --- App
        App --- DB
        App --- Redis
    end
```

### Hình 4.15: Sơ đồ triển khai Production đề xuất
```mermaid
graph TD
    Internet((Internet)) --> ALB[AWS Application Load Balancer]
    ALB --> K8s[Kubernetes Cluster]
    
    subgraph "EKS Cluster"
        Ingress[Nginx Ingress]
        Pod1[FastAPI Pod 1]
        Pod2[FastAPI Pod 2]
        Pod3[FastAPI Pod N]
        Ingress --> Pod1 & Pod2 & Pod3
    end
    
    Pod1 & Pod2 & Pod3 --> RDS[(AWS RDS - Postgres)]
    Pod1 & Pod2 & Pod3 --> ElastiCache[(AWS ElastiCache - Redis)]
```

### Hình 4.16: Cấu trúc thư mục Code Backend
```mermaid
graph TD
    Root[vnu_repository_backend/]
    Root --> App[app/]
    App --> API[api/]
    App --> Core[core/]
    App --> DB[db/]
    App --> Models[models/]
    App --> Schemas[schemas/]
    App --> Services[services/]
    Root --> Docker[docker-compose.yml]
    Root --> Req[requirements.txt]
```
