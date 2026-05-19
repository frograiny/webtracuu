import os
import sys

# Đổi thư mục làm việc vào backend để Pydantic đọc được file .env
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
os.chdir(backend_dir)
sys.path.append(backend_dir)

try:
    from app.db.session import SessionLocal
    from app.models.user import User
    from app.core.security import get_password_hash

    def reset_admin():
        db = SessionLocal()
        admin_user = db.query(User).filter(User.role == "admin").first()
        
        print("\n==================================================")
        print("   TOOL KHOI PHUC TAI KHOAN ADMIN")
        print("==================================================\n")
        
        if admin_user:
            print(f"✅ Da tim thay tai khoan Admin cua he thong!")
            print(f"👉 Email dang nhap: {admin_user.email}")
            print(f"👉 Mat khau dang duoc khoi phuc ve: 12345678\n")
            
            admin_user.hashed_password = get_password_hash("12345678")
            db.commit()
            print("🎉 Khoi phuc mat khau thanh cong! Ban hay quay lai web de dang nhap.")
        else:
            print("❌ Khong tim thay tai khoan Admin nao trong CSDL!")
            print("💡 Theo logic code cua ban: Nguoi dau tien bam nut 'Dang ky' tren Web se tu dong duoc cap quyen Admin.")
            print("   Ban hay tao tai khoan moi tren Web la duoc.")
            
        print("\n==================================================")
        db.close()

    if __name__ == "__main__":
        reset_admin()
except Exception as e:
    print(f"Co loi xay ra: {e}")
