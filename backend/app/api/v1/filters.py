from fastapi import APIRouter, Depends  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.db.session import get_db  # type: ignore
from app.models.project import ResearchProject  # type: ignore
from app.utils.audience import normalize_target_audience_options

router = APIRouter()


@router.get("/")
def get_filters(db: Session = Depends(get_db)):
    fields = db.query(ResearchProject.field).distinct().order_by(ResearchProject.field).all()
    field_list = ["Tất cả"] + [f[0] for f in fields if f[0]]

    years = db.query(ResearchProject.year).distinct().order_by(ResearchProject.year.desc()).all()
    year_list = ["Tất cả"] + [str(y[0]) for y in years if y[0]]

    audiences = db.query(ResearchProject.target_audience).distinct().all()
    audience_list = normalize_target_audience_options(a[0] for a in audiences)

    return {
        "status": "success",
        "data": {
            "fields": field_list,
            "years": year_list,
            "audiences": audience_list,
        },
    }
