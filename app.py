from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, func, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import uvicorn
import chromadb
from sentence_transformers import SentenceTransformer
import os

# ==========================================
# 1. CẤU HÌNH DATABASE (POSTGRESQL)
# ==========================================
# HƯỚNG DẪN SETUP:
# 1. Cài PostgreSQL: https://www.postgresql.org/download/
# 2. Tạo database: createdb vnu_research_db
# 3. Cài dependencies: pip install fastapi uvicorn sqlalchemy psycopg2-binary
# 4. Chạy migration: python app.py (để tạo tables)
# 5. Seed dữ liệu mẫu (xem cuối file)
# 6. Chạy server: uvicorn app:app --reload --port 8000

# Thay đổi chuỗi kết nối này bằng thông tin DB thực tế của VNU
DATABASE_URL = "postgresql://user:password@localhost:5432/vnu_research_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================
# 2. ĐỊNH NGHĨA BẢNG (MODEL)
# ==========================================
class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    target_audience = Column(String) # Giáo viên, Học sinh
    field = Column(String)           # Lĩnh vực
    year = Column(Integer)
    status = Column(String)
    abstract = Column(Text)
    keywords = Column(JSON, default=[])  # Từ khóa/Tags

    """
    LƯU Ý QUAN TRỌNG TRÊN DATABASE (Chạy script SQL này trực tiếp trên PostgreSQL):
    
    CREATE EXTENSION IF NOT EXISTS pg_trgm;
    
    -- Tạo GIN Index để tăng tốc độ tìm kiếm cực đại cho Tên đề tài và Tóm tắt
    CREATE INDEX idx_project_title_trgm ON research_projects USING GIN (title gin_trgm_ops);
    CREATE INDEX idx_project_abstract_trgm ON research_projects USING GIN (abstract gin_trgm_ops);
    """

# ==========================================
# 3. KHỞI TẠO FASTAPI
# ==========================================
app = FastAPI(
    title="VNU Research API",
    description="API tìm kiếm NCKH cực nhanh sử dụng PostgreSQL Trigram",
    version="1.0.0"
)

# CORS configuration cho phép Frontend gọi API từ bất kỳ domain nào
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origins (Production: chỉ định domain cụ thể)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 4. KHỞI TẠO AI MODEL VÀ CHROMADB (SEMANTIC SEARCH)
# ==========================================
print("[Loading] Dang tai mo hinh AI hieu Tieng Viet (Lan dau se mat chut thoi gian de tai)...")
# Sử dụng mô hình đa ngôn ngữ (hỗ trợ Tiếng Việt rất tốt), dung lượng nhẹ (~400MB)
ai_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
print("[OK] AI Model da san sang!")

# Khởi tạo ChromaDB - Lưu trữ trực tiếp vào thư mục './nckh_db' (Không cần cài đặt Server)
db_client = chromadb.PersistentClient(path="./nckh_db")
ai_collection = db_client.get_or_create_collection(name="vnu_research_projects")
print("[OK] ChromaDB da san sang!")

# Dependency để lấy DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 5. HÀM SYNC DỮ LIỆU VÀO AI DATABASE
# ==========================================
def sync_projects_to_ai():
    """Lưu tất cả projects từ PostgreSQL vào ChromaDB để tìm kiếm AI"""
    db = SessionLocal()
    try:
        if ai_collection.count() == 0:
            print("Đang mã hóa (embedding) dữ liệu đề tài thành các Vector AI...")
            
            projects = db.query(ResearchProject).all()
            
            if not projects:
                print("[WARNING] Khong co du lieu trong PostgreSQL. Vui long seed du lieu truoc.")
                return

            ids = []
            documents = []
            metadatas = []

            for p in projects:
                # Gộp Tên đề tài, Tóm tắt và Từ khóa để AI hiểu toàn bộ ngữ cảnh
                keywords_text = " ".join(p.keywords) if p.keywords else ""
                text_to_ai = f"Tên đề tài: {p.title}. Lĩnh vực: {p.field}. Nội dung: {p.abstract}. Từ khóa: {keywords_text}"
                
                ids.append(p.id)
                documents.append(text_to_ai)
                metadatas.append({
                    "id": p.id,
                    "title": p.title,
                    "author": p.author,
                    "abstract": p.abstract,
                    "field": p.field,
                    "target_audience": p.target_audience,
                    "year": p.year,
                    "status": p.status,
                    "keywords": p.keywords or []
                })

            # Dùng AI Model biến văn bản thành Vector số học
            embeddings = ai_model.encode(documents).tolist()

            # Lưu tất cả vào ChromaDB
            ai_collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            print(f"[OK] Da ma hoa {len(projects)} de tai vao AI Database!")
        else:
            print(f"[OK] AI Database da co {ai_collection.count()} de tai, san sang tim kiem.")
    finally:
        db.close()

