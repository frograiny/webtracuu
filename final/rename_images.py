import os

# Đường dẫn thư mục chứa ảnh (thư mục final)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Danh sách mapping tên file cũ -> tên file mới (theo chuẩn số thứ tự báo cáo)
rename_map = {
    # Chương 2
    "hethong.png": "2.1.png",
    "usercase.png": "2.2.png",
    "usecase_chinhsuadetai.png": "2.3.png",
    "usecase_quantri.png": "2.4.png",
    
    # Chương 3
    "image.png": "3.1.png",
    "bieudohoatdong_luongtimkiem.png": "3.2.png",
    # 3.3.png đã chuẩn tên rồi nên không cần đổi
    "luondangbaiduyetbai.png": "3.4.png",
    "luongquantri_phanquyen.png": "3.6.png",
    
    # Chương 4
    "luongtuongtac.png": "4.2.png",
    "sodo_pakage.png": "4.3.png",
    "Component_Backend_theo_cac_module.png": "4.4.png",
    "Sequence diagram_cho_luong_Refresh_Token.png": "4.6.png",
    "Component_diagram_cho_module_Tim_kiem.png": "4.7.png",
    "so_do_luong_du_lieu_lutru_tep.png": "4.9.png",
    "du_lieu_logic_rut_gon.png": "4.10.png",
    "Phan_loai_nhom_theo_api_modul.png": "4.12.png",
    "So_do_bao_mat_nhieu_tang.png": "4.13.png",
    "So_do_trien_khai_bang_docker.png": "4.14.png",
    "trien_khai_Production.png": "4.15.png",
    "code_be.png": "4.16.png",
    
    # Chương 5
    "trangchu.png": "5.1.png"
}

def rename_images():
    print("Đang tiến hành đổi tên hàng loạt ảnh...")
    success_count = 0
    for old_name, new_name in rename_map.items():
        old_path = os.path.join(script_dir, old_name)
        new_path = os.path.join(script_dir, new_name)
        
        # Kiểm tra xem file cũ có tồn tại không
        if os.path.exists(old_path):
            try:
                # Nếu file mới đã tồn tại thì xóa trước khi đổi tên để tránh lỗi
                if os.path.exists(new_path):
                    os.remove(new_path)
                os.rename(old_path, new_path)
                print(f" [OK] Đã đổi: {old_name} ---> {new_name}")
                success_count += 1
            except Exception as e:
                print(f" [LỖI] Không thể đổi tên {old_name}: {e}")
        else:
            # Nếu không tìm thấy file cũ, có thể người dùng đã đổi tên nó rồi hoặc chưa tạo
            pass
            
    print(f"\n🎉 HOÀN TẤT! Đã đổi tên thành công {success_count} file ảnh theo chuẩn X.Y.png")

if __name__ == "__main__":
    rename_images()
