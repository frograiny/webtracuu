# 📋 KỲ HOẠCH THỰC HIỆN - RESKIN GIAO DIỆN CỔNG THÔNG TIN HỌC THUẬT

**Ngày lập kế hoạch:** 15/03/2026  
**Trạng thái:** 🚀 Sẵn sàng thực hiện

---

## 🎯 MỤC TIÊU CHÍNH
Chuyển đổi từ giao diện Dashboard (bo tròn hiện tại) sang **Cổng thông tin học thuật** chuẩn web đại học VNU

---

## 📦 PHẦN I: FRONTEND (UI/UX RESKIN)

### 1. LÀM LẠI LAYOUT CẢ TRANG

#### ✅ TOPBAR (Mới tạo)
- **Vị trí:** Trên cùng trang, thanh ngang nhỏ
- **Màu sắc:** Xám đậm hoặc xanh đậm
- **Nội dung:**
  - Số điện thoại: `+84 (0)2 3629-XXXX`
  - Email: `vnu@vnu.edu.vn`
  - Link nội bộ (Portal, Mail, ...)
- **Thành phần mới cần tạo:**
  - `src/components/Layout/Topbar.tsx`

#### ✅ HEADER (Cấu trúc hiện tại cần sửa)
- **Background:** Trắng
- **Bố cục:** 2 phần
  - **Trái (Logo + Tên khoa):**
    - Logo VNU (hình ảnh hoặc vector)
    - Tên khoa: **Tiếng Việt in đậm** (Khoa Công Nghệ Thông Tin)
    - Tên khoa: *Tiếng Anh size nhỏ hơn* (School of Information Technology)
  - **Phải (Navigation Menu):** 
    - Các mục: **NGHIÊN CỨU**, **TUYỂN DỤNG**, **ĐÀO TẠO**, **LIÊN HỆ** (tất cả IN HOA)
    - Chữ in đậm, style: bold
- **Thành phần mới cần tạo:**
  - `src/components/Layout/Header.tsx`
  - `src/components/Layout/Navigation.tsx`

#### ✅ MAIN CONTENT (Chia lưới 75-25)
- **Cột trái (75%)**
  - Tiêu đề mục: `| NGHIÊN CỨU KHOA HỌC` (có dấu `|` phía trước)
  - Thanh tìm kiếm (SearchBar - sửa styling)
  - Kết quả tìm kiếm (Results area)
  
- **Cột phải (25%) - Sidebar**
  - **Phần 1: BẢNG TIN KHOA**
    - Danh sách tin tức/thông báo gần đây
    - Mỗi item: Tiêu đề + Ngày
  - **Phần 2: LIÊN KẾT NGOÀI**
    - Các link hữu ích (Website chính, Forum, ...)
    - Mỗi link: Icon + Text
- **Thành phần mới cần tạo:**
  - `src/components/Layout/Sidebar.tsx`
  - `src/components/Layout/MainLayout.tsx` (wrapper chính)

---

### 2. CHỈNH SỬA COMPONENT SEARCHBAR

#### 📝 Thay đổi Styling
| Thuộc tính | Hiện tại | Mới |
|-----------|---------|-----|
| **Border Radius** | `rounded-2xl` (bo tròn 24px) | `rounded-sm` hoặc `rounded-md` (góc vuông/nhẹ) |
| **Border** | `border-gray-200` | Border mỏng, dark mode: `border-gray-300` |
| **Focus Color** | `focus:border-blue-500` | `focus:border-[#005073]` (Xanh VNU) |
| **Focus Ring** | `focus-within:ring-blue-100` | `focus-within:ring-[#E8F3FA]` (Xanh nhạt VNU) |
| **Shadow** | `shadow-sm` | Tính toán lại (optional) |

#### 🔧 Chức năng Giữ Nguyên
- ✅ Debounce (300ms)
- ✅ Dropdown phân loại: Đề tài / Luận văn / Khóa luận
- ✅ Gọi Mock API
- ✅ Clear button (nút X xóa text)
- ✅ Loading indicator

#### 📂 File cần sửa
- `src/components/Search/SearchBar.tsx` - Thay đổi className Tailwind

---

## 📦 PHẦN II: BACKEND (PYTHON/FASTAPI)

