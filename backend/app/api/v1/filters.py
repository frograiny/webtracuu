from fastapi import APIRouter, Depends # type: ignore
from sqlalchemy.orm import Session # type: ignore
from app.db.session import get_db
from app.models.project import ResearchProject

router = APIRouter()

@router.get("/")
def get_filters(db: Session = Depends(get_db)):
    """
    Lấy danh sách các tùy chọn bộ lọc (Lĩnh vực, Năm, Đối tượng)
    Sử dụng để populate dropdown trên Frontend
    """
    fields = db.query(ResearchProject.field).distinct().order_by(ResearchProject.field).all()
    field_list = ["Tất cả"] + [f[0] for f in fields if f[0]]

    years = db.query(ResearchProject.year).distinct().order_by(ResearchProject.year.desc()).all()
    year_list = ["Tất cả"] + [str(y[0]) for y in years if y[0]]

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
