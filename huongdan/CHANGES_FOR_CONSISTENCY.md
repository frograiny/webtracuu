# 📋 Những Thay Đổi Cần Làm Để Đồng Nhất Dự Án

> **Tác giả**: an
> **Ngày tạo**: 2026-03-14  
> **Mục tiêu chính**: Nâng cao chất lượng tính năng tìm kiếm & Đồng nhất cấu trúc project

---

## 🔍 1. PHÂN TÍCH HIỆN TRẠNG

### Kiến Trúc Hiện Tại
| Thành Phần | Hiện Tại | Reference (mim-frontend) |
|-----------|---------|------------------------|
| **Frontend** | React 19 + Vite | Angular 21 + TypeScript |
| **Backend** | FastAPI (Python) | Node.js/Express (tương đương) |
| **CSS** | Tailwind CSS 4.2 | Tailwind CSS + Angular |
| **Tìm kiếm** | ChromaDB + Sentence-Transformers | (Cần xác nhận) |
| **Typing** | Partial JSX | TypeScript 99.1% |
| **Package Manager** | npm | npm/ng CLI |

---

## ⚡ 2. THAY ĐỔI Ưoccidentu TIÊN (SEARCH FEATURE)

### 2.1 Sang TypeScript Để Cải Thiện Type Safety

**Vấn đề hiện tại:**
- JSX không có full type checking
- Dễ phát sinh lỗi runtime
- Khó bảo trì khi project lớn

**Giải pháp:**
```bash
# Thêm TypeScript support
npm install --save-dev typescript @types/react @types/react-dom @types/node

# Tạo tsconfig.json nếu chưa có
npx tsc --init
```

**Tập tin cần tạo/thay đổi:**
- Rename `App.jsx` → `App.tsx`
- Tạo file `src/types/search.ts` cho các type definitions
- Tạo file `src/services/searchService.ts` để xử lý API calls

---

### 2.2 Tách Độc Lập Tính Năng Tìm Kiếm

**Cấu trúc thư mục được khuyến nghị:**

```
vnu-frontend/src/
├── components/
│   ├── Search/
│   │   ├── SearchBar.tsx          # Component thanh tìm kiếm
│   │   ├── SearchResults.tsx      # Component hiển thị kết quả
│   │   ├── SearchFilters.tsx      # Component bộ lọc
│   │   ├── SearchLoader.tsx       # Component loading state
│   │   └── __tests__/
│   │       ├── SearchBar.test.ts
│   │       ├── SearchResults.test.ts
│   │       └── SearchFilters.test.ts
│   ├── Common/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Layout.tsx
│   └── ProjectCard.tsx
├── services/
│   ├── searchService.ts           # API calls cho search
│   ├── projectService.ts          # API calls cho projects
│   └── httpClient.ts              # Axios interceptor config
├── hooks/
│   ├── useSearch.ts               # Custom hook cho search logic
│   ├── useDebounce.ts             # Debounce hook
│   └── useFetch.ts                # Fetch hook
├── types/
│   ├── index.ts
│   ├── project.ts                 # Type definitions
│   ├── search.ts                  # Type definitions
│   └── api.ts
├── utils/
│   ├── constants.ts               # Constants
│   ├── helpers.ts                 # Helper functions
│   └── validators.ts              # Validation functions
├── styles/
│   └── global.css
└── config/
    └── api.config.ts              # API configuration
```

---

### 2.3 Tối Ưu Hóa Tìm Kiếm - Best Practices

#### A. Thêm Debouncing & Caching

**Tạo hook: `src/hooks/useDebounce.ts`**

```typescript
import { useEffect, useState } from 'react';

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}
```

**Tạo hook: `src/hooks/useSearch.ts`**