# Sync dữ liệu khi khởi động
sync_projects_to_ai()

# ==========================================
# 6. API SEARCH (POSTGRESQL - KEYWORD SEARCH)
# ==========================================
@app.get("/api/v1/projects/search")
def search_projects(
    q: str = Query("", description="Từ khóa tìm kiếm (tên đề tài, tác giả...)"),
    field: str = Query("Tất cả", description="Lọc theo lĩnh vực"),
    target: str = Query("Tất cả", description="Lọc theo đối tượng (GV/HS)"),
    year: str = Query("Tất cả", description="Lọc theo năm"),
    limit: int = Query(20, ge=1, le=100, description="Số lượng kết quả trả về"),
    offset: int = Query(0, ge=0, description="Bỏ qua bao nhiêu kết quả (phân trang)"),
    db: Session = Depends(get_db)
):
    # Bắt đầu xây dựng câu truy vấn
    query = db.query(ResearchProject)

    # 1. LỌC THEO TỪ KHÓA (Sử dụng pg_trgm similarity cho độ chính xác & tốc độ)
    if q:
        # Sử dụng operator % của pg_trgm để kiểm tra sự tương đồng (Fuzzy search)
        # Thay vì LIKE, chúng ta dùng filter(title.op('%')(q)) hoặc func.similarity
        # Ở đây dùng func.similarity để vừa lọc vừa lấy điểm số (score) sắp xếp
        similarity_threshold = 0.2 # Ngưỡng độ chính xác (0.0 -> 1.0)
        
        # Tìm kiếm trên cả Tiêu đề và Tóm tắt
        search_filter = (
            (func.similarity(ResearchProject.title, q) > similarity_threshold) |
            (func.similarity(ResearchProject.author, q) > similarity_threshold)
        )
        query = query.filter(search_filter)
        
        # Sắp xếp kết quả: Tên đề tài hoặc tác giả nào giống từ khóa nhất sẽ lên đầu
        query = query.order_by(
            func.greatest(
                func.similarity(ResearchProject.title, q),
                func.similarity(ResearchProject.author, q)
            ).desc()
        )
    else:
        # Nếu không có từ khóa, sắp xếp theo năm mới nhất
        query = query.order_by(ResearchProject.year.desc())

    # 2. LỌC THEO CÁC TIÊU CHÍ KHÁC (Chính xác tuyệt đối)
    if field != "Tất cả":
        query = query.filter(ResearchProject.field == field)
    
    if target != "Tất cả":
        query = query.filter(ResearchProject.target_audience == target)
        
    if year != "Tất cả":
        query = query.filter(ResearchProject.year == int(year))

    # 3. PHÂN TRANG VÀ THỰC THI (Limit / Offset)
    total_count = query.count() # Tổng số kết quả
    results = query.offset(offset).limit(limit).all()

    # Định dạng kết quả trả về cho Frontend React
    return {
        "status": "success",
        "data": {
            "total": total_count,
            "items": [
                {
                    "id": item.id,
                    "tenDeTai": item.title,
                    "chuNhiem": item.author,
                    "doiTuong": item.target_audience,
                    "linhVuc": item.field,
                    "namThucHien": item.year,
                    "trangThai": item.status,
                    "tomTat": item.abstract,
                    "tuKhoa": item.keywords or []
                } for item in results
            ]
        }
    }

# Lệnh để chạy server: 
# uvicorn app:app --reload --port 8000

# ==========================================
# 5. ENDPOINT LẤY FILTER OPTIONS
# ==========================================
@app.get("/api/v1/filters")
def get_filters(db: Session = Depends(get_db)):
    """
    Lấy danh sách các tùy chọn bộ lọc (Lĩnh vực, Năm, Đối tượng)
    Sử dụng để populate dropdown trên Frontend
    """
    # Lấy danh sách các lĩnh vực khác nhau
    fields = db.query(ResearchProject.field).distinct().order_by(ResearchProject.field).all()
    field_list = ["Tất cả"] + [f[0] for f in fields if f[0]]

    # Lấy danh sách các năm khác nhau
    years = db.query(ResearchProject.year).distinct().order_by(ResearchProject.year.desc()).all()
    year_list = ["Tất cả"] + [str(y[0]) for y in years if y[0]]

    # Lấy danh sách các đối tượng khác nhau
    audiences = db.query(ResearchProject.target_audience).distinct().order_by(ResearchProject.target_audience).all()
    audience_list = ["Tất cả"] + [a[0] for a in audiences if a[0]]

    return {
        "status": "success",
        "data": {
            "fields": field_list,
            "years": year_list,
            "audiences": audience_list
        }
    }

