# 🔍 ĐÁNH GIÁ CHI TIẾT DỰ ÁN - PHÂN TÍCH HỆ THỐNG

**Ngày phân tích:** 15/03/2026

---

## 📋 TỔNG QUAN CẤU TRÚC

```
d:\nghich\webtruong/
├── [Backend - Python]
│   ├── app.py (FastAPI + PostgreSQL)
│   ├── ai_search_api_fixed.py (AI search - chưa dùng)
│   ├── requirements.txt
│   └── Dockerfile
│
├── [Frontend - React + TypeScript]
│   └── vnu-frontend/
│       ├── src/
│       │   ├── App.tsx (Entry point)
│       │   ├── main.tsx
│       │   ├── components/
│       │   │   ├── Layout/ (EMPTY!)
│       │   │   ├── Search/
│       │   │   │   ├── SearchBar.tsx
│       │   │   │   └── SearchFilters.tsx
│       │   │   └── ProjectCard.tsx
│       │   ├── hooks/
│       │   │   ├── useSearch.ts
│       │   │   └── useDebounce.ts
│       │   ├── services/
│       │   │   ├── httpClient.ts
│       │   │   └── searchService.ts
│       │   ├── types/
│       │   └── config/
│       └── vite.config.ts
│
├── [Database]
│   └── nckh_db/ (SQLite local, production dùng PostgreSQL)
│
└── [Docker]
    └── docker-compose.yml
```

---

## ✅ PHẦN 1: BACKEND ANALYSIS

### file: `app.py`

#### 🟢 ĐIỂM MẠNH
```python
✅ FastAPI structure rõ ràng
✅ CORS middleware setting properly
✅ PostgreSQL connection ready (with env support)
✅ SQLAlchemy ORM pattern tốt
✅ Endpoint logic hợp lý (search, filter, detail)
✅ pg_trgm similarity search implementation
✅ Logging system initialized
✅ Error handling có sẵn
```

#### ⚠️ VẤN ĐỀ CẦN FIX

**1. Database Schema (ResearchProject Model)**
```python
# ❌ HỌ CÒN THIẾU 2 TRƯỜNG
class ResearchProject(Base):
    # ... hiện tại có:
    id, title, author, target_audience, field, year, status, abstract, keywords
    
    # ❌ THIẾU:
    # - document_type (Đề tài / Luận văn / Khóa luận)
    # - implementation_year (chi tiết năm thực hiện)
```

**2. Search Endpoint - chưa filter theo `type`**
```python
# ❌ HIỆN TẠI
@app.get("/api/v1/projects/search")
def search_projects(
    q: str = Query(""),
    field: str = Query("Tất cả"),
    target: str = Query("Tất cả"),
    year: str = Query("Tất cả"),
    # ❌ THIẾU: type parameter!
    db: Session = Depends(get_db)
):
    # ... filter logic ...
    if field != "Tất cả":
        query = query.filter(ResearchProject.field == field)
    if target != "Tất cả":
        query = query.filter(ResearchProject.target_audience == target)
    if year != "Tất cả":
        query = query.filter(ResearchProject.year == int(year))
    # ❌ THIẾU: if document_type != "Tất cả": ...
```

#### 🔧 FIX CẦN THỰC HIỆN

**Bước 1: Thêm cột vào Model**
```python
class ResearchProject(Base):
    __tablename__ = "research_projects"
    # (các cột cũ)
    document_type = Column(String)        # NEW: Đề tài/Luận văn/Khóa luận
    implementation_year = Column(Integer) # NEW: năm thực hiện chi tiết
```

**Bước 2: Cập nhật endpoint**
```python
@app.get("/api/v1/projects/search")
def search_projects(
    q: str = Query(""),
    field: str = Query("Tất cả"),
    target: str = Query("Tất cả"),
    year: str = Query("Tất cả"),
    doc_type: str = Query("Tất cả"),  # NEW parameter
    db: Session = Depends(get_db)
):
    # ...existing filters...
    if doc_type != "Tất cả":
        query = query.filter(ResearchProject.document_type == doc_type)
```

**Bước 3: Cập nhật get_filters endpoint**
```python
@app.get("/api/v1/filters")
def get_filters(db: Session = Depends(get_db)):
    # Cập nhật để trả về danh sách document_type
    doc_types = db.query(ResearchProject.document_type).distinct().all()
    return {
        "data": {
            "fields": field_list,
            "years": year_list,
            "audiences": audience_list,
            "doc_types": ["Tất cả"] + [d[0] for d in doc_types if d[0]]  # NEW
        }
    }
```

---

## ✅ PHẦN 2: FRONTEND ANALYSIS

### File: `src/App.tsx` - ENTRY POINT

#### 🟢 ĐIỂM MẠNH
```
✅ Hooks (useSearch, useDebounce) đã tạo tốt
✅ Component composition rõ ràng
✅ SearchBar + SearchFilters layout hợp lý
✅ ProjectCard rendering logic OK
✅ Loading/Error states được xử lý
✅ Responsive grid setup (grid-cols-1 md:grid-cols-3)
```

