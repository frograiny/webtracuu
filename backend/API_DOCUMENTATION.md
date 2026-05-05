# VNU Research API - Documentation

## 📚 Overview

The VNU Research API provides endpoints for searching research projects, user authentication, and admin management. The API uses JWT authentication for protected endpoints.

**Base URL:** `http://localhost:8000/api/v1`

---

## 🔐 Authentication

### JWT Bearer Token

Most endpoints require authentication using JWT tokens. Include the token in the `Authorization` header:

```
Authorization: Bearer {access_token}
```

### Getting a Token

1. **Register a new user:**
   ```
   POST /auth/register
   ```

2. **Login to get a token:**
   ```
   POST /auth/login
   ```

---

## 📋 API Endpoints

### Auth Endpoints

#### Register User
```
POST /auth/register
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "securepassword123"
}

Response (201 Created):
{
  "id": "uuid-string",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "admin" (first user) | "viewer" (subsequent users),
  "is_active": true,
  "created_at": "2026-05-05T10:00:00Z"
}
```

#### Login User
```
POST /auth/login
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "admin",
    "is_active": true
  }
}
```

#### Get Current User
```
GET /auth/me
Authorization: Bearer {access_token}

Response (200 OK):
{
  "id": "uuid-string",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "admin",
  "is_active": true,
  "created_at": "2026-05-05T10:00:00Z"
}
```

#### List Users (Admin Only)
```
GET /auth/users
Authorization: Bearer {admin_token}

Response (200 OK):
{
  "status": "success",
  "data": [
    {
      "id": "uuid-1",
      "email": "admin@example.com",
      "full_name": "Admin User",
      "role": "admin",
      "is_active": true,
      "created_at": "2026-05-05T10:00:00Z"
    },
    {
      "id": "uuid-2",
      "email": "user@example.com",
      "full_name": "Regular User",
      "role": "viewer",
      "is_active": true,
      "created_at": "2026-05-05T10:05:00Z"
    }
  ]
}
```

#### Update User Role (Admin Only)
```
PATCH /auth/users/{user_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

Request:
{
  "role": "admin" | "viewer"
}

Response (200 OK):
{
  "status": "success",
  "data": {
    "id": "uuid-string",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "admin",
    "is_active": true,
    "created_at": "2026-05-05T10:00:00Z"
  }
}
```

#### Deactivate User (Admin Only)
```
PATCH /auth/users/{user_id}/deactivate
Authorization: Bearer {admin_token}

Response (200 OK):
{
  "status": "success",
  "data": {
    "id": "uuid-string",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "viewer",
    "is_active": false,
    "created_at": "2026-05-05T10:00:00Z"
  }
}
```

#### Delete User (Admin Only)
```
DELETE /auth/users/{user_id}
Authorization: Bearer {admin_token}

Response (204 No Content)
```

---

### Project Endpoints

#### Search Projects
```
GET /projects/search?q=keyword&field=Computer%20Science&target=Sinh%20viên&year=2025&type=Thesis&limit=20&offset=0

Query Parameters:
- q (string): Search keyword (optional)
- field (string): Filter by field (default: "Tất cả")
- target (string): Filter by target audience - "Sinh viên", "Giảng viên", "Doanh nghiệp" (default: "Tất cả")
- year (integer): Filter by year (default: "Tất cả")
- type (string): Filter by document type (default: "Tất cả")
- limit (integer): Results per page, max 100 (default: 20)
- offset (integer): Number of results to skip (default: 0)

Response (200 OK):
{
  "status": "success",
  "data": {
    "total": 150,
    "items": [
      {
        "id": "uuid-string",
        "tenDeTai": "Ứng dụng Machine Learning trong Y tế",
        "chuNhiem": "Dr. Nguyễn Văn A",
        "doiTuong": "Sinh viên",
        "linhVuc": "Computer Science",
        "namThucHien": 2025,
        "trangThai": "Hoàn thành",
        "tomTat": "Research abstract...",
        "tuKhoa": ["AI", "Healthcare", "Machine Learning"],
        "loaiTaiLieu": "Thesis",
        "namTrienKhai": 2024
      }
    ]
  }
}
```

#### Get Project Detail
```
GET /projects/{project_id}

Response (200 OK):
{
  "status": "success",
  "data": {
    "id": "uuid-string",
    "tenDeTai": "Ứng dụng Machine Learning trong Y tế",
    "chuNhiem": "Dr. Nguyễn Văn A",
    "doiTuong": "Sinh viên",
    "linhVuc": "Computer Science",
    "namThucHien": 2025,
    "trangThai": "Hoàn thành",
    "tomTat": "Research abstract...",
    "tuKhoa": ["AI", "Healthcare", "Machine Learning"],
    "loaiTaiLieu": "Thesis",
    "namTrienKhai": 2024
  }
}
```