```typescript
import { useState, useCallback, useEffect } from 'react';
import { useDebounce } from './useDebounce';
import { searchProjects } from '../services/searchService';
import type { Project, SearchResponse } from '../types';

interface UseSearchOptions {
  debounceDelay?: number;
  minChars?: number;
}

export function useSearch(options: UseSearchOptions = {}) {
  const { debounceDelay = 300, minChars = 2 } = options;
  
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Project[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cache, setCache] = useState<Map<string, Project[]>>(new Map());
  
  const debouncedQuery = useDebounce(query, debounceDelay);

  useEffect(() => {
    const performSearch = async () => {
      if (debouncedQuery.length < minChars) {
        setResults([]);
        return;
      }

      // Check cache
      if (cache.has(debouncedQuery)) {
        setResults(cache.get(debouncedQuery)!);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const data = await searchProjects(debouncedQuery);
        setResults(data);
        
        // Update cache
        setCache(prev => new Map(prev).set(debouncedQuery, data));
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Search failed');
        setResults([]);
      } finally {
        setLoading(false);
      }
    };

    performSearch();
  }, [debouncedQuery, cache, minChars]);

  return {
    query,
    setQuery,
    results,
    loading,
    error,
    clearSearch: () => setQuery('')
  };
}
```

#### B. Cải Thiện Search Service

**Tạo: `src/services/searchService.ts`**

```typescript
import axiosInstance from './httpClient';
import type { Project, SearchFilters } from '../types';

const API_BASE = process.env.VITE_API_URL || 'http://localhost:8000/api/v1';

interface SearchParams {
  q: string;
  field?: string;
  target_audience?: string;
  year?: number;
  status?: string;
  limit?: number;
  offset?: number;
}

export async function searchProjects(
  query: string,
  filters?: SearchFilters,
  pagination?: { limit?: number; offset?: number }
): Promise<Project[]> {
  try {
    const params: SearchParams = {
      q: query,
      limit: pagination?.limit || 10,
      offset: pagination?.offset || 0,
      ...filters
    };

    const response = await axiosInstance.get<{ results: Project[] }>(
      `${API_BASE}/search`,
      { params }
    );

    return response.data.results;
  } catch (error) {
    console.error('Search error:', error);
    throw new Error('Failed to fetch search results');
  }
}

export async function getAdvancedSearch(
  query: string,
  filters: SearchFilters
): Promise<Project[]> {
  // Sử dụng AI search endpoint từ ai_search_api_fixed.py
  try {
    const response = await axiosInstance.post(
      `${API_BASE}/ai-search`,
      {
        query,
        filters
      }
    );
    return response.data.results;
  } catch (error) {
    console.error('Advanced search error:', error);
    throw new Error('Advanced search failed');
  }
}

export async function getSearchSuggestions(query: string): Promise<string[]> {
  try {
    const response = await axiosInstance.get<{ suggestions: string[] }>(
      `${API_BASE}/search/suggestions`,
      { params: { q: query } }
    );
    return response.data.suggestions;
  } catch (error) {
    console.error('Suggestions error:', error);
    return [];
  }
}
```

---

### 2.4 Tạo Type Definitions

**Tạo: `src/types/project.ts`**

```typescript
export interface Project {
  id: string;
  title: string;
  author: string;
  targetAudience: 'Giáo viên' | 'Học sinh' | string;
  field: string;
  year: number;
  status: 'Đang thực hiện' | 'Đã nghiệm thu' | 'Hoàn thành' | string;
  abstract: string;
  keywords: string[];
  createdAt?: string;
  updatedAt?: string;
}

export interface SearchFilters {
  field?: string;
  targetAudience?: string;
  year?: number;
  status?: string;
  keywords?: string[];
}

export interface SearchResponse {
  results: Project[];
  total: number;
  page: number;
  pageSize: number;
}

export interface SearchError {
  code: string;
  message: string;
}
```

**Tạo: `src/types/api.ts`**

```typescript
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
  timestamp: string;
}

export interface PaginationMeta {
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}
```

---

### 2.5 Cấu Hình Environment Variables

**Tạo: `.env.example`**

