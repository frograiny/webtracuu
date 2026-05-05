"""
API Tìm kiếm & Chi tiết Đề tài NCKH.

Thuật toán tìm kiếm hybrid:
  1. Exact match trên cột normalized (nhanh, dùng index)
  2. Token-level scoring: mỗi keyword được so khớp riêng → tính điểm tổng hợp
  3. Hỗ trợ cả có dấu lẫn không dấu, không cần PostgreSQL extension
"""

from uuid import uuid4

import re
from fastapi import APIRouter, Depends, HTTPException, Query, status, Request, BackgroundTasks  # type: ignore
from sqlalchemy import and_, case, func, literal, or_  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from prometheus_client import Counter, Histogram

from app.api.v1.auth import get_current_user, get_current_admin
from app.core.exceptions import ConflictError, NotFoundError, ForbiddenError
from app.core.rate_limit import limiter
from fastapi_cache.decorator import cache
from app.db.session import get_db  # type: ignore
from app.models.project import ResearchProject  # type: ignore
from app.models.user import User  # type: ignore
from app.schemas.project import (
    ProjectCreate,
    ProjectDetailResponse,
    ProjectItem,
    ProjectUpdate,
    SearchData,
    SearchResponse,
)
from app.utils.audience import STUDENT_AUDIENCE, normalize_target_audience
from app.utils.text import normalize_query

router = APIRouter()

# ────────────────────────────────────────────────────
# Business Metrics (Prometheus)
# ────────────────────────────────────────────────────
SEARCH_REQUESTS = Counter(
    "search_requests_total",
    "Total search requests",
    ["status"] # found, empty
)

SEARCH_RESULTS = Histogram(
    "search_results_count",
    "Number of search results returned",
    buckets=[0, 1, 5, 10, 20, 50, 100]
)

# ────────────────────────────────────────────────────
# Cache Strategy
# ────────────────────────────────────────────────────
def search_key_builder(func, namespace: str = "", request: Request = None, response=None, *args, **kwargs):
    # Tối ưu Cache Key bằng cách loại bỏ khoảng trắng thừa và viết thường
    q = kwargs.get("q", "").strip().lower()
    q = re.sub(r'\s+', ' ', q)
    offset = kwargs.get("offset", 0)
    limit = kwargs.get("limit", 20)
    # Các filter khác
    doc_type = kwargs.get("type", "Tất cả")
    field = kwargs.get("field", "Tất cả")
    target = kwargs.get("target", "Tất cả")
    year = kwargs.get("year", "Tất cả")
    return f"{namespace}:{func.__name__}:{q}:{doc_type}:{field}:{target}:{year}:{offset}:{limit}"

async def clear_search_cache():
    await FastAPICache.clear(namespace="search")

# ────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────


def _to_project_item(item: ResearchProject) -> dict:
    """Chuyển ORM object → dict theo format ProjectItem."""
    return {
        "id": item.id,
        "tenDeTai": item.title,
        "chuNhiem": item.author,
        "doiTuong": normalize_target_audience(item.target_audience),
        "linhVuc": item.field,
        "namThucHien": item.year,
        "trangThai": item.status,
        "tomTat": item.abstract,
        "tuKhoa": item.keywords or [],
        "loaiTaiLieu": item.document_type,
        "namTrienKhai": item.implementation_year,
    }


def _build_target_filter(target: str):
    normalized_target = normalize_target_audience(target)

    if normalized_target == STUDENT_AUDIENCE:
        return ResearchProject.target_audience.in_([STUDENT_AUDIENCE, "Học sinh"])

    return ResearchProject.target_audience.not_in([STUDENT_AUDIENCE, "Học sinh"])


def _apply_base_filters(query, *, doc_type: str, field: str, target: str, year: str):
    """Áp dụng các bộ lọc cơ bản (type, field, target, year)."""
    if doc_type != "Tất cả":
        query = query.filter(ResearchProject.document_type == doc_type)
    if field != "Tất cả":
        query = query.filter(ResearchProject.field == field)
    if target != "Tất cả":
        query = query.filter(_build_target_filter(target))
    if year != "Tất cả":
        query = query.filter(ResearchProject.year == int(year))
    return query


