#!/bin/bash
set -e

echo "=== VNU Research Backend - Docker Entrypoint ==="
echo "DATABASE_URL = $DATABASE_URL"

# Đợi PostgreSQL sẵn sàng
echo "Waiting for PostgreSQL..."
until python -c "
import os, psycopg2
try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    conn.close()
    print('  Connected!')
except Exception as e:
    print(f'  Not ready: {e}')
    raise SystemExit(1)
" 2>/dev/null; do
    echo "  PostgreSQL not ready, retrying in 2s..."
    sleep 2
done
echo "PostgreSQL is ready!"

# Enable unaccent extension
echo "Enabling PostgreSQL extensions..."
python -c "
import os, psycopg2
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cursor = conn.cursor()
cursor.execute('CREATE EXTENSION IF NOT EXISTS unaccent;')
cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
conn.commit()
try:
    cursor.execute('ALTER FUNCTION unaccent(text) IMMUTABLE;')
    conn.commit()
    print('  Successfully altered built-in unaccent to IMMUTABLE.')
except Exception as e:
    print(f'  Skipped altering built-in unaccent (insufficient privileges). Creating public.immutable_unaccent wrapper instead...')
    conn.rollback()
cursor.execute(\"CREATE OR REPLACE FUNCTION public.immutable_unaccent(text) RETURNS text AS 'SELECT unaccent(\$1)' LANGUAGE sql IMMUTABLE;\")
conn.commit()
cursor.close()
conn.close()
print('Extensions and immutable_unaccent wrapper configured successfully!')
"

# Chạy migration (tạo bảng nếu chưa có)
echo "Running database setup..."
python -c "
from app.db.session import engine, Base
from app.models.project import ResearchProject
from app.models.user import User
Base.metadata.create_all(bind=engine)
print('Tables created/verified successfully!')
"

# Seed dữ liệu mẫu nếu DB trống
python -c "
from app.db.session import SessionLocal
from app.models.project import ResearchProject
db = SessionLocal()
count = db.query(ResearchProject).count()
db.close()
if count == 0:
    print('Database empty, seeding sample data...')
    from seed_data import seed_database
    seed_database()
else:
    print(f'Database already has {count} projects, skipping seed.')
"

# Khởi chạy FastAPI
echo "Starting Uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 "$@"