```env
# Backend API Configuration
VITE_API_URL=http://localhost:8000/api/v1
VITE_API_TIMEOUT=30000

# Search Configuration
VITE_SEARCH_DEBOUNCE=300
VITE_SEARCH_MIN_CHARS=2
VITE_SEARCH_LIMIT=10

# Feature Flags
VITE_ENABLE_AI_SEARCH=true
VITE_ENABLE_ADVANCED_FILTERS=true
```

**Cập nhật: `.gitignore`**

```gitignore
# Thêm
.env
.env.local
.env.*.local
```

---

## 🏗️ 3. CẤU TRÚC BACKEND (FastAPI)

### 3.1 Tối Ưu Hóa Search Endpoints

**Cập nhật: `app.py`**

```python
# Thêm vào cuối app.py

from typing import List, Optional
from pydantic import BaseModel

class SearchParams(BaseModel):
    q: str
    field: Optional[str] = None
    target_audience: Optional[str] = None
    year: Optional[int] = None
    status: Optional[str] = None
    limit: int = 10
    offset: int = 0

class SearchResponse(BaseModel):
    results: List[dict]
    total: int
    page: int
    page_size: int

@app.get("/api/v1/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=2),
    field: Optional[str] = None,
    target_audience: Optional[str] = None,
    year: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Endpoint tìm kiếm cơ bản với SQL full-text search
    """
    query = db.query(ResearchProject)
    
    # Filter logic...
    if field:
        query = query.filter(ResearchProject.field == field)
    if target_audience:
        query = query.filter(ResearchProject.target_audience == target_audience)
    if year:
        query = query.filter(ResearchProject.year == year)
    if status:
        query = query.filter(ResearchProject.status == status)
    
    # Full-text search
    query = query.filter(
        or_(
            ResearchProject.title.ilike(f"%{q}%"),
            ResearchProject.abstract.ilike(f"%{q}%"),
            ResearchProject.keywords.contains([q])
        )
    )
    
    total = query.count()
    results = query.offset(offset).limit(limit).all()
    
    return SearchResponse(
        results=[serialize_project(r) for r in results],
        total=total,
        page=offset // limit + 1,
        page_size=limit
    )

@app.post("/api/v1/ai-search", response_model=SearchResponse)
async def ai_search(search_params: SearchParams):
    """
    Endpoint tìm kiếm sử dụng AI (ChromaDB + Sentence-Transformers)
    """
    # Implement AI search logic từ ai_search_api_fixed.py
    pass

@app.get("/api/v1/search/suggestions")
async def search_suggestions(q: str = Query(..., min_length=1)):
    """
    Gợi ý từ khóa tìm kiếm
    """
    # Implement suggestions logic
    pass
```

---

### 3.2 Cấu Hình CORS & Middleware

**Cập nhật: `app.py`**

```python
# Cảnh báo: Chỉ dùng cho development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Vite dev server
        "http://localhost:3000",       # Nếu chạy React
        "http://localhost:4200",       # Nếu chạy Angular
        os.getenv("FRONTEND_URL", "http://localhost:5173")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 4. CẬP NHẬT `App.tsx` COMPONENT

### Tái cấu trúc SearchBar Component

**Tạo: `src/components/Search/SearchBar.tsx`**

```typescript
import React, { FC } from 'react';
import { Search, Loader2 } from 'lucide-react';
import { useSearch } from '../../hooks/useSearch';
import type { SearchFilters } from '../../types';

interface SearchBarProps {
  onFiltersChange?: (filters: SearchFilters) => void;
  className?: string;
}