# ────────────────────────────────────────────────────
# Thuật toán tìm kiếm mới: True Production (FTS + pg_trgm)
# ────────────────────────────────────────────────────

SYNONYMS = {
    "ai": ["ai", "tri tue nhan tao", "artificial intelligence"],
    "cntt": ["cntt", "cong nghe thong tin", "it"],
    "y hoc": ["y hoc", "y te", "y khoa"],
}

def apply_synonyms(query: str) -> str:
    words = query.lower().split()
    expanded = []
    for w in words:
        if w in SYNONYMS:
            expanded.extend(SYNONYMS[w])
        else:
            expanded.append(w)
    return " ".join(set(expanded))


def _build_search_query(db: Session, q_normalized: str):
    """
    Xây dựng query tìm kiếm dựa trên PostgreSQL FTS và pg_trgm.

    Thuật toán:
    - Sử dụng TSVECTOR (search_vector) kết hợp với toán tử @@ để tìm kiếm Full Text.
    - Dùng hàm ts_rank để lấy điểm BM25/TF-IDF chuẩn xác.
    - Dùng pg_trgm similarity cho Fuzzy matching (sai chính tả, đảo từ).
    """
    expanded_query = apply_synonyms(q_normalized)
    keywords = expanded_query.split()
    if not keywords:
        return None

    # Thay khoảng trắng bằng & để tạo TSQUERY (AND logic cho FTS)
    tsquery_string = " & ".join(keywords)
    search_query = func.to_tsquery('simple', func.unaccent(tsquery_string))

    # Điều kiện FTS
    fts_condition = ResearchProject.search_vector.op('@@')(search_query)

    # Điểm FTS (ts_rank)
    ts_rank_score = func.ts_rank(ResearchProject.search_vector, search_query)

    # Điểm Similarity (pg_trgm) trên Title và Author
    # Giúp tìm những từ sai chính tả hoặc gõ sát nghĩa
    title_sim = func.similarity(func.unaccent(ResearchProject.title), func.unaccent(q_normalized))
    author_sim = func.similarity(func.unaccent(ResearchProject.author), func.unaccent(q_normalized))
    max_sim = func.greatest(title_sim, author_sim)

    # Tổng điểm: ưu tiên FTS rank (trọng số cao) + Similarity
    total_score = ts_rank_score * 2.0 + max_sim

    # Filter: thỏa mãn FTS hoặc similarity > 0.2 (để pass lỗi chính tả nhỏ)
    combined_filter = or_(fts_condition, max_sim > 0.2)

    query = (
        db.query(ResearchProject, total_score.label("relevance_score"))
        .filter(combined_filter)
        .order_by(total_score.desc(), ResearchProject.year.desc())
    )

    return query


# ────────────────────────────────────────────────────
# Endpoints
# ────────────────────────────────────────────────────


@router.get("/search", response_model=SearchResponse)
@limiter.limit("30/minute")
@cache(expire=300, namespace="search", key_builder=search_key_builder)
def search_projects(
    request: Request,
    q: str = Query("", max_length=200, description="Từ khóa tìm kiếm"),
    type: str = Query("Tất cả", description="Lọc theo loại tài liệu"),
    field: str = Query("Tất cả", description="Lọc theo lĩnh vực"),
    target: str = Query("Tất cả", description="Lọc theo đối tượng"),
    year: str = Query("Tất cả", description="Lọc theo năm"),
    limit: int = Query(20, ge=1, le=100, description="Số lượng kết quả trả về"),
    offset: int = Query(0, ge=0, description="Bỏ qua bao nhiêu kết quả"),
    db: Session = Depends(get_db),
):
    """
    Tìm kiếm đề tài NCKH.

    - Hỗ trợ tiếng Việt có dấu và không dấu
    - Kết quả xếp hạng theo độ liên quan (relevance score)
    - Hỗ trợ phân trang (limit/offset)
    """
    if q:
        q_normalized = normalize_query(q)
        search_query = _build_search_query(db, q_normalized)

        if search_query is None:
            SEARCH_REQUESTS.labels(status="empty").inc()
            SEARCH_RESULTS.observe(0)
            return SearchResponse(data=SearchData(total=0, items=[]))

        # Áp dụng base filters lên query (filter trên entity, không phải tuple)
        if type != "Tất cả":
            search_query = search_query.filter(ResearchProject.document_type == type)
        if field != "Tất cả":
            search_query = search_query.filter(ResearchProject.field == field)
        if target != "Tất cả":
            search_query = search_query.filter(_build_target_filter(target))
        if year != "Tất cả":
            search_query = search_query.filter(ResearchProject.year == int(year))

        total_count = search_query.count()
        rows = search_query.offset(offset).limit(limit).all()

        # rows là list of (ResearchProject, score) tuples
        items = [_to_project_item(row[0]) for row in rows]
        
        # Ghi nhận Business Metrics
        SEARCH_REQUESTS.labels(status="found" if total_count > 0 else "empty").inc()
        SEARCH_RESULTS.observe(total_count)
        
        return SearchResponse(data=SearchData(total=total_count, items=items))

    # Không có query → trả về tất cả (có filter)
    query = db.query(ResearchProject)
    query = _apply_base_filters(query, doc_type=type, field=field, target=target, year=year)
    query = query.order_by(ResearchProject.year.desc())

    total_count = query.count()
    results = query.offset(offset).limit(limit).all()
    items = [_to_project_item(item) for item in results]

    return SearchResponse(data=SearchData(total=total_count, items=items))


