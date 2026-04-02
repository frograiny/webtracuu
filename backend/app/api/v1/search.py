import unicodedata

from fastapi import APIRouter, Depends, Query  # type: ignore
from sqlalchemy import and_, func, or_  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.db.session import get_db  # type: ignore
from app.models.project import ResearchProject  # type: ignore
from app.utils.audience import STUDENT_AUDIENCE, normalize_target_audience

router = APIRouter()

_VN_ACCENTED = "àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ"
_VN_UNACCENTED = "aaaaaaaaaaaaaaaaadeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyAAAAAAAAAAAAAAAAADEEEEEEEEEEEIIIIIOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYY"


def remove_vietnamese_diacritics(text_input: str) -> str:
    text_input = text_input.replace("đ", "d").replace("Đ", "D")
    nfkd_form = unicodedata.normalize("NFD", text_input)
    return "".join(c for c in nfkd_form if unicodedata.category(c) != "Mn")


def _sql_unaccent(column):
    return func.translate(func.lower(column), _VN_ACCENTED, _VN_UNACCENTED)


def _build_result_items(results):
    return [
        {
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
        for item in results
    ]


def _build_target_filter(target: str):
    normalized_target = normalize_target_audience(target)

    if normalized_target == STUDENT_AUDIENCE:
        return ResearchProject.target_audience.in_([STUDENT_AUDIENCE, "Học sinh"])

    return ResearchProject.target_audience.not_in([STUDENT_AUDIENCE, "Học sinh"])


@router.get("/search")
def search_projects(
    q: str = Query("", description="Từ khóa tìm kiếm"),
    type: str = Query("Tất cả", description="Lọc theo loại tài liệu"),
    field: str = Query("Tất cả", description="Lọc theo lĩnh vực"),
    target: str = Query("Tất cả", description="Lọc theo đối tượng"),
    year: str = Query("Tất cả", description="Lọc theo năm"),
    limit: int = Query(20, ge=1, le=100, description="Số lượng kết quả trả về"),
    offset: int = Query(0, ge=0, description="Bỏ qua bao nhiêu kết quả"),
    db: Session = Depends(get_db),
):
    base_filters = []
    if type != "Tất cả":
        base_filters.append(ResearchProject.document_type == type)
    if field != "Tất cả":
        base_filters.append(ResearchProject.field == field)
    if target != "Tất cả":
        base_filters.append(_build_target_filter(target))
    if year != "Tất cả":
        base_filters.append(ResearchProject.year == int(year))

    if q:
        fts_filter = or_(
            func.to_tsvector("simple", ResearchProject.title).op("@@")(func.plainto_tsquery("simple", q)),
            func.to_tsvector("simple", ResearchProject.author).op("@@")(func.plainto_tsquery("simple", q)),
        )
        query = db.query(ResearchProject).filter(fts_filter)
        for current_filter in base_filters:
            query = query.filter(current_filter)

        rank_score = func.ts_rank(
            func.to_tsvector("simple", ResearchProject.title),
            func.plainto_tsquery("simple", q),
        )
        query = query.order_by(rank_score.desc(), ResearchProject.year.desc())

        total_count = query.count()
        if total_count > 0:
            results = query.offset(offset).limit(limit).all()
            return {"status": "success", "data": {"total": total_count, "items": _build_result_items(results)}}

        q_normalized = remove_vietnamese_diacritics(q).lower()
        keywords = q_normalized.split()

        if keywords:
            ilike_conditions = []
            for keyword in keywords:
                pattern = f"%{keyword}%"
                ilike_conditions.append(
                    or_(
                        _sql_unaccent(ResearchProject.title).ilike(pattern),
                        _sql_unaccent(ResearchProject.author).ilike(pattern),
                    )
                )

            fallback_filter = and_(*ilike_conditions)
            query_fb = db.query(ResearchProject).filter(fallback_filter)
            for current_filter in base_filters:
                query_fb = query_fb.filter(current_filter)
            query_fb = query_fb.order_by(ResearchProject.year.desc())

            total_count = query_fb.count()
            results = query_fb.offset(offset).limit(limit).all()
            return {"status": "success", "data": {"total": total_count, "items": _build_result_items(results)}}

        return {"status": "success", "data": {"total": 0, "items": []}}

    query = db.query(ResearchProject)
    for current_filter in base_filters:
        query = query.filter(current_filter)
    query = query.order_by(ResearchProject.year.desc())

    total_count = query.count()
    results = query.offset(offset).limit(limit).all()

    return {"status": "success", "data": {"total": total_count, "items": _build_result_items(results)}}
