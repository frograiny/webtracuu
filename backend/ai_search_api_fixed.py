# NẾU BỊ LỖI SQLITE QUÁ CŨ, HÃY BỎ COMMENT 3 DÒNG BÊN DƯỚI:
# import sys
# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from typing import Any
from fastapi import FastAPI, Query  # type: ignore
from contextlib import asynccontextmanager
import chromadb  # type: ignore
from sentence_transformers import SentenceTransformer  # type: ignore
import uvicorn  # type: ignore
import logging

# Cấu hình log để dễ theo dõi lỗi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Biến toàn cục để lưu Model và Collection
ai_model: Any = None
collection: Any = None

# Dữ liệu mẫu
mock_projects = [
    {
        "id": "NCKH-2023-001",
        "title": "Ứng dụng trí tuệ nhân tạo trong việc cá nhân hóa lộ trình học tập",
        "author": "Nguyễn Văn An",
        "abstract": "Nghiên cứu ứng dụng các thuật toán học máy để phân tích kết quả học tập của học sinh, từ đó tự động đề xuất bài tập và tài liệu phù hợp với năng lực từng cá nhân."
    },
    {
        "id": "NCKH-2023-002",
        "title": "Giải pháp nâng cao ý thức bảo vệ môi trường cho học sinh THPT",
        "author": "Trần Thị Bích",
        "abstract": "Thiết kế các chuỗi sự kiện, câu lạc bộ, đánh giá sự thay đổi trong nhận thức và hành động của học sinh về rác thải nhựa và biến đổi khí hậu."
    },
    {
        "id": "NCKH-2024-001",
        "title": "Chế tạo vật liệu sinh học thay thế nhựa dùng một lần từ vỏ trấu",
        "author": "Lê Hoàng Cường",
        "abstract": "Dự án nghiên cứu quy trình xử lý vỏ trấu phế phẩm nông nghiệp thành các sản phẩm như đĩa, ly, muỗng có khả năng phân hủy sinh học trong môi trường tự nhiên."
    }
]

# ==========================================
# 1. QUẢN LÝ VÒNG ĐỜI ỨNG DỤNG (FIX XUNG ĐỘT KHỞI ĐỘNG)
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    global ai_model, collection
    
    logger.info("Đang khởi tạo Hệ thống AI...")
    
    try:
        # Tải mô hình
        logger.info("Đang tải model ngôn ngữ (có thể mất 1-2 phút lần đầu)...")
        ai_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Khởi tạo Database
        logger.info("Khởi tạo Vector Database (ChromaDB)...")
        db_client = chromadb.PersistentClient(path="./nckh_db")
        collection = db_client.get_or_create_collection(name="vnu_projects")
        
        # Nạp dữ liệu nếu DB trống
        if collection.count() == 0:
            logger.info("DB trống. Đang mã hóa dữ liệu mẫu thành Vector...")
            ids, documents, metadatas = [], [], []

            for p in mock_projects:
                text_to_ai = f"Tên đề tài: {p['title']}. Nội dung: {p['abstract']}"
                ids.append(p["id"])
                documents.append(text_to_ai)
                metadatas.append(p)

            embeddings = ai_model.encode(documents).tolist()  # type: ignore
            collection.add(  # type: ignore
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            logger.info("Đã nạp thành công!")
        else:
            logger.info(f"Hệ thống sẵn sàng! Đã có {collection.count()} đề tài trong DB.")
            
    except Exception as e:
        logger.error(f"CÓ LỖI XẢY RA KHI KHỞI ĐỘNG AI: {str(e)}")
        
    yield # Bắt đầu chạy Server
    
    # Dọn dẹp khi tắt server
    logger.info("Đang tắt hệ thống AI...")

# ==========================================
# Khởi tạo App với lifespan
app = FastAPI(title="VNU AI Search API", lifespan=lifespan)

# ==========================================
# 2. API TÌM KIẾM
# ==========================================
@app.get("/api/ai-search")
def ai_search(q: str = Query(..., description="Nhập câu hỏi tự nhiên")):
    if not q or not collection or not ai_model:
        return {"data": [], "message": "Hệ thống chưa sẵn sàng hoặc thiếu từ khóa"}

    try:
        # Biến câu hỏi thành Vector
        query_vector = ai_model.encode([q]).tolist()  # type: ignore

        # Tìm kiếm 3 kết quả giống nhất
        results = collection.query(  # type: ignore
            query_embeddings=query_vector,
            n_results=3
        )

        response_data = []
        if results['metadatas'] and len(results['metadatas']) > 0:
            for i in range(len(results['metadatas'][0])):
                meta = results['metadatas'][0][i]
                distance = results['distances'][0][i] 
                
                response_data.append({
                    "id": meta["id"],
                    "tenDeTai": meta["title"],
                    "chuNhiem": meta["author"],
                    "tomTat": meta["abstract"],
                    "doChinhXac_AI": f"{round((1 - distance) * 100, 1)}%" # Chuyển thành % cho dễ nhìn
                })

        return {
            "query": q,
            "data": response_data
        }
    except Exception as e:
        return {"error": str(e)}
