import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session  # type: ignore

from app.db.session import SessionLocal
from app.models.project import ResearchProject
from app.utils.audience import normalize_target_audience


def normalize_existing_target_audience() -> None:
    db: Session = SessionLocal()

    try:
        projects = db.query(ResearchProject).all()
        updated_count = 0

        for project in projects:
            normalized_value = normalize_target_audience(project.target_audience)
            if project.target_audience != normalized_value:
                project.target_audience = normalized_value
                updated_count += 1

        db.commit()
        print(f"Normalized target audience for {updated_count} projects.")
    except Exception as exc:
        db.rollback()
        print(f"Failed to normalize target audience: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    normalize_existing_target_audience()