@router.post("", response_model=ProjectDetailResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Tạo mới một đề tài NCKH.
    
    Chỉ admin mới có quyền tạo.
    """
    # Check duplicate title
    existing = (
        db.query(ResearchProject)
        .filter(ResearchProject.title.ilike(f"%{payload.tenDeTai}%"))
        .first()
    )
    if existing:
        raise ConflictError("Tiêu đề đề tài đã tồn tại")
    
    # Create new project
    project = ResearchProject(
        id=str(uuid4()),
        title=payload.tenDeTai,
        author=payload.chuNhiem,
        target_audience=payload.doiTuong,
        field=payload.linhVuc,
        year=payload.namThucHien,
        status=payload.trangThai,
        abstract=payload.tomTat,
        keywords=payload.tuKhoa,
        document_type=payload.loaiTaiLieu,
        implementation_year=payload.namTrienKhai,
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Invalidate Cache
    background_tasks.add_task(clear_search_cache)
    
    return ProjectDetailResponse(data=_to_project_item(project))


@router.put("/{project_id}", response_model=ProjectDetailResponse)
def update_project(
    project_id: str,
    payload: ProjectUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Cập nhật một đề tài NCKH.
    
    Chỉ admin mới có quyền cập nhật.
    """
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if not project:
        raise NotFoundError("Không tìm thấy đề tài")
    
    # Check duplicate title if updating title
    if payload.tenDeTai and payload.tenDeTai != project.title:
        existing = (
            db.query(ResearchProject)
            .filter(
                ResearchProject.title.ilike(f"%{payload.tenDeTai}%"),
                ResearchProject.id != project_id,
            )
            .first()
        )
        if existing:
            raise ConflictError("Tiêu đề đề tài đã tồn tại")
    
    # Update fields
    if payload.tenDeTai:
        project.title = payload.tenDeTai
    if payload.chuNhiem:
        project.author = payload.chuNhiem
    if payload.doiTuong:
        project.target_audience = payload.doiTuong
    if payload.linhVuc:
        project.field = payload.linhVuc
    if payload.namThucHien:
        project.year = payload.namThucHien
    if payload.trangThai:
        project.status = payload.trangThai
    if payload.tomTat is not None:
        project.abstract = payload.tomTat
    if payload.tuKhoa is not None:
        project.keywords = payload.tuKhoa
    if payload.loaiTaiLieu is not None:
        project.document_type = payload.loaiTaiLieu
    if payload.namTrienKhai is not None:
        project.implementation_year = payload.namTrienKhai
    
    db.commit()
    db.refresh(project)
    
    # Invalidate Cache
    background_tasks.add_task(clear_search_cache)
    
    return ProjectDetailResponse(data=_to_project_item(project))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Xóa một đề tài NCKH.
    
    Chỉ admin mới có quyền xóa.
    """
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if not project:
        raise NotFoundError("Không tìm thấy đề tài")
    
    db.delete(project)
    db.commit()
    
    # Invalidate Cache
    background_tasks.add_task(clear_search_cache)
    
    return None
