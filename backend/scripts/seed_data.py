import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session # type: ignore
from app.db.session import SessionLocal, engine
from app.models.project import ResearchProject

mock_projects = [
    {
        "id": "NCKH-2023-001",
        "title": "Ứng dụng trí tuệ nhân tạo trong việc cá nhân hóa lộ trình học tập",
        "author": "Nguyễn Văn An",
        "target_audience": "Giáo viên",
        "field": "Công nghệ thông tin",
        "year": 2023,
        "status": "Đã nghiệm thu",
        "abstract": "Nghiên cứu ứng dụng các thuật toán học máy để phân tích kết quả học tập",
        "keywords": ["AI", "Giáo dục", "Cá nhân hóa"],
        "document_type": "Đề tài NCKH",
        "implementation_year": 2023
    },
    {
        "id": "NCKH-2022-005",
        "title": "Thiết kế hệ thống tưới tiêu tự động sử dụng năng lượng mặt trời cho vườn trường",
        "author": "Phạm Minh Đức",
        "target_audience": "Học sinh",
        "field": "Kỹ thuật cơ điện",
        "year": 2022,
        "status": "Đã nghiệm thu",
        "abstract": "Hệ thống sử dụng cảm biến độ ẩm đất và ánh sáng",
        "keywords": ["IoT", "Năng lượng mặt trời", "Tự động hóa"],
        "document_type": "Đề tài NCKH",
        "implementation_year": 2021
    }
]

def seed():
    db: Session = SessionLocal()
    try:
        if db.query(ResearchProject).count() == 0:
            for p_data in mock_projects:
                project = ResearchProject(**p_data)
                db.add(project)
            db.commit()
            print("Đã tự động nạp dữ liệu mẫu (Seeded)!")
        else:
            print("DB đã có dữ liệu, bỏ qua bước Seed.")
    except Exception as e:
        db.rollback()
        print(f"Lỗi khi seed data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