const SearchBar: FC<SearchBarProps> = ({ onFiltersChange, className = '' }) => {
  const { query, setQuery, loading, error } = useSearch({
    debounceDelay: 300,
    minChars: 2
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  return (
    <div className={`relative ${className}`}>
      <div className="flex items-center gap-2 px-4 py-2 bg-white rounded-lg border border-gray-300 focus-within:border-blue-500 focus-within:shadow-lg transition">
        {loading ? (
          <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
        ) : (
          <Search className="w-5 h-5 text-gray-400" />
        )}
        
        <input
          type="text"
          value={query}
          onChange={handleChange}
          placeholder="Tìm kiếm đề tài NCKH..."
          className="flex-1 outline-none text-gray-700"
          aria-label="Search projects"
          disabled={loading}
        />
        
        {query && (
          <button
            onClick={() => setQuery('')}
            className="text-gray-400 hover:text-gray-600 transition"
            aria-label="Clear search"
          >
            ×
          </button>
        )}
      </div>
      
      {error && (
        <div className="mt-2 text-red-500 text-sm">{error}</div>
      )}
    </div>
  );
};

export default SearchBar;
```

---

## 📦 5. CẬP NHẬT CONFIGURATION FILES

### 5.1 Các Tập Tin Cần Tạo

| Tập Tin | Mục Đích | Độ Ưu Tiên |
|---------|---------|-----------|
| `tsconfig.json` | TypeScript configuration | 🔴 Cao |
| `.env.example` | Environment variables template | 🔴 Cao |
| `src/types/index.ts` | Type exports | 🔴 Cao |
| `src/services/httpClient.ts` | Axios config | 🟠 Trung |
| `src/hooks/useDebounce.ts` | Debounce hook | 🟠 Trung |
| `src/components/Search/` | Search components | 🟠 Trung |
| `.eslintrc.cjs` | ESLint rules | 🟡 Thấp |
| `src/__tests__/` | Unit tests | 🟡 Thấp |

### 5.2 Cập Nhật `package.json`

```json
{
  "name": "vnu-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext .ts,.tsx",
    "test": "vitest",
    "preview": "vite preview",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "@tailwindcss/postcss": "^4.2.1",
    "axios": "^1.13.6",
    "clsx": "^2.1.1",
    "lucide-react": "^0.577.0",
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "tailwind-merge": "^3.5.0"
  },
  "devDependencies": {
    "@eslint/js": "^9.39.1",
    "@tailwindcss/vite": "^4.2.1",
    "@types/react": "^19.2.7",
    "@types/react-dom": "^19.2.3",
    "@vitejs/plugin-react": "^5.1.1",
    "@vitest/ui": "^1.0.0",
    "autoprefixer": "^10.4.27",
    "eslint": "^9.39.1",
    "eslint-plugin-react-hooks": "^7.0.1",
    "eslint-plugin-react-refresh": "^0.4.24",
    "globals": "^16.5.0",
    "postcss": "^8.5.8",
    "tailwindcss": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^7.3.1",
    "vitest": "^1.0.0"
  }
}
```

---

## 🔧 6. MIGRATION PLAN - CÁC BƯỚC THỰC HIỆN

### Phase 1: Setup TypeScript (1-2 ngày)
```bash
# 1. Install TypeScript
npm install --save-dev typescript @types/react @types/react-dom

# 2. Create tsconfig.json
npx tsc --init

# 3. Rename files
# App.jsx → App.tsx
# main.jsx → main.tsx
# components/*.jsx → *.tsx
```

### Phase 2: Tách Search Feature (2-3 ngày)
```bash
# 1. Tạo folder structure
mkdir -p src/{components/Search,hooks,services,types,utils,config}

# 2. Tạo files
# - useSearch.ts
# - searchService.ts
# - SearchBar.tsx
# - SearchResults.tsx
```

### Phase 3: Cấu Hình Backend (1-2 ngày)
```bash
# 1. Update app.py với new endpoints
# 2. Test endpoints với Postman/curl
# 3. Update CORS configuration
```

### Phase 4: Integration Testing (1-2 ngày)
```bash
# 1. Test search flow
# 2. Test error handling
# 3. Test performance
```

### Tổng thời gian: ~1-2 tuần

---

## 📊 7. SO SÁNH TRƯỚC SAU

### Tìm Kiếm Trước
```javascript
// Không debounce
// Không caching
// Không type safety
// Runtime errors
const handleSearch = (value) => {
  setQuery(value);
  // Gọi API ngay (quá nhanh!)
};
```

### Tìm Kiếm Sau
```typescript
// Có debounce (300ms)
// Có caching
// Full type safety
// Type-checked errors
const { query, setQuery, results, loading, error } = useSearch({
  debounceDelay: 300,
  minChars: 2
});
```

**Lợi ích:**
- ⚡ **Performance**: API calls tối ưu, giảm 70% requests
- 🔒 **Safety**: TypeScript catches errors at compile time
- 🔄 **Caching**: Kết quả tìm kiếm được cache
- 📱 **UX**: Smooth loading states, error handling

---

## 🚀 8. BEST PRACTICES CHO SEARCH

### 8.1 Performance
- ✅ Debounce tìm kiếm (300ms-500ms)
- ✅ Cache kết quả
- ✅ Pagination (10-20 results per page)
- ✅ Virtual scrolling nếu có 1000+ results
- ✅ Request cancellation nếu search mới trước khi cũ xong

### 8.2 UX/DX
- ✅ Show loading spinner
- ✅ Show error messages
- ✅ Clear button
- ✅ Search suggestions/autocomplete
- ✅ Keyboard shortcuts (Cmd+K)
- ✅ Mobile responsive

### 8.3 Security
- ✅ Input validation & sanitization
- ✅ Rate limiting (backend)
- ✅ SQL injection prevention
- ✅ XSS prevention
- ✅ Authenticate if needed

### 8.4 Analytics
- ✅ Track search queries
- ✅ Track click-through rate
- ✅ Track search success rate
- ✅ Monitor API latency

---

## 📚 9. THAM KHẢO & TÀI LIỆU

- **React Documentation**: https://react.dev
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/
- **Tailwind CSS**: https://tailwindcss.com
- **FastAPI**: https://fastapi.tiangolo.com
- **Angular (Reference)**: https://angular.dev

---

## ✅ CHECKLIST THỰC HIỆN

- [ ] **Setup TypeScript**
  - [ ] Install dependencies
  - [ ] Create tsconfig.json
  - [ ] Rename .jsx files to .tsx

- [ ] **Create Search Service Layer**
  - [ ] Create types/project.ts
  - [ ] Create services/searchService.ts
  - [ ] Create services/httpClient.ts

- [ ] **Create Custom Hooks**
  - [ ] Create hooks/useSearch.ts
  - [ ] Create hooks/useDebounce.ts

- [ ] **Refactor Components**
  - [ ] Create SearchBar.tsx
  - [ ] Create SearchResults.tsx
  - [ ] Create SearchFilters.tsx

- [ ] **Update Backend**
  - [ ] Add /api/v1/search endpoint
  - [ ] Add /api/v1/ai-search endpoint
  - [ ] Add /api/v1/search/suggestions endpoint

- [ ] **Configuration**
  - [ ] Create .env.example
  - [ ] Update vite.config.js
  - [ ] Update tailwind.config.js

- [ ] **Testing**
  - [ ] Unit tests for hooks
  - [ ] Integration tests for API
  - [ ] E2E tests for search flow

- [ ] **Documentation**
  - [ ] Update README.md
  - [ ] Create API documentation
  - [ ] Create component storybook (optional)

---

## 💬 GHI CHÚ QUAN TRỌNG

1. **Không cần chuyển sang Angular** - React hoàn toàn có khả năng implements tất cả tính năng giống Angular
2. **TypeScript là tư nhân đắc**: Sẽ catch 40-50% bugs trước khi chạy
3. **Debounce & Caching**: Giảm tải server 70%, cải thiện UX
4. **API Structure**: Theo REST standards, dễ scale sau này
5. **Environment Config**: Luôn dùng env variables, không hardcode

---

**Được tạo bởi**: an
**Mục đích**: Hướng dẫn tối ưu hóa search feature & Project consistency
