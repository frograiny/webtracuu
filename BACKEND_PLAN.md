# 📋 Kế Hoạch Hoàn Thành Backend API

## 🎯 Mục Tiêu
Hoàn thành 100% Backend API với đầy đủ CRUD operations và quản lý người dùng cho admin.

---

## 📊 Tình Trạng Hiện Tại
- ✅ Authentication (JWT, login, register)
- ✅ Search API (advanced token scoring)
- ✅ Filters API
- ❌ **CRUD Operations** (tạo, sửa, xóa project)
- ❌ **Admin endpoints** (list projects)
- ❌ **Role-based access control**
- ❌ **Comprehensive error handling**

---

## 🚀 Giai Đoạn 1: Core CRUD Endpoints (1-2 ngày)

### Task 1.1: Thêm Permission & RBAC Decorators
**File:** `backend/app/core/security.py`
- [ ] Tạo decorator `@admin_required` để check role = "admin"
- [ ] Tạo decorator `@viewer_required` để check role = "viewer"
- [ ] Hàm helper check admin access

**Output:**
```python
@router.post("/projects")
@admin_required
def create_project(...):
    pass
```

### Task 1.2: Schema cho CRUD
**File:** `backend/app/schemas/project.py`
- [ ] Thêm `ProjectCreate` schema (input từ frontend)
- [ ] Thêm `ProjectUpdate` schema (update từ frontend)
- [ ] Thêm `ProjectListResponse` (list projects)

**Fields cần:**
```python
class ProjectCreate(BaseModel):
    title: str
    author: str
    target_audience: str
    field: str
    year: int
    status: str
    abstract: str
    keywords: list[str]
    document_type: str
    implementation_year: int
```

### Task 1.3: CRUD Endpoints trong Search Router
**File:** `backend/app/api/v1/search.py`

#### ✏️ Endpoint 1: CREATE Project
```
POST /api/v1/projects
Headers: Authorization: Bearer {token}
Body: ProjectCreate
Response: ProjectDetailResponse
```
- Validate input
- Check admin role
- Insert vào database
- Return project details

#### ✏️ Endpoint 2: LIST Projects (Admin Only)
```
GET /api/v1/projects
Headers: Authorization: Bearer {token}
Query: limit=20, offset=0, target_audience=...
Response: SearchResponse (list)
```
- Check admin role
- Return toàn bộ projects

#### ✏️ Endpoint 3: GET Project Detail
```
GET /api/v1/projects/{id}
Response: ProjectDetailResponse
```
- Fetch by ID
- No auth required (public)

#### ✏️ Endpoint 4: UPDATE Project
```
PUT /api/v1/projects/{id}
Headers: Authorization: Bearer {token}
Body: ProjectUpdate
Response: ProjectDetailResponse
```
- Validate input
- Check admin role
- Update database
- Return updated project

#### ✏️ Endpoint 5: DELETE Project
```
DELETE /api/v1/projects/{id}
Headers: Authorization: Bearer {token}
Response: {"status": "success", "message": "Project deleted"}
```
- Check admin role
- Delete from database
- Return success

---

## 🛡️ Giai Đoạn 2: Error Handling & Validation (1 ngày)

### Task 2.1: Custom Exception Classes
**File:** `backend/app/core/exceptions.py` (NEW)
- [ ] `ValidationError` - input validation failed
- [ ] `NotFoundError` - resource not found
- [ ] `UnauthorizedError` - auth failed
- [ ] `ForbiddenError` - permission denied
- [ ] `ConflictError` - duplicate resource

### Task 2.2: Error Response Handler
**File:** `backend/app/core/exceptions.py`
- [ ] Exception handler middleware trong main.py
- [ ] Format consistent error responses:
```python
{
    "status": "error",
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "details": {...}
}
```

### Task 2.3: Input Validation
**File:** `backend/app/api/v1/search.py`
- [ ] Validate ProjectCreate
  - title: min 10 chars, max 500
  - author: min 3 chars, max 200
  - year: 2000-2030
  - abstract: max 2000
- [ ] Validate ProjectUpdate (same as create)
- [ ] Catch duplicate titles

---

## 📝 Giai Đoạn 3: User Management Endpoints (1 ngày)

### Task 3.1: Thêm User Endpoints
**File:** `backend/app/api/v1/auth.py`

#### ✏️ Endpoint 1: LIST Users (Admin Only)
```
GET /api/v1/auth/users
Headers: Authorization: Bearer {token}
Response: [UserRead, ...]
```

#### ✏️ Endpoint 2: UPDATE User Role (Admin Only)
```
PATCH /api/v1/auth/users/{user_id}
Body: {"role": "admin" | "viewer"}
Response: UserRead
```

#### ✏️ Endpoint 3: DELETE User (Admin Only)
```
DELETE /api/v1/auth/users/{user_id}
Response: {"status": "success"}
```

