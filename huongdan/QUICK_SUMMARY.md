# ⚡ TÓM TẮT NHANH - THAY ĐỔI CẦN LÀM

## 🎯 MỤC TIÊU
Chuyển từ **Dashboard bo tròn** → **Cổng thông tin học thuật** theo tiêu chuẩn web đại học

---

## 🚀 THAY ĐỔI CHÍNH (TOP PRIORITY)

### PHẦN 1: BACKEND (30 phút)
```python
# File: app.py

# 1️⃣ Thêm 2 cột vào Model
class ResearchProject(Base):
    # ... cũ ...
    document_type = Column(String)        # NEW: Đề tài/Luận văn/Khóa luận
    implementation_year = Column(Integer) # NEW: Năm thực hiện

# 2️⃣ Cập nhật endpoint search - thêm tham số 'type'
@app.get("/api/v1/projects/search")
def search_projects(
    q: str,
    field: str,
    target: str,
    year: str,
    doc_type: str = Query("Tất cả"),  # ← NEW
):
    # ... filter logic ...
    if doc_type != "Tất cả":  # ← NEW
        query = query.filter(ResearchProject.document_type == doc_type)

# 3️⃣ Cập nhật get_filters - thêm doc_types
@app.get("/api/v1/filters")
def get_filters(db: Session):
    # ... lấy fields, years, audiences ...
    doc_types = db.query(ResearchProject.document_type).distinct().all()
    return {
        "data": {
            "fields": field_list,
            "years": year_list,
            "audiences": audience_list,
            "doc_types": doc_type_list  # ← NEW
        }
    }
```

---

### PHẦN 2A: FRONTEND - LAYOUT (1 tiếng)

**Tạo 6 component mới trong `src/components/Layout/`:**

#### 1. `Topbar.tsx` - Thanh ngang trên cùng
- Số điện thoại, Email, Links nội bộ
- Background: xám đậm

#### 2. `Header.tsx` - Logo + Tên + Menu
- **Trái:** Logo VNU + Tên Khoa (VN + EN)
- **Phải:** Navigation menu (IN HOA)

#### 3. `Navigation.tsx` - Menu items
- NGHIÊN CỨU, TUYỂN DỤNG, ĐÀO TẠO, ĐỨC HỌC, LIÊN HỆ

#### 4. `SectionTitle.tsx` - Title có line separator
- `| NGHIÊN CỨU KHOA HỌC`

#### 5. `Sidebar.tsx` - Sidebar phải (25%)
- Phần 1: BẢNG TIN KHOA (danh sách tin tức)
- Phần 2: LIÊN KẾT NGOÀI (external links)

#### 6. `MainLayout.tsx` - Main wrapper
- Kết hợp toàn bộ layout
- Grid 75-25 cho main content + sidebar

---

### PHẦN 2B: FRONTEND - STYLING (30 phút)

**Chỉnh 2 file hiện tại:**

#### `SearchBar.tsx` - Thay styling
```
rounded-xl  →  rounded-md       (góc vuông/nhẹ)
border-blue-500  →  border-[#005073]  (xanh VNU)
ring-blue-100  →  ring-[#E8F3FA]      (focus ring)
```

#### `SearchFilters.tsx` - Thêm dropdown
```
Thêm filter: Loại tài liệu
Dropdown: Tất cả / Đề tài / Luận văn / Khóa luận
```

#### `App.tsx` - Wrap with MainLayout
```
<MainLayout>
  {/* SearchBar, Filters, Results */}
</MainLayout>
```

---

## 📊 BẢNG THAY ĐỔI

| Module | File | Thay đổi | Độ phức tạp |
|--------|------|---------|-----------|
| **Backend** | `app.py` | Thêm cột + endpoint | 🟢 Đơn giản |
| **Backend** | SQL Script | Migration | 🟢 Đơn giản |
| **Frontend** | Tạo mới | 6 Layout components | 🟡 Trung bình |
| **Frontend** | `SearchBar.tsx` | CSS styling | 🟢 Đơn giản |
| **Frontend** | `SearchFilters.tsx` | Thêm filter | 🟢 Đơn giản |
| **Frontend** | `App.tsx` | Wrap layout | 🟢 Đơn giản |

---

## 🎨 MÀU SẮC VNU

```
Xanh chính:    #005073  ← Focus border, links
Xanh nhạt:     #E8F3FA  ← Focus ring background
Xám đậm:       #2C3E50  ← Topbar, footer
Trắng:         #FFFFFF  ← Header background
Chữ chính:     #1F2937  ← Text (gray-900)
```

---

## ✅ TASK PRIORITY

```
🔴 URGENT (Backend - 30 phút)
├─ Thêm cột database
├─ Update Model
└─ Update API endpoint

🟡 MEDIUM (Frontend - 1.5 tiếng)
├─ Tạo Layout components
├─ Update SearchBar styling
└─ Wrap App.tsx

⚪ NICE-TO-HAVE
├─ Theme constants file
├─ Responsive testing
└─ Demo slides
```

---

## 📁 STRUCTURE AFTER

```
src/
├── App.tsx (UPDATE: wrap with MainLayout)
├── components/
│   ├── Layout/ (6 NEW files)
│   │   ├── Topbar.tsx
│   │   ├── Header.tsx
│   │   ├── Navigation.tsx
│   │   ├── SectionTitle.tsx
│   │   ├── Sidebar.tsx
│   │   ├── MainLayout.tsx
│   │   └── index.ts
│   ├── Search/
│   │   ├── SearchBar.tsx (UPDATE: styling)
│   │   └── SearchFilters.tsx (UPDATE: add docType)
│   └── ProjectCard.tsx
├── config/
│   └── theme.config.ts (NEW: colors)
└── ...
```

---

## 🚦 NEXT STEPS

**Chọn 1 trong 2 option:**

### Option A: Backend First (Khuyên dùng)
```
1. Update app.py (30 min)
2. Test API (15 min)
3. Làm Frontend layout (1h)
4. Test toàn bộ (30 min)
```

### Option B: Frontend First
```
1. Tạo Layout components (1h)
2. Update SearchBar styling (15 min)
3. Thay đổi Backend (30 min)
4. Test & integrate (30 min)
```

---

**Bạn muốn bắt đầu từ đâu?**

➡️ Backend (app.py + database)  
➡️ Frontend (Layout components)  
➡️ Cùng lúc (parallelize)