### 1. CẬP NHẬT DATABASE SCHEMA

#### 📋 Thêm cột vào bảng `research_projects`
```sql
-- Cột 1: document_type (Loại tài liệu)
ALTER TABLE research_projects ADD COLUMN document_type VARCHAR(50);
-- Giá trị có thể: 'Đề tài', 'Luận văn', 'Khóa luận', 'Báo cáo', v.v.

-- Cột 2: implementation_year (Năm thực hiện - chi tiết hơn)
ALTER TABLE research_projects ADD COLUMN implementation_year INTEGER;
-- Giá trị: năm cụ thể (2024, 2025, v.v.)

-- Tạo Index cho cột mới để tăng tốc độ truy vấn
CREATE INDEX idx_document_type ON research_projects(document_type);
```

#### 📝 File cần sửa
- `app.py` - Cập nhật class `ResearchProject` thêm 2 cột mới

---

### 2. NÂNG CẤP THUẬT TOÁN TÌM KIẾM

#### 🔍 Sử dụng PostgreSQL + Extension pg_trgm + GIN Index
**Lợi ích:**
- Tìm kiếm "Fuzzy" (gần đúng, không cần chính xác từng chữ)
- Tốc độ siêu nhanh với GIN Index
- Sắp xếp theo độ phù hợp

**SQL đã có sẵn trong code:**
```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_project_title_trgm ON research_projects USING GIN (title gin_trgm_ops);
CREATE INDEX idx_project_abstract_trgm ON research_projects USING GIN (abstract gin_trgm_ops);
```

**Backend đã dùng:** `func.similarity()` từ SQLAlchemy ✅ (không cần thay đổi)

---

### 3. CẬP NHẬT SEARCH API ENDPOINT

#### 📡 Endpoint `/api/v1/projects/search` - Thêm tham số `type`

**Tham số hiện tại:**
```
GET /api/v1/projects/search?q=AI&field=Công%20Nghệ&year=2024&target=Giáo%20viên
```

**Thêm tham số mới:**
```
GET /api/v1/projects/search?q=AI&type=Đề%20tài&field=Công%20Nghệ&year=2024&target=Giáo%20viên
```

**Chi tiết Parameter:**
| Tham số | Kiểu | Mô tả | Giá trị ví dụ |
|--------|------|-------|--------------|
| `q` | string | Từ khóa tìm kiếm | `"AI"` |
| `type` | string | Loại tài liệu (NEW) | `"Đề tài"`, `"Luận văn"`, `"Khóa luận"` |
| `field` | string | Lĩnh vực | `"Công Nghệ"` |
| `year` | string | Năm thực hiện | `"2024"` |
| `target` | string | Đối tượng | `"Giáo viên"` |
| `limit` | int | Số kết quả | `20` |
| `offset` | int | Phân trang | `0` |

#### 📝 File cần sửa
- `app.py` - Hàm `search_projects()` thêm parameter `document_type`

---

### 4. XỬ LÝ CORS (Đã sẵn có ✅)
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: chỉ định domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
**Trạng thái:** ✅ Đã hoàn thiện, không cần thay đổi

---

## 📊 ĐÁNH GIÁ HỆ THỐNG HIỆN TẠI

### ✅ Điểm Tốt
1. **Backend:** 
   - ✅ Cấu trúc FastAPI sạch, rõ ràng
   - ✅ Có CORS middleware
   - ✅ PostgreSQL + pg_trgm sẵn sàng
   - ✅ API endpoint logic hợp lý
   - ✅ Logging chuẩn

2. **Frontend:**
   - ✅ React + TypeScript được cấu hình
   - ✅ Debounce hook hoạt động tốt
   - ✅ Component structure tổ chức tốt
   - ✅ Tailwind CSS áp dụng đúng

### ⚠️ Vấn đề cần cải thiện
1. **Frontend:**
   - ❌ Thiếu Layout component (Topbar, Header, Sidebar)
   - ❌ SearchBar styling quá "modern" (bo tròn thì đậm), cần "minimalist" hơn
   - ❌ Chưa có component cho Section Title (`| NGHIÊN CỨU KHOA HỌC`)
   - ❌ Sidebar chưa được thiết kế