#### ⚠️ VẤN ĐỀ

**1. Layout thiếu mòn - Không có Topbar/Header/Sidebar**
```jsx
// ❌ HIỆN TẠI: Chi có Header cơ bản
<header className="bg-white border-b border-gray-200 sticky top-0 z-10">
    <div className="flex justify-between items-center h-16">
        <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded-lg...">
        
        # ❌ VẤN ĐỀ: 
        # - Không có Topbar phía trên
        # - Logo + tên khoa layout sai
        # - Navigation menu không có

// ✅ CẦN: Full layout bao gồm:
// ├── Topbar (email, phone, links)
// ├── Header (logo + name + navigation IN HOA)
// └── Main (75-25 grid)
//     ├── Left: Tìm kiếm + Kết quả
//     └── Right: Sidebar (News + Links)
```

**2. SearchBar styling quá "modern" cho phong cách web đại học**
```jsx
// ❌ HIỆN TẠI
<div className="... rounded-xl border-gray-200 focus-within:border-blue-500 ...">
                   ^^^^^^^^ quá tròn (24px)
                              ^^^^^^^^^^^ màu blue generic, không phải xanh VNU

// ✅ CẦN
<div className="... rounded-md border-gray-300 focus-within:border-[#005073] ...">
                   ^^^^^^^^^ góc tối thiểu
                              ^^^^^^^^^^^ xanh VNU 
```

**3. Component Structure - Layout folder trống**
```
vnu-frontend/src/components/
├── Layout/
│   ├── ❌ EMPTY (không có file nào!)
│   ├── Cần: Topbar.tsx
│   ├── Cần: Header.tsx
│   ├── Cần: Navigation.tsx
│   ├── Cần: Sidebar.tsx
│   ├── Cần: MainLayout.tsx
│   └── Cần: SectionTitle.tsx
├── Search/
│   ├── ✅ SearchBar.tsx
│   └── ✅ SearchFilters.tsx
└── ProjectCard.tsx
```

#### 🔧 FIX CẦN THỰC HIỆN

**Thay đổi 1: Cập nhật SearchBar styling**
```tsx
// src/components/Search/SearchBar.tsx
<div className={`relative ${className}`}>
    <div className="flex items-center gap-2 px-4 py-3 bg-white 
                    rounded-md  // ← Đổi từ rounded-xl
                    border border-gray-300  // ← Đổi từ gray-200
                    focus-within:border-[#005073]  // ← Đổi từ blue-500
                    focus-within:ring-[#E8F3FA]  // ← Đổi căn
                    transition-all duration-300 shadow-sm">
```

**Thay đổi 2: Tạo Layout Components**
- `src/components/Layout/Topbar.tsx` - Horizontal bar với contact info
- `src/components/Layout/Header.tsx` - Logo + tên khoa + navigation
- `src/components/Layout/Navigation.tsx` - Menu items (NGHIÊN CỨU, TUYỂN DỤNG, ...)
- `src/components/Layout/Sidebar.tsx` - News + Links sidebar
- `src/components/Layout/MainLayout.tsx` - Wrapper 75-25 grid
- `src/components/Layout/SectionTitle.tsx` - Title with line separator

**Thay đổi 3: Cập nhật App.tsx**
```tsx
// src/App.tsx
import MainLayout from './components/Layout/MainLayout';

function App() {
    return (
        <div className="min-h-screen bg-gray-50 font-sans">
            <MainLayout>
                {/* SearchBar, Filters, Results */}
            </MainLayout>
        </div>
    );
}
```

---

### File: `src/components/Search/SearchBar.tsx`

#### HIỆN TẠI
```tsx
✅ Props structure tốt
✅ Clear button hoạt động
✅ Loading indicator có
✅ Placeholder tiếng Việt đúng
❌ Border radius quá bo tròn (rounded-xl = 24px)
❌ Focus color không phải xanh VNU
❌ Ring color căn không đúng
```

**FIX:** Thay className như trên ↑

---

### File: `src/components/Search/SearchFilters.tsx`

#### HIỆN TẠI
```tsx
✅ 3 dropdown: field, year, audience
✅ Select styling OK
❌ Thiếu dropdown cho document_type (Đề tài/Luận văn/Khóa luận)
❌ Grid layout có thể mất khi thêm filter mới
```

**FIX:** 
```tsx
// Thêm filter mới
<div>
    <label className="block text-sm font-medium text-gray-700 mb-1.5">
        Loại tài liệu
    </label>
    <select
        className="w-full bg-white border border-gray-200 text-gray-700 text-sm rounded-lg..."
        value={filters.docType || 'Tất cả'}
        onChange={(e) => handleChange('docType', e.target.value)}
    >
        {filterOptions.docTypes?.map(dt => (
            <option key={dt} value={dt}>{dt}</option>
        ))}
    </select>
</div>
```

---