#### Create Project (Admin Only)
```
POST /projects
Authorization: Bearer {admin_token}
Content-Type: application/json

Request:
{
  "tenDeTai": "Ứng dụng AI trong Giáo dục",
  "chuNhiem": "Dr. Nguyễn Văn B",
  "doiTuong": "Giảng viên",
  "linhVuc": "Education Technology",
  "namThucHien": 2026,
  "trangThai": "Đang thực hiện",
  "tomTat": "This project focuses on...",
  "tuKhoa": ["AI", "Education", "Online Learning"],
  "loaiTaiLieu": "Thesis",
  "namTrienKhai": 2025
}

Response (201 Created):
{
  "status": "success",
  "data": {
    "id": "uuid-string",
    "tenDeTai": "Ứng dụng AI trong Giáo dục",
    "chuNhiem": "Dr. Nguyễn Văn B",
    "doiTuong": "Giảng viên",
    "linhVuc": "Education Technology",
    "namThucHien": 2026,
    "trangThai": "Đang thực hiện",
    "tomTat": "This project focuses on...",
    "tuKhoa": ["AI", "Education", "Online Learning"],
    "loaiTaiLieu": "Thesis",
    "namTrienKhai": 2025
  }
}
```

#### Update Project (Admin Only)
```
PUT /projects/{project_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

Request (all fields optional):
{
  "tenDeTai": "Updated Title",
  "chuNhiem": "Dr. Updated Name",
  "doiTuong": "Doanh nghiệp",
  "linhVuc": "Data Science",
  "namThucHien": 2026,
  "trangThai": "Đã nghiệm thu",
  "tomTat": "Updated abstract",
  "tuKhoa": ["Updated", "Keywords"],
  "loaiTaiLieu": "Paper",
  "namTrienKhai": 2026
}

Response (200 OK):
{
  "status": "success",
  "data": { ... updated project data ... }
}
```

#### Delete Project (Admin Only)
```
DELETE /projects/{project_id}
Authorization: Bearer {admin_token}

Response (204 No Content)
```

---

### Filter Endpoints

#### Get Available Filters
```
GET /filters

Response (200 OK):
{
  "status": "success",
  "data": {
    "fields": ["Tất cả", "Computer Science", "Education Technology", "Data Science", ...],
    "years": ["Tất cả", "2026", "2025", "2024", "2023", ...],
    "audiences": ["Tất cả", "Sinh viên", "Giảng viên", "Doanh nghiệp"],
    "documentTypes": ["Tất cả", "Thesis", "Paper", "Research Project", ...]
  }
}
```

---

## ❌ Error Responses

### Validation Error (422)
```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "detail": "Validation failed",
  "errors": [
    {
      "field": "tenDeTai",
      "message": "ensure this value has at least 10 characters"
    }
  ]
}
```

### Unauthorized (401)
```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "detail": "Could not validate credentials"
}
```

### Forbidden (403)
```json
{
  "status": "error",
  "code": "FORBIDDEN",
  "detail": "Chỉ admin có thể tạo đề tài"
}
```

### Not Found (404)
```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "detail": "Không tìm thấy đề tài"
}
```

### Conflict (409)
```json
{
  "status": "error",
  "code": "CONFLICT",
  "detail": "Tiêu đề đề tài đã tồn tại"
}
```

---

## 🔑 Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 422 | Input validation failed |
| `UNAUTHORIZED` | 401 | Authentication required or failed |
| `FORBIDDEN` | 403 | User lacks required permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource already exists (duplicate) |
| `INTERNAL_ERROR` | 500 | Internal server error |

---

## 🧪 Testing with cURL

### 1. Register a user
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "full_name": "Admin User",
    "password": "admin123456"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123456"
  }'
```

### 3. Create a project
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "tenDeTai": "Sample Research Project",
    "chuNhiem": "Dr. John Doe",
    "doiTuong": "Sinh viên",
    "linhVuc": "Computer Science",
    "namThucHien": 2026,
    "trangThai": "Đang thực hiện",
    "tomTat": "This is a sample research project",
    "tuKhoa": ["AI", "ML"],
    "loaiTaiLieu": "Thesis",
    "namTrienKhai": 2025
  }'
```

### 4. Search projects
```bash
curl -X GET "http://localhost:8000/api/v1/projects/search?q=AI&field=Computer%20Science&limit=10&offset=0"
```

---

## 📱 Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "status": "success",
  "data": { ... }
}
```

### Error Response
```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "detail": "Error message"
}
```

---

## 🔒 Authorization Rules

| Endpoint | Public | Viewer | Admin |
|----------|--------|--------|-------|
| `GET /projects/search` | ✅ | ✅ | ✅ |
| `GET /projects/{id}` | ✅ | ✅ | ✅ |
| `POST /projects` | ❌ | ❌ | ✅ |
| `PUT /projects/{id}` | ❌ | ❌ | ✅ |
| `DELETE /projects/{id}` | ❌ | ❌ | ✅ |
| `GET /auth/users` | ❌ | ❌ | ✅ |
| `PATCH /auth/users/{id}` | ❌ | ❌ | ✅ |
| `DELETE /auth/users/{id}` | ❌ | ❌ | ✅ |
| `PATCH /auth/users/{id}/deactivate` | ❌ | ❌ | ✅ |

---

## 📝 Notes

- All dates are in ISO 8601 format with timezone info
- Search results are ranked by relevance
- Pagination is supported via `limit` and `offset` parameters
- The first user registered automatically becomes an admin
- Subsequent users are created with "viewer" role by default
- Only admins can modify the role of other users
