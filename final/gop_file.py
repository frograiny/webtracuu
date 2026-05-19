import os

# Lấy đường dẫn tuyệt đối của thư mục chứa script này (tức là thư mục 'final')
script_dir = os.path.dirname(os.path.abspath(__file__))

# Danh sách các file cần gộp theo đúng thứ tự
files_to_merge = [
    "trang_bia_muc_luc.md",
    "chuong_1.md",
    "chuong_2_part1.md",
    "chuong_2_part2.md",
    "chuong_3_part1.md",
    "chuong_3_part2.md",
    "chuong_4_part1.md",
    "chuong_4_part2.md",
    "chuong_4_part3.md",
    "chuong_5_6.md",
    "cac_so_do_bo_sung.md"
]

# File đầu ra cũng sẽ nằm trong cùng thư mục 'final'
output_file = os.path.join(script_dir, "bao_cao_hoan_chinh_FULL.md")

def merge_files():
    print("Đang tiến hành gộp các file báo cáo...")
    with open(output_file, "w", encoding="utf-8") as outfile:
        for fname in files_to_merge:
            filepath = os.path.join(script_dir, fname)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as infile:
                    outfile.write(f"<!-- BẮT ĐẦU FILE: {fname} -->\n\n")
                    outfile.write(infile.read())
                    outfile.write(f"\n\n<!-- KẾT THÚC FILE: {fname} -->\n\n")
                print(f" [OK] Đã gộp: {fname}")
            else:
                print(f" [LỖI] Không tìm thấy file: {filepath}")
                
    print(f"\n🎉 HOÀN TẤT! Toàn bộ nội dung đã được gộp an toàn vào file: {output_file}")
    print("Vui lòng mở file này bằng Typora hoặc VSCode để kiểm tra trước khi xuất PDF.")

if __name__ == "__main__":
    merge_files()
