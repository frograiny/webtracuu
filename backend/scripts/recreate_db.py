from sqlalchemy import text  # type: ignore
from app import engine, Base  # type: ignore

# Drop all tables and recreate them to apply schema changes
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS research_projects CASCADE;"))
    conn.commit()

Base.metadata.create_all(bind=engine)
print("Database schema dropped and recreated successfully.")
