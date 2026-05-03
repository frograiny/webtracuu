"""
Script: Backfill normalized columns cho dữ liệu cũ.

Chạy 1 lần sau khi thêm cột title_normalized / author_normalized.
Usage: python -m scripts.backfill_normalized
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.project import ResearchProject
from app.utils.text import remove_diacritics


def backfill():
    db = SessionLocal()
    try:
        projects = db.query(ResearchProject).all()
        updated = 0
        for p in projects:
            changed = False
            if p.title and not p.title_normalized:
                p.title_normalized = remove_diacritics(p.title).lower()
                changed = True
            if p.author and not p.author_normalized:
                p.author_normalized = remove_diacritics(p.author).lower()
                changed = True
            if changed:
                updated += 1

        db.commit()
        print(f"✅ Đã cập nhật {updated}/{len(projects)} records.")
    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