#### ✏️ Endpoint 4: DEACTIVATE User (Admin Only)
```
PATCH /api/v1/auth/users/{user_id}/deactivate
Response: UserRead
```

---

## 🧪 Giai Đoạn 4: Testing & Documentation (1 ngày)

### Task 4.1: Tester Endpoints với curl/Postman
- [ ] Test toàn bộ 5 CRUD endpoints
- [ ] Test auth (success/fail)
- [ ] Test validation errors
- [ ] Test pagination

### Task 4.2: Postman Collection
**File:** `backend/postman_collection.json`
- [ ] Export collection từ Postman
- [ ] Include auth flow
- [ ] Environment variables (base_url, token)

### Task 4.3: API Documentation
**File:** `backend/API_DOCUMENTATION.md`
- [ ] List tất cả endpoints
- [ ] Request/response examples
- [ ] Error codes reference
- [ ] Authentication flow

---

## 📂 File Structure Sau Khi Hoàn Thành

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          (updated: user endpoints)
│   │       ├── filters.py       (unchanged)
│   │       └── search.py        (updated: CRUD endpoints)
│   ├── core/
│   │   ├── config.py            (unchanged)
│   │   ├── exceptions.py        (NEW: custom exceptions)
│   │   ├── security.py          (updated: RBAC decorators)
│   │   └── ...
│   ├── models/
│   │   ├── project.py           (unchanged)
│   │   └── user.py              (unchanged)
│   ├── schemas/
│   │   ├── auth.py              (unchanged)
│   │   └── project.py           (updated: CRUD schemas)
│   └── main.py                  (updated: exception handlers)
├── tests/
│   ├── test_auth.py             (NEW)
│   ├── test_projects.py         (NEW)
│   └── test_crud.py             (NEW)
├── postman_collection.json      (NEW)
├── API_DOCUMENTATION.md         (NEW)
└── requirements.txt             (unchanged)
```

---

## ✅ Checklist Chi Tiết

### Phase 1: RBAC & Schemas
- [ ] Task 1.1: RBAC decorators
  - [ ] `@admin_required` decorator
  - [ ] `@viewer_required` decorator
  - [ ] Helper functions

- [ ] Task 1.2: CRUD Schemas
  - [ ] ProjectCreate
  - [ ] ProjectUpdate
  - [ ] ProjectListResponse

- [ ] Task 1.3: CRUD Endpoints
  - [ ] POST /api/v1/projects (create)
  - [ ] GET /api/v1/projects (list admin)
  - [ ] GET /api/v1/projects/{id} (detail)
  - [ ] PUT /api/v1/projects/{id} (update)
  - [ ] DELETE /api/v1/projects/{id} (delete)

### Phase 2: Error Handling
- [ ] Task 2.1: Exception Classes
  - [ ] Custom exception types
  - [ ] Exception mapping

- [ ] Task 2.2: Error Handler
  - [ ] Middleware setup
  - [ ] Error response format

- [ ] Task 2.3: Input Validation
  - [ ] ProjectCreate validation
  - [ ] ProjectUpdate validation
  - [ ] Duplicate check

### Phase 3: User Management
- [ ] Task 3.1: User Endpoints
  - [ ] GET /api/v1/auth/users (list)
  - [ ] PATCH /api/v1/auth/users/{id} (update role)
  - [ ] DELETE /api/v1/auth/users/{id}
  - [ ] PATCH /api/v1/auth/users/{id}/deactivate

### Phase 4: Testing & Docs
- [ ] Task 4.1: Manual Testing
- [ ] Task 4.2: Postman Collection
- [ ] Task 4.3: API Documentation

---

## 📌 Lưu Ý Quan Trọng

1. **Authentication Check:** Mỗi endpoint CRUD phải check token (except GET detail)
2. **Authorization Check:** Admin-only endpoints phải check role = "admin"
3. **Input Validation:** Tất cả inputs phải validate trước khi save
4. **Error Messages:** Tiếng Anh thân thiện (vì frontend dùng)
5. **Database Transactions:** Update/Delete nên dùng transaction
6. **Soft Delete:** Có thể implement soft delete cho projects sau

---

## ⏱️ Timeline Ước Tính

| Giai Đoạn | Task | Giờ | Ngày |
|-----------|------|-----|------|
| 1 | RBAC + Schemas | 2h | Ngày 1 |
| 1 | CRUD Endpoints | 4h | Ngày 1-2 |
| 2 | Error Handling | 3h | Ngày 2 |
| 3 | User Management | 2h | Ngày 2-3 |
| 4 | Testing + Docs | 2h | Ngày 3 |
| **TOTAL** | | **13h** | **3 ngày** |

---

## 🎬 Bước Tiếp Theo

1. ✅ Review kế hoạch này
2. ⏳ Chúng ta bắt đầu Task 1.1 (RBAC decorators)
3. → Task 1.2 (Schemas)
4. → Task 1.3 (CRUD Endpoints)
5. ... Và cứ tiếp tục

**Sẵn sàng bắt đầu?** 🚀
