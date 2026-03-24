from fastapi import APIRouter, Depends, Query # type: ignore
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import func, or_ # type: ignore

from app.db.session import get_db # type: ignore
from app.models.project import ResearchProject # type: ignore

router = APIRouter()

@router.get("/search")
def search_projects(
    q: str = Query("", description="Từ khóa tìm kiếm (tên đề tài, tác giả...)"),
    type: str = Query("Tất cả", description="Lọc theo loại tài liệu"),
    field: str = Query("Tất cả", description="Lọc theo lĩnh vực"),
    target: str = Query("Tất cả", description="Lọc theo đối tượng (GV/HS)"),
    year: str = Query("Tất cả", description="Lọc theo năm"),
    limit: int = Query(20, ge=1, le=100, description="Số lượng kết quả trả về"),
    offset: int = Query(0, ge=0, description="Bỏ qua bao nhiêu kết quả (phân trang)"),
    db: Session = Depends(get_db)
):
    query = db.query(ResearchProject)

    if q:
        # Cải tiến lần 3: Sử dụng Full-Text Search (FTS) nội tại của PostgreSQL
        # Dùng plainto_tsquery để hỗ trợ gõ nhiều từ khóa mà không cần pg_trgm
        search_filter = or_(
            func.to_tsvector('simple', ResearchProject.title).op('@@')(func.plainto_tsquery('simple', q)),
            func.to_tsvector('simple', ResearchProject.author).op('@@')(func.plainto_tsquery('simple', q))
        )
        query = query.filter(search_filter)
        
        # Bổ sung thuật toán tính Rank để sắp xếp kết quả chuẩn xác (Từ khóa khớp nhiều sẽ lên đầu)
        rank_score = func.ts_rank(
            func.to_tsvector('simple', ResearchProject.title), 
            func.plainto_tsquery('simple', q)
        )
        query = query.order_by(rank_score.desc(), ResearchProject.year.desc())
    else:
        query = query.order_by(ResearchProject.year.desc())

    if type != "Tất cả":
        query = query.filter(ResearchProject.document_type == type)
    if field != "Tất cả":
        query = query.filter(ResearchProject.field == field)
    if target != "Tất cả":
        query = query.filter(ResearchProject.target_audience == target)
    if year != "Tất cả":
        query = query.filter(ResearchProject.year == int(year))

    total_count = query.count()
    results = query.offset(offset).limit(limit).all()

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
                    "tuKhoa": item.keywords or [],
                    "loaiTaiLieu": item.document_type,
                    "namTrienKhai": item.implementation_year
                } for item in results
            ]
        }
    }

@router.get("/{project_id}")
def get_project_detail(project_id: str, db: Session = Depends(get_db)):
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
