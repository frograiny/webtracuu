import os
import sys

# Thêm thư mục hiện tại vào sys.path để import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine, Base, SessionLocal
from app.models.project import ResearchProject
from app.core.config import settings

def seed_database():
    print(f"Dang khoi tao database ({settings.DATABASE_URL[:20]}...)")
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
        ),
        ResearchProject(
            id="NCKH-2024-002",
            title="Phát triển hệ thống quản lý rác thải thông minh trong đô thị",
            author="Lê Văn Bình",
            target_audience="Sinh viên",
            field="Công nghệ thông tin",
            year=2024,
            status="Đang thực hiện",
            abstract="Nghiên cứu và xây dựng hệ thống cảm biến giám sát mức rác thải...",
            keywords=["Smart City", "IoT", "Môi trường"],
            document_type="Đề tài NCKH"
        ),
        ResearchProject(
            id="NCKH-2023-003",
            title="Nghiên cứu tác động của biến đổi khí hậu đến năng suất lúa tại ĐBSCL",
            author="Nguyễn Thị Chi",
            target_audience="Giảng viên",
            field="Nông nghiệp",
            year=2023,
            status="Đã nghiệm thu",
            abstract="Phân tích số liệu khí tượng và thực nghiệm canh tác...",
            keywords=["Biến đổi khí hậu", "Nông nghiệp", "Lúa gạo"],
            document_type="Đề tài NCKH"
        ),
        ResearchProject(
            id="NCKH-2023-004",
            title="Xây dựng ứng dụng học tiếng Anh tương tác cho trẻ em tiểu học",
            author="Phạm Văn Dũng",
            target_audience="Giáo viên",
            field="Công nghệ giáo dục",
            year=2023,
            status="Đã nghiệm thu",
            abstract="Phát triển phần mềm hỗ trợ học tập thông qua trò chơi...",
            keywords=["EdTech", "English", "Children"],
            document_type="Sản phẩm"
        ),
        ResearchProject(
            id="NCKH-2024-003",
            title="Sản xuất phân bón hữu cơ từ phụ phẩm nông nghiệp quy mô hộ gia đình",
            author="Hoàng Văn Em",
            target_audience="Học sinh",
            field="Sinh học",
            year=2024,
            status="Đang thực hiện",
            abstract="Quy trình ủ phân hữu cơ vi sinh từ vỏ trái cây và bã trà...",
            keywords=["Organic", "Biology", "Recycle"],
            document_type="Dự án học sinh"
        ),
        ResearchProject(
            id="NCKH-2022-006",
            title="Thiết kế và chế tạo Robot hỗ trợ vận chuyển trong bệnh viện",
            author="Nguyễn Văn Phúc",
            target_audience="Sinh viên",
            field="Cơ điện tử",
            year=2022,
            status="Đã nghiệm thu",
            abstract="Robot tự hành có khả năng tránh vật cản và vận chuyển vật tư y tế...",
            keywords=["Robot", "Medical", "Automation"],
            document_type="Đề tài NCKH"
        ),
        ResearchProject(
            id="NCKH-2023-005",
            title="Phân tích xu hướng tiêu dùng xanh của giới trẻ tại các thành phố lớn",
            author="Đỗ Thị Giang",
            target_audience="Giảng viên",
            field="Kinh tế",
            year=2023,
            status="Đã nghiệm thu",
            abstract="Khảo sát và đánh giá hành vi mua sắm các sản phẩm thân thiện môi trường...",
            keywords=["Green Marketing", "Consumer Behavior"],
            document_type="Đề tài NCKH"
        ),
        ResearchProject(
            id="NCKH-2024-004",
            title="Ứng dụng công nghệ Blockchain trong truy xuất nguồn gốc nông sản",
            author="Bùi Văn Hùng",
            target_audience="Sinh viên",
            field="Công nghệ thông tin",
            year=2024,
            status="Đang thực hiện",
            abstract="Xây dựng nền tảng minh bạch hóa thông tin chuỗi cung ứng...",
            keywords=["Blockchain", "Traceability", "AgriTech"],
            document_type="Đề tài NCKH"
        ),
        ResearchProject(
            id="NCKH-2023-006",
            title="Nghiên cứu sức khỏe tâm thần của học sinh sau đại dịch COVID-19",
            author="Vũ Thị Hồng",
            target_audience="Giáo viên",
            field="Tâm lý học",
            year=2023,
            status="Đã nghiệm thu",
            abstract="Đánh giá mức độ lo âu và đề xuất các giải pháp hỗ trợ tâm lý...",
            keywords=["Psychology", "Mental Health", "School"],
            document_type="Đề tài NCKH"
        ),
        ResearchProject(
            id="NCKH-2022-007",
            title="Cải tiến quy trình sản xuất nước mắm truyền thống ít muối",
            author="Lý Văn Nam",
            target_audience="Giảng viên",
            field="Công nghệ thực phẩm",
            year=2022,
            status="Đã nghiệm thu",
            abstract="Ứng dụng công nghệ lọc và lên men tiên tiến để giảm hàm lượng natri...",
            keywords=["Food Tech", "Traditional"],
            document_type="Đề tài NCKH"
        ),
        ResearchProject(
            id="NCKH-2024-005",
            title="Giải pháp năng lượng mặt trời mini cho đèn đường nông thôn",
            author="Nguyễn Văn Khánh",
            target_audience="Học sinh",
            field="Vật lý",
            year=2024,
            status="Đang thực hiện",
            abstract="Thiết kế bộ đèn led tích hợp tấm pin năng lượng mặt trời giá rẻ...",
            keywords=["Solar", "Physics", "Rural"],
            document_type="Dự án học sinh"
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