2. **Backend:**
   - ❌ Chưa thêm cột `document_type` vào Database
   - ❌ API endpoint chưa hỗ trợ filter theo `type`
   - ❌ Database seed data chưa có giá trị `document_type`

3. **Cấu trúc Folder:**
   - ❌ `src/components/Layout/` folder trống (cần tạo component)
   - ⚠️ Cần tạo thêm component cho News/Sidebar

---

## 🔗 CORS - TRẠNG THÁI HIỆN TẠI
| Item | Trạng thái | Ghi chú |
|------|----------|--------|
| Allow Origins | ✅ `["*"]` | Production nên thay `localhost:3000` |
| Allow Methods | ✅ `["*"]` | GET, POST, PUT, DELETE đều OK |
| Allow Headers | ✅ `["*"]` | Content-Type, Authorization, v.v. |
| Credentials | ✅ `True` | Cookie support enabled |

---

## 📝 THỨ TỰ THỰC HIỆN KHUYÊN NGHỊ

### Giai đoạn 1: Backend (1-2 tiếng)
- [ ] Cập nhật Database Schema (thêm 2 cột)
- [ ] Cập nhật Model ResearchProject
- [ ] Cập nhật endpoint search (thêm filter `type`)
- [ ] Kiểm tra API với Postman/Swagger

### Giai đoạn 2: Frontend - Layout (2-3 tiếng)
- [ ] Tạo Topbar component
- [ ] Tạo Header component với Logo + Navigation
- [ ] Tạo Sidebar component (News + Links)
- [ ] Tạo MainLayout wrapper

### Giai đoạn 3: Frontend - Component Styling (1-2 tiếng)
- [ ] Chỉnh SearchBar: từ bo tròn → góc vuông, màu xanh VNU
- [ ] Tạo SectionTitle component (`| NGHIÊN CỨU KHOA HỌC`)
- [ ] Cập nhật App.tsx để dùng MainLayout
- [ ] Test responsive (Mobile, Tablet, Desktop)

### Giai đoạn 4: Testing & Polish (1-2 tiếng)
- [ ] Test toàn bộ flow: Search → Display → Detail
- [ ] Kiểm tra performance
- [ ] Tối ưu hóa CSS
- [ ] Chuẩn bị demo cho nhóm

---

## 📂 CẤU TRÚC FILE SAU KHI HOÀN THÀNH

```
src/
├── components/
│   ├── Layout/
│   │   ├── Topbar.tsx (NEW)
│   │   ├── Header.tsx (NEW)
│   │   ├── Navigation.tsx (NEW)
│   │   ├── Sidebar.tsx (NEW)
│   │   ├── MainLayout.tsx (NEW)
│   │   └── SectionTitle.tsx (NEW)
│   ├── Search/
│   │   ├── SearchBar.tsx (UPDATED - styling)
│   │   └── SearchFilters.tsx (guarda nguyên)
│   └── ProjectCard.tsx (giữ nguyên)
├── App.tsx (UPDATED - dùng MainLayout)
└── ... (các file khác)
```

---

## 🎨 MÀU SẮC VNU KHUYÊN NGHỊ
| Tên | Hex | Tailwind | Mục đích |
|-----|-----|----------|---------|
| **Xanh chính** | `#005073` | custom | Header border, focus |
| **Xanh nhạt** | `#E8F3FA` | custom | Focus ring |
| **Xám đậm** | `#2C3E50` | `gray-800` | Topbar background |
| **Trắng** | `#FFFFFF` | `white` | Header background |
| **Đen chữ** | `#1F2937` | `gray-900` | Text chính |

---

## 📌 GHI CHÚ QUAN TRỌNG

1. **Database Migration:** 
   - Backup database trước khi thêm cột
   - SQL script có sẵn, chỉ cần chạy

2. **Frontend Build:**
   - Sau khi sửa TypeScript, chạy `npm run build` để check lỗi
   - Dùng `npm run dev` để test live

3. **API Testing:**
   - Dùng Swagger UI: `http://localhost:8000/docs`
   - Hoặc Postman với endpoint: `http://localhost:8000/api/v1/projects/search`

4. **Git Commit:**
   - Commit từng giai đoạn để dễ revert nếu cần
   - Ví dụ: `feat: Add Topbar and Header components` 

---

**Chúc bạn thực hiện hiệu quả! 🚀**
