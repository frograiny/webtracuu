"""
API Tìm kiếm & Chi tiết Đề tài NCKH.

Thuật toán tìm kiếm hybrid:
  1. Exact match trên cột normalized (nhanh, dùng index)
  2. Token-level scoring: mỗi keyword được so khớp riêng → tính điểm tổng hợp
  3. Hỗ trợ cả có dấu lẫn không dấu, không cần PostgreSQL extension
"""

from fastapi import APIRouter, Depends, HTTPException, Query  # type: ignore
from sqlalchemy import and_, case, func, literal, or_  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.db.session import get_db  # type: ignore
from app.models.project import ResearchProject  # type: ignore
from app.schemas.project import (
    ProjectDetailResponse,
    ProjectItem,
    SearchData,
    SearchResponse,
)
from app.utils.audience import STUDENT_AUDIENCE, normalize_target_audience
from app.utils.text import normalize_query

router = APIRouter()

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
# Thuật toán tìm kiếm mới: Single-pass Token Scoring
# ────────────────────────────────────────────────────


def _build_search_query(db: Session, q_normalized: str):
    """
    Xây dựng query tìm kiếm dựa trên token scoring.

    Thuật toán:
    - Tách query thành các keyword (tokens)
    - Mỗi token được tìm bằng LIKE trên cột đã normalized (có index)
    - Tính điểm: title match = 3 điểm, author match = 1 điểm
    - Exact match (title chứa toàn bộ query) = bonus 5 điểm
    - Sắp xếp theo tổng điểm giảm dần

    So với thuật toán cũ:
    - Chỉ 1 query (thay vì 2: FTS + fallback)
    - Luôn dùng cột normalized → không cần runtime translate()
    - Điểm số chính xác hơn ts_rank cho tiếng Việt
    """
    keywords = q_normalized.split()
    if not keywords:
        return None

    # Xây dựng điều kiện match: ít nhất 1 keyword match title HOẶC author
    match_conditions = []
    score_components = []

    for kw in keywords:
        pattern = f"%{kw}%"
        title_match = ResearchProject.title_normalized.like(pattern)
        author_match = ResearchProject.author_normalized.like(pattern)

        match_conditions.append(or_(title_match, author_match))

        # Tính điểm cho mỗi keyword: title = 3đ, author = 1đ
        score_components.append(
            case((title_match, 3), else_=0) + case((author_match, 1), else_=0)
        )

    # Bonus: exact phrase match trên title = +5đ
    exact_phrase_bonus = case(
        (ResearchProject.title_normalized.like(f"%{q_normalized}%"), 5),
        else_=0,
    )

    # Tổng điểm
    total_score = exact_phrase_bonus
    for sc in score_components:
        total_score = total_score + sc

    # Filter: tất cả keywords phải match ít nhất 1 cột (AND logic)
    combined_filter = and_(*match_conditions)

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
def search_projects(
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
        return SearchResponse(data=SearchData(total=total_count, items=items))

    # Không có query → trả về tất cả (có filter)
    query = db.query(ResearchProject)
    query = _apply_base_filters(query, doc_type=type, field=field, target=target, year=year)
    query = query.order_by(ResearchProject.year.desc())

    total_count = query.count()
    results = query.offset(offset).limit(limit).all()
    items = [_to_project_item(item) for item in results]

    return SearchResponse(data=SearchData(total=total_count, items=items))


@router.get("/{project_id}", response_model=ProjectDetailResponse)
def get_project_detail(project_id: str, db: Session = Depends(get_db)):
    """Lấy chi tiết 1 đề tài NCKH theo ID."""
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy đề tài")
    return ProjectDetailResponse(data=_to_project_item(project))