# ==========================================
# 6. ENDPOINT LẤY CHI TIẾT MỘT ĐỀ TÀI
# ==========================================
@app.get("/api/v1/projects/{project_id}")
def get_project_detail(project_id: str, db: Session = Depends(get_db)):
    """Lấy chi tiết đầy đủ của một đề tài"""
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    
    if not project:
        return {
            "status": "error",
            "message": f"Không tìm thấy đề tài với ID: {project_id}"
        }
    
    return {
        "status": "success",
        "data": {
            "id": project.id,
            "tenDeTai": project.title,
            "chuNhiem": project.author,
            "doiTuong": project.target_audience,
            "linhVuc": project.field,
            "namThucHien": project.year,
            "trangThai": project.status,
            "tomTat": project.abstract,
            "tuKhoa": project.keywords or []
        }
    }

# ==========================================
# 7. API TÌM KIẾM NGỮ NGHĨA (AI SEMANTIC SEARCH)
# ==========================================
@app.get("/api/v1/ai-search")
def ai_search(q: str = Query(..., description="Nhập câu hỏi tự nhiên. VD: 'có đề tài nào về AI và giáo dục không?'")):
    """
    Tìm kiếm bằng AI Semantic Search - Hiểu ý nghĩa thay vì chỉ match từ khóa
    Ví dụ:
    - Input: "cái gì về viết bài để ai có thể học" 
    - Kết quả: Trả về đề tài "Ứng dụng AI cá nhân hóa lộ trình học tập"
    """
    if not q or q.strip() == "":
        return {
            "query": q,
            "message": "Vui lòng nhập câu hỏi",
            "data": []
        }

    try:
        # Bước 1: Biến câu hỏi của người dùng thành Vector
        query_vector = ai_model.encode([q]).tolist()

        # Bước 2: Tìm kiếm trong ChromaDB những Vector gần giống nhất
        # N_results=5 nghĩa là trả về 5 kết quả phù hợp nhất
        results = ai_collection.query(
            query_embeddings=query_vector,
            n_results=5
        )

        # Bước 3: Định dạng lại kết quả trả về cho Frontend React
        response_data = []
        
        # ChromaDB trả về list of lists, ta duyệt qua kết quả đầu tiên
        if results['metadatas'] and len(results['metadatas']) > 0:
            for i in range(len(results['metadatas'][0])):
                meta = results['metadatas'][0][i]
                # Khoảng cách (distance) càng nhỏ -> Càng giống từ khóa
                distance = results['distances'][0][i] 
                
                response_data.append({
                    "id": meta["id"],
                    "tenDeTai": meta["title"],
                    "chuNhiem": meta["author"],
                    "doiTuong": meta["target_audience"],
                    "linhVuc": meta["field"],
                    "namThucHien": meta["year"],
                    "trangThai": meta["status"],
                    "tomTat": meta["abstract"],
                    "tuKhoa": meta["keywords"],
                    "ai_relevance_score": round((1 - distance) * 100, 2)  # Điểm độ chính xác AI (0-100%)
                })

        return {
            "status": "success",
            "query": q,
            "message": "Kết quả được tìm kiếm bằng AI Semantic Search (hiểu ý nghĩa)",
            "data": response_data
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi AI Search: {str(e)}"
        }

# ==========================================
# 8. ENDPOINT ĐỒNG BỘ DỮ LIỆU (VÀO AI DATABASE)
# ==========================================
@app.post("/api/v1/sync-ai-db")
def sync_ai_db():
    """
    Đồng bộ lại dữ liệu từ PostgreSQL sang ChromaDB
    Dùng khi bạn thêm/sửa đề tài trong Database
    """
    try:
        # Xóa tất cả dữ liệu cũ từ ChromaDB
        all_ids = ai_collection.get(include=[], limit=10000)["ids"]
        if all_ids:
            ai_collection.delete(ids=all_ids)
        
        # Sync lại toàn bộ dữ liệu
        sync_projects_to_ai()
        
        return {
            "status": "success",
            "message": "[OK] Da dong bo lai AI Database"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi khi đồng bộ: {str(e)}"
        }

# ==========================================
# 9. HEALTH CHECK & INFO
# ==========================================
@app.get("/health")
def health_check():
    """Kiểm tra trạng thái API"""
    return {
        "status": "ok",
        "message": "VNU Research API is running",
        "ai_db_count": ai_collection.count(),
        "features": ["PostgreSQL Search", "AI Semantic Search", "Filters", "Project Details"]
    }

