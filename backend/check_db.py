import psycopg2  # type: ignore
from app import DATABASE_URL  # type: ignore

print("Connecting to:", DATABASE_URL)
try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'research_projects';")
    columns = cursor.fetchall()
    print("Columns in research_projects:", [c[0] for c in columns])
    
    cursor.execute("SELECT * FROM research_projects LIMIT 1;")
    data = cursor.fetchall()
    print("Data sample:", data)
    
except Exception as e:
    print("Error:", e)
finally:
    if 'conn' in locals() and conn:
        conn.close()
