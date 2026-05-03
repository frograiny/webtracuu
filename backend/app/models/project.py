from sqlalchemy import Column, Integer, String, Text, JSON, event  # type: ignore
from app.db.session import Base
from app.utils.text import remove_diacritics


class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    target_audience = Column(String)  # Giáo viên, Học sinh
    field = Column(String)            # Lĩnh vực
    year = Column(Integer)
    status = Column(String)
    abstract = Column(Text)
    keywords = Column(JSON, default=[])  # Từ khóa/Tags
    document_type = Column(String, nullable=True)
    implementation_year = Column(Integer, nullable=True)

    # --- Cột chuẩn hóa cho tìm kiếm nhanh (pre-computed, indexed) ---
    title_normalized = Column(String, nullable=True, index=True)
    author_normalized = Column(String, nullable=True, index=True)


def _auto_normalize(mapper, connection, target):
    """Tự động cập nhật cột normalized khi insert/update."""
    if target.title:
        target.title_normalized = remove_diacritics(target.title).lower()
    if target.author:
        target.author_normalized = remove_diacritics(target.author).lower()


event.listen(ResearchProject, "before_insert", _auto_normalize)
event.listen(ResearchProject, "before_update", _auto_normalize)
