from sqlalchemy import Column, Integer, String, Text, JSON, Computed, Index  # type: ignore
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import deferred  # type: ignore
from app.db.session import Base


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
    search_vector = deferred(
        Column(
            TSVECTOR,
            Computed("setweight(to_tsvector('simple', unaccent(coalesce(title, ''))), 'A') || setweight(to_tsvector('simple', unaccent(coalesce(author, ''))), 'C')", persisted=True),
        )
    )

    __table_args__ = (
        Index("ix_research_projects_search_vector", "search_vector", postgresql_using="gin"),
    )