### File: `src/hooks/useSearch.ts`

#### HIỆN TẠI
```tsx
✅ Debounce logic tốt (300ms)
✅ Cache handling OK
✅ Loading state đúng
✅ Error handling có sẵn
❌ API call còn đơn giản (chỉ những endpoint cơ bản)
```

**Nhận xét:** Logic này không cần thay đổi, chỉ Backend API cần update thêm parameter `type`

---

## 🔗 INTEGRATION POINTS - FRONTEND & BACKEND

### API Endpoint Mapping

**Hiện tại:**
```
GET /api/v1/projects/search
  Params: q, field, target, year, limit, offset
  Returns: { status, data: { total, items: [] } }

GET /api/v1/filters
  Returns: { status, data: { fields, years, audiences } }

GET /api/v1/projects/{id}
  Returns: { status, data: { chi tiết project } }
```

**Sau khi update:**
```
GET /api/v1/projects/search
  Params: q, field, target, year, doc_type, limit, offset  ← NEW param
  Returns: { status, data: { total, items: [] } }

GET /api/v1/filters
  Returns: { status, data: { fields, years, audiences, doc_types } }  ← NEW field

GET /api/v1/projects/{id}
  Returns: { status, data: { ... document_type, implementation_year } }  ← NEW fields
```

---

## 💾 DATABASE MIGRATION SCRIPT

```sql
-- 1. Thêm cột mới vào bảng research_projects
ALTER TABLE research_projects 
ADD COLUMN document_type VARCHAR(50) DEFAULT 'Đề tài';

ALTER TABLE research_projects 
ADD COLUMN implementation_year INTEGER DEFAULT 2024;

-- 2. Tạo Index để tối ưu query
CREATE INDEX idx_document_type ON research_projects(document_type);

-- 3. Populate dữ liệu mẫu (optional - nếu có seed data)
UPDATE research_projects 
SET document_type = CASE 
    WHEN id LIKE '%thesis%' THEN 'Luận văn'
    WHEN id LIKE '%report%' THEN 'Báo cáo'
    ELSE 'Đề tài'
    END
WHERE document_type IS NULL;
```

---

## 📦 DEPENDENCIES CHECK

### Backend (`requirements.txt`)
```
✅ fastapi - Web framework
✅ uvicorn - ASGI server
✅ sqlalchemy - ORM
✅ psycopg2-binary - PostgreSQL driver
✅ python-multipart - Form data
⚠️ chromadb - AI semantic search (hiện bị comment out)
⚠️ sentence-transformers - Embeddings (hiện bị comment out)
```

**Ghi chú:** AI features bị vô hiệu hóa để Docker nhẹ nhàng, OK cho hiện tại.

### Frontend (`package.json`)
```json
✅ react, react-dom
✅ typescript
✅ vite
✅ tailwindcss
✅ lucide-react (icons)
✅ axios hoặc fetch API
```

**Ghi chú:** Cần kiểm tra xem `httpClient.ts` dùng gì (axios/fetch)

---

## 🎯 TÓM TẮT THAY ĐỔI CẦN THỰC HIỆN

| Loại | Tệp | Thay đổi | Ưu tiên |
|------|-----|---------|--------|
| Backend | `app.py` | Thêm cột `document_type`, `implementation_year` | 🔴 Cao |
| Backend | `app.py` | Update endpoint search thêm filter `type` | 🔴 Cao |
| Backend | SQL Script | Chạy migration script | 🔴 Cao |
| Frontend | `SearchBar.tsx` | Chỉnh màu/corner radius | 🟡 Trung |
| Frontend | `SearchFilters.tsx` | Thêm dropdown `docType` | 🟡 Trung |
| Frontend | Tạo mới | Layout components (Topbar, Header) | 🟡 Trung |
| Frontend | `App.tsx` | Hích hợp MainLayout wrapper | 🟡 Trung |
| Frontend | `useSearch.ts` | (Không cần thay) | ⚪ Thấp |

---

## ✨ CHECKLIST HOÀN THÀNH

- [ ] Backend: Cập nhật Model thêm 2 cột
- [ ] Backend: Cập nhật API endpoint search
- [ ] Backend: Cập nhật get_filters endpoint
- [ ] Backend: Chạy SQL migration
- [ ] Frontend: Tạo Topbar.tsx
- [ ] Frontend: Tạo Header.tsx + Navigation.tsx
- [ ] Frontend: Tạo Sidebar.tsx
- [ ] Frontend: Tạo MainLayout.tsx + SectionTitle.tsx
- [ ] Frontend: Cập nhật SearchBar styling
- [ ] Frontend: Cập nhật SearchFilters thêm docType
- [ ] Frontend: Cập nhật App.tsx
- [ ] Test: API endpoints với Swagger
- [ ] Test: Frontend UI responsive
- [ ] Test: Search functionality với filter mới
- [ ] Demo: Trình bày cho nhóm

---

**Status:** 📍 Sẵn sàng bắt đầu thực hiện!

