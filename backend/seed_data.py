import os
import sys

# Thêm thư mục hiện tại vào sys.path để import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine, Base, SessionLocal
from app.models.project import ResearchProject

def seed_database():
    print("Dang khoi tao database SQLite...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Dữ liệu mẫu (từ ResearchProjectDemo.jsx)
    projects = [
        ResearchProject(
            id="NCKH-2023-001",
            title="Ứng dụng trí tuệ nhân tạo trong việc cá nhân hóa lộ trình học tập",
            author="Nguyễn Văn An",
            target_audience="Giáo viên",
            field="Công nghệ thông tin",
            year=2023,
            status="Đã nghiệm thu",
            abstract="Nghiên cứu ứng dụng các thuật toán học máy...",
            keywords=["AI", "Giáo dục", "Cá nhân hóa"],
            document_type="Đề tài NCKH"
        ),
        ResearchProject(
            id="NCKH-2023-002",
            title="Giải pháp nâng cao ý thức bảo vệ môi trường cho học sinh THPT",
            author="Trần Thị Bích",
            target_audience="Giáo viên",
            field="Khoa học xã hội",
            year=2023,
            status="Đã nghiệm thu",
            abstract="Đề tài tập trung vào việc thiết kế...",
            keywords=["Môi trường", "Ý thức"],
            document_type="Dự án"
        ),
        ResearchProject(
            id="NCKH-2024-001",
            title="Chế tạo vật liệu sinh học thay thế nhựa từ vỏ trấu",
            author="Lê Hoàng Cường",
            target_audience="Học sinh",
            field="Hóa học & Vật liệu",
            year=2024,
            status="Đang thực hiện",
            abstract="Dự án nghiên cứu quy trình xử lý...",
            keywords=["Vật liệu sinh học", "Vỏ trấu"],
            document_type="Dự án học sinh"
        ),
        ResearchProject(
            id="NCKH-2022-005",
            title="Hệ thống tưới tiêu tự động năng lượng mặt trời",
            author="Phạm Minh Đức",
            target_audience="Học sinh",
            field="Kỹ thuật cơ điện",
            year=2022,
            status="Đã nghiệm thu",
            abstract="Hệ thống sử dụng cảm biến độ ẩm...",
            keywords=["IoT", "Năng lượng mặt trời"],
            document_type="Sản phẩm"
        )
    ]
    
    try:
        # Xóa dữ liệu cũ nếu có
        db.query(ResearchProject).delete()
        
        # Thêm dữ liệu mới
        db.add_all(projects)
        db.commit()
        print("OK: Da seed du lieu thanh cong vao research.db!")
    except Exception as e:
        print(f"Error: Loi khi seed du lieu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
