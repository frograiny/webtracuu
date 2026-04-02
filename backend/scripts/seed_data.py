import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session # type: ignore
from app.db.session import SessionLocal, engine
from app.models.project import ResearchProject
from app.utils.audience import normalize_target_audience

mock_projects = [
  
  {
    "id": "NCKH-2023-001",
    "title": "Ứng dụng trí tuệ nhân tạo trong việc cá nhân hóa lộ trình học tập",
    "author": "Nguyễn Văn An",
    "target_audience": "Giảng viên",
    "field": "Công nghệ thông tin",
    "year": 2023,
    "status": "Đã nghiệm thu",
    "abstract": "Nghiên cứu ứng dụng các thuật toán học máy để phân tích kết quả học tập và đề xuất lộ trình riêng biệt.",
    "keywords": ["AI", "Giáo dục", "Cá nhân hóa"],
    "document_type": "Đề tài NCKH",
    "implementation_year": 2023
  },
  {
    "id": "NCKH-2023-002",
    "title": "Phân tích tác động của biến đổi khí hậu đến năng suất lúa tại Đồng bằng sông Cửu Long",
    "author": "Trần Thị Bình",
    "target_audience": "Nông dân, Nhà quản lý",
    "field": "Nông nghiệp",
    "year": 2023,
    "status": "Đang thực hiện",
    "abstract": "Đánh giá sự thay đổi lưu lượng nước và xâm nhập mặn ảnh hưởng đến các vụ mùa chính.",
    "keywords": ["Biến đổi khí hậu", "Lúa gạo", "ĐBSCL"],
    "document_type": "Đề tài NCKH",
    "implementation_year": 2023
  },
  {
    "id": "NCKH-2024-005",
    "title": "Xây dựng hệ thống Chatbot hỗ trợ tư vấn tâm lý học đường cho học sinh THPT",
    "author": "Lê Hoàng Nam",
    "target_audience": "Sinh viên",
    "field": "Tâm lý học",
    "year": 2024,
    "status": "Mới đăng ký",
    "abstract": "Sử dụng xử lý ngôn ngữ tự nhiên (NLP) để nhận diện dấu hiệu trầm cảm và lo âu ở lứa tuổi học đường.",
    "keywords": ["Chatbot", "Tâm lý", "Học sinh"],
    "document_type": "Đề tài NCKH",
    "implementation_year": 2024
  },
  {
    "id": "NCKH-2022-012",
    "title": "Giải pháp phát triển kinh tế số cho doanh nghiệp vừa và nhỏ (SMEs) tại Việt Nam",
    "author": "Phạm Minh Đức",
    "target_audience": "Doanh nghiệp",
    "field": "Kinh tế",
    "year": 2022,
    "status": "Đã nghiệm thu",
    "abstract": "Đề xuất các mô hình chuyển đổi số phù hợp với nguồn lực hạn chế của các SMEs hiện nay.",
    "keywords": ["Kinh tế số", "SMEs", "Chuyển đổi số"],
    "document_type": "Đề tài NCKH",
    "implementation_year": 2022
  },
  {
    "id": "NCKH-2023-045",
    "title": "Nghiên cứu quy trình sản xuất nhựa sinh học từ vỏ tôm",
    "author": "Vũ Thu Thảo",
    "target_audience": "Nhà máy sản xuất",
    "field": "Hóa học - Môi trường",
    "year": 2023,
    "status": "Đã nghiệm thu",
    "abstract": "Tận dụng phế phẩm thủy sản để tạo ra vật liệu thân thiện với môi trường, thay thế nhựa truyền thống.",
    "keywords": ["Nhựa sinh học", "Vỏ tôm", "Môi trường"],
    "document_type": "Đề tài NCKH",
    "implementation_year": 2023
  },
  {
    "id": "NCKH-2024-001",
    "title": "Tối ưu hóa thuật toán Blockchain trong bảo mật giao dịch ngân hàng",
    "author": "Hoàng Anh Tuấn",
    "target_audience": "Tổ chức tài chính",
    "field": "Công nghệ thông tin",
    "year": 2024,
    "status": "Đang thực hiện",
    "abstract": "Cải thiện tốc độ xác thực giao dịch trong khi vẫn đảm bảo tính bảo mật tuyệt đối của chuỗi khối.",
    "keywords": ["Blockchain", "Bảo mật", "Ngân hàng"],
    "document_type": "Đề tài NCKH",
    "implementation_year": 2024
  },
  {
    "id": "NCKH-2023-088",
    "title": "Ảnh hưởng của mạng xã hội đến hành vi tiêu dùng của Gen Z",
    "author": "Đặng Hồng Nhung",
    "target_audience": "Nhà tiếp thị",
    "field": "Marketing",
    "year": 2023,
    "status": "Đã nghiệm thu",
    "abstract": "Khảo sát thói quen mua sắm trực tuyến qua TikTok và Facebook của giới trẻ thành thị.",
    "keywords": ["Gen Z", "Mạng xã hội", "Hành vi tiêu dùng"],
    "document_type": "Đề tài NCKH",
    "implementation_year": 2023
  },
  {
    "id": "NCKH-2022-105",
    "title": "Thiết kế hệ thống tưới nước tự động dựa trên cảm biến độ ẩm đất",
    "author": "Ngô Quốc Cường",
    "target_audience": "Nông dân",
    "field": "Cơ điện tử",
    "year": 2022,
    "status": "Đã nghiệm thu",
    "abstract": "Chế tạo thiết bị IoT giúp tự động hóa việc chăm sóc cây trồng, tiết kiệm 30% lượng nước tưới.",
    "keywords": ["IoT", "Nông nghiệp thông minh", "Tự động hóa"],
    "document_type": "Đề tài NCKH",
    "implementation_year": 2022
  },
  {
    "id": "NCKH-2024-019",
    "title": "Phát triển Vaccine thảo dược phòng bệnh cho cá tra",
    "author": "Trịnh Xuân Bắc",
    "target_audience": "Hộ nuôi thủy sản",
    "field": "Sinh học",
    "year": 2024,
    "status": "Đang thực hiện",
    "abstract": "Nghiên cứu các loại thảo mộc có khả năng kháng khuẩn cao để giảm thiểu việc sử dụng kháng sinh.",
    "keywords": ["Cá tra", "Thủy sản", "Thảo dược"],
    "document_type": "Đề tài NCKH",
    "implementation_year": 2024
  },
  {
    "id": "NCKH-2023-112",
    "title": "Bảo tồn giá trị văn hóa cồng chiêng trong thời đại du lịch số",
    "author": "H'Lý Niê",
    "target_audience": "Nhà văn hóa",
    "field": "Văn hóa học",
    "year": 2023,
    "status": "Đã nghiệm thu",
    "abstract": "Xây dựng bảo tàng ảo và ứng dụng AR để giới thiệu văn hóa Tây Nguyên đến du khách quốc tế.",
    "keywords": ["Văn hóa", "Cồng chiêng", "Du lịch"],
    "document_type": "Đề tài NCKH",
    "implementation_year": 2023
  },

    {
        "id": "NCKH-2022-005",
        "title": "Thiết kế hệ thống tưới tiêu tự động sử dụng năng lượng mặt trời cho vườn trường",
        "author": "Phạm Minh Đức",
        "target_audience": "Sinh viên",
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
                p_data["target_audience"] = normalize_target_audience(p_data.get("target_audience"))
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
