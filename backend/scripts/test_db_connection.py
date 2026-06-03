import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add current directory to path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import config
try:
    from app.core.config import settings
    db_url = settings.DATABASE_URL
    print(f"Thử kết nối tới: {db_url}")
    
    engine = create_engine(db_url)
    connection = engine.connect()
    print("✅ Kết nối tới Docker Postgres THÀNH CÔNG!")
    connection.close()
except Exception as e:
    print(f"❌ Kết nối THẤT BẠI: {e}")