# ==========================================
# 10. SEED DỮ LIỆU MẪU (Dùng cho development)
# ==========================================
@app.post("/api/v1/seed-data")
def seed_data(db: Session = Depends(get_db)):
    """
    Endpoint để populate dữ liệu mẫu vào database
    POST http://localhost:8000/api/v1/seed-data
    """
    # Xóa dữ liệu cũ
    db.query(ResearchProject).delete()

    sample_data = [
        ResearchProject(
            id="NCKH-2023-001",
            title="Ứng dụng trí tuệ nhân tạo trong việc cá nhân hóa lộ trình học tập",
            author="Nguyễn Văn An",
            target_audience="Giáo viên",
            field="Công nghệ thông tin",
            year=2023,
            status="Đã nghiệm thu",
            abstract="Nghiên cứu ứng dụng các thuật toán học máy để phân tích kết quả học tập của học sinh, từ đó tự động đề xuất bài tập và tài liệu phù hợp với năng lực từng cá nhân.",
            keywords=["AI", "Giáo dục", "Cá nhân hóa"]
        ),
        ResearchProject(
            id="NCKH-2023-002",
            title="Giải pháp nâng cao ý thức bảo vệ môi trường cho học sinh THPT qua các hoạt động ngoại khóa",
            author="Trần Thị Bích",
            target_audience="Giáo viên",
            field="Khoa học xã hội",
            year=2023,
            status="Đã nghiệm thu",
            abstract="Đề tài tập trung vào việc thiết kế và tổ chức các chuỗi sự kiện, câu lạc bộ bảo vệ môi trường.",
            keywords=["Môi trường", "Ngoại khóa", "Ý thức"]
        ),
        ResearchProject(
            id="NCKH-2024-001",
            title="Chế tạo vật liệu sinh học thay thế nhựa dùng một lần từ vỏ trấu",
            author="Lê Hoàng Cường",
            target_audience="Học sinh",
            field="Hóa học & Vật liệu",
            year=2024,
            status="Đang thực hiện",
            abstract="Dự án nghiên cứu quy trình xử lý vỏ trấu phế phẩm nông nghiệp thành các sản phẩm.",
            keywords=["Vật liệu sinh học", "Vỏ trấu", "Bảo vệ môi trường"]
        ),
        ResearchProject(
            id="NCKH-2022-005",
            title="Thiết kế hệ thống tưới tiêu tự động sử dụng năng lượng mặt trời cho vườn trường",
            author="Phạm Minh Đức",
            target_audience="Học sinh",
            field="Kỹ thuật cơ điện",
            year=2022,
            status="Đã nghiệm thu",
            abstract="Hệ thống sử dụng cảm biến độ ẩm đất và ánh sáng để điều khiển máy bơm nước tự động.",
            keywords=["IoT", "Năng lượng mặt trời", "Tự động hóa"]
        ),
    ]

    db.add_all(sample_data)
    db.commit()

    # Đồng bộ dữ liệu vào AI Database
    sync_projects_to_ai()

    return {
        "status": "success",
        "message": f"[OK] Da seed {len(sample_data)} ban ghi du lieu mau",
        "note": "Dữ liệu đã được đồng bộ vào AI Database"
    }

# ==========================================
# 11. TẠOBẢNG DATABASE TỰ ĐỘNG
# ==========================================
# Tự động tạo tất cả tables khi khởi động
Base.metadata.create_all(bind=engine)

# ==========================================
# HƯỚNG DẪN VÀ CÀI ĐẶT
# ==========================================
# 📦 CÀI ĐẶT DEPENDENCIES:
# pip install fastapi uvicorn sqlalchemy psycopg2-binary chromadb sentence-transformers
#
# 🚀 CHẠY SERVER:
# uvicorn app:app --reload --port 8000
#
# 📝 SEED DỮ LIỆU MẪU:
# curl -X POST http://localhost:8000/api/v1/seed-data
#
# 🔎 ENDPOINTS CHÍNH:
# 1. /api/v1/projects/search - Tìm kiếm từ khóa (PostgreSQL Trigram)
# 2. /api/v1/ai-search - Tìm kiếm bằng AI (Semantic Search)
# 3. /api/v1/filters - Lấy danh sách filter options
# 4. /api/v1/projects/{id} - Lấy chi tiết một đề tài
# 5. /api/v1/sync-ai-db - Đồng bộ lại AI Database
# 6. /health - Kiểm tra trạng thái API
#
# 🌐 CÀI ĐẶT POSTGRESQL:
# 1. Tải PostgreSQL: https://www.postgresql.org/download/
# 2. Tạo database: createdb vnu_research_db  
# 3. Chỉnh DATABASE_URL nếu cần (dòng ~18)