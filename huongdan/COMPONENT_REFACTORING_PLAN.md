# 📁 REFACTORING CẤU TRÚC THÀNH PHẦN (COMPONENTS STRUCTURE)

**Mục đích:** Hướng dẫn tạo/sửa file để phù hợp với layout mới

---

## 🎨 LAYOUT MỚI - VISUAL STRUCTURE

```
┌──────────────────────────────────────────────────────────┐
│ TOPBAR: Số điện thoại | Email | Links nội bộ            │ (new)
├──────────────────────────────────────────────────────────┤
│ HEADER:                                                  │ (update)
│ ┌─────────────────┐  ┌────────────────────────────────┐  │
│ │ Logo + Tên Khoa │  │ NGHIÊN CỨU  TUYỂN DỤNG  ĐÀO TẠO │  │
│ │ (VN + EN)       │  │ ĐỨC HỌC  LIÊN HỆ              │  │
│ └─────────────────┘  └────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  MAIN CONTENT (75-25 Grid Layout)                        │
│  ┌──────────────────────┐  ┌──────────────────────────┐  │
│  │  COLUMN LEFT (75%)   │  │  SIDEBAR RIGHT (25%)     │  │
│  │                      │  │                          │  │
│  │ | NGHIÊN CỨU KH      │  │ 📢 BẢNG TIN KHOA         │  │
│  │                      │  │ ┌────────────────────┐   │  │
│  │ [SearchBar]          │  │ │ Tin 1 - 15/03/2026 │   │  │
│  │                      │  │ │ Tin 2 - 14/03/2026 │   │  │
│  │ [SearchFilters: vvv] │  │ │ Tin 3 - 13/03/2026 │   │  │
│  │                      │  │ └────────────────────┘   │  │
│  │ Kết quả tìm kiếm:    │  │                          │  │
│  │ ┌─────────────────┐  │  │ 🔗 LIÊN KẾT NGOÀI        │  │
│  │ │ Project Card 1  │  │  │ • Website chính         │  │
│  │ ├─────────────────┤  │  │ • Student Forum         │  │
│  │ │ Project Card 2  │  │  │ • Email Support         │  │
│  │ ├─────────────────┤  │  │                          │  │
│  │ │ Project Card 3  │  │  │                          │  │
│  │ └─────────────────┘  │  │                          │  │
│  │                      │  │                          │  │
│  └──────────────────────┘  └──────────────────────────┘  │
└──────────────────────────────────────────────────────────┘

Footer: (optional)
```

---

## 📂 FILE STRUCTURE - FRONTEND

### Hiện tại (TRƯỚC)
```
src/
├── App.tsx
├── main.tsx
├── App.css
├── index.css
├── components/
│   ├── Layout/          ← ❌ EMPTY FOLDER!
│   ├── Search/
│   │   ├── SearchBar.tsx        (✅ OK)
│   │   └── SearchFilters.tsx    (✅ OK)
│   └── ProjectCard.tsx          (✅ OK)
├── hooks/
│   ├── useSearch.ts  (✅ OK)
│   └── useDebounce.ts  (✅ OK)
├── services/
│   ├── httpClient.ts  (✅ OK)
│   └── searchService.ts  (✅ OK)
├── types/
│   ├── api.ts
│   ├── index.ts
│   └── project.ts
└── config/
```

### Sau khi cải thiện (SAU)
```
src/
├── App.tsx                          (UPDATE: wrap with MainLayout)
├── main.tsx
├── App.css
├── index.css
├── components/
│   ├── Layout/                      ← 🟢 TẠOCODE MỚI
│   │   ├── Topbar.tsx              (NEW)
│   │   ├── Header.tsx              (NEW)
│   │   ├── Navigation.tsx          (NEW - Component con trong Header)
│   │   ├── Sidebar.tsx             (NEW)
│   │   ├── SectionTitle.tsx        (NEW - Title với line separator)
│   │   ├── MainLayout.tsx          (NEW - Wrapper chính)
│   │   └── Layout.css              (NEW - styles riêng nếu cần)
│   ├── Search/
│   │   ├── SearchBar.tsx           (UPDATE: styling)
│   │   └── SearchFilters.tsx       (UPDATE: thêm docType filter)
│   └── ProjectCard.tsx             (KEEP: không thay)
├── hooks/
│   ├── useSearch.ts                (KEEP)
│   └── useDebounce.ts              (KEEP)
├── services/
│   ├── httpClient.ts               (KEEP)
│   └── searchService.ts            (KEEP)
├── types/
│   ├── api.ts
│   ├── index.ts
│   └── project.ts
└── config/
    └── theme.config.ts             (NEW - VNU colors constants)
```

---

## 🔧 COMPONENT DETAILS - PHẢI TẠOARE

### 1️⃣ `Topbar.tsx` - Thanh ngang trên cùng
```tsx
// src/components/Layout/Topbar.tsx

interface TopbarProps {
  phone?: string;
  email?: string;
  internalLinks?: { label: string; href: string }[];
}

export const Topbar: FC<TopbarProps> = ({
  phone = "+84 (0)2 3629-1111",
  email = "info@vnu.edu.vn",
  internalLinks = [
    { label: "Portal", href: "#" },
    { label: "Mail", href: "#" },
    { label: "Library", href: "#" }
  ]
}) => {
  return (
    <div className="bg-gray-800 text-white text-sm py-2 px-4">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="flex gap-6">
          <span>📞 {phone}</span>
          <span>📧 {email}</span>
        </div>
        <div className="flex gap-4">
          {internalLinks.map(link => (
            <a key={link.label} href={link.href} className="hover:underline">
              {link.label}
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};
```

---

### 2️⃣ `Header.tsx` - Logo + Tên + Menu
```tsx
// src/components/Layout/Header.tsx

export const Header: FC = () => {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          
          {/* LEFT: Logo + Tên Khoa */}
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-[#005073] rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">VNU</span>
            </div>
            <div>
              <h1 className="font-bold text-lg text-gray-900">
                Khoa Công Nghệ Thông Tin
              </h1>
              <p className="text-sm text-gray-600">
                School of Information Technology
              </p>
            </div>
          </div>

          {/* RIGHT: Navigation Menu */}
          <Navigation />
          
        </div>
      </div>
    </header>
  );
};
```

---

### 3️⃣ `Navigation.tsx` - Menu phía trên
```tsx
// src/components/Layout/Navigation.tsx

const menuItems = [
  { label: "NGHIÊN CỨU", href: "#research" },
  { label: "TUYỂN DỤNG", href: "#recruitment" },
  { label: "ĐÀO TẠO", href: "#education" },
  { label: "ĐỨC HỌC", href: "#ethics" },
  { label: "LIÊN HỆ", href: "#contact" }
];

export const Navigation: FC = () => {
  return (
    <nav className="flex gap-8">
      {menuItems.map(item => (
        <a
          key={item.label}
          href={item.href}
          className="font-bold text-sm text-gray-900 hover:text-[#005073] transition-colors"
        >
          {item.label}
        </a>
      ))}
    </nav>
  );
};
```

---

### 4️⃣ `SectionTitle.tsx` - Title với line separator
```tsx
// src/components/Layout/SectionTitle.tsx

interface SectionTitleProps {
  title: string;
  subtitle?: string;
}

export const SectionTitle: FC<SectionTitleProps> = ({ title, subtitle }) => {
  return (
    <div className="mb-6">
      <div className="flex items-center gap-3">
        <div className="w-1 h-8 bg-[#005073] rounded-full"></div>
        <h2 className="text-2xl font-bold text-gray-900">
          {title}
        </h2>
      </div>
      {subtitle && (
        <p className="text-gray-600 mt-2">{subtitle}</p>
      )}
    </div>
  );
};
```

---

### 5️⃣ `Sidebar.tsx` - News + Links
```tsx
// src/components/Layout/Sidebar.tsx

const mockNews = [
  { id: 1, title: "Thông báo tuyển sinh 2025", date: "15/03/2026" },
  { id: 2, title: "Kết quả học bổng các nước", date: "14/03/2026" },
  { id: 3, title: "Seminar về AI trong giáo dục", date: "13/03/2026" }
];

const mockLinks = [
  { label: "Website chính của trường", href: "#" },
  { label: "Thư viện điện tử", href: "#" },
  { label: "Trang e-Learning", href: "#" }
];

export const Sidebar: FC = () => {
  return (
    <aside className="space-y-6">
      {/* Section 1: News */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h3 className="font-bold text-lg text-gray-900 mb-4">📢 BẢNG TIN KHOA</h3>
        <ul className="space-y-3">
          {mockNews.map(item => (
            <li key={item.id} className="border-b pb-2">
              <a href="#" className="hover:text-[#005073] transition-colors">
                <p className="text-sm font-medium text-gray-700">{item.title}</p>
                <p className="text-xs text-gray-500">{item.date}</p>
              </a>
            </li>
          ))}
        </ul>
      </div>

      {/* Section 2: Links */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h3 className="font-bold text-lg text-gray-900 mb-4">🔗 LIÊN KẾT NGOÀI</h3>
        <ul className="space-y-2">
          {mockLinks.map((link, idx) => (
            <li key={idx}>
              <a 
                href={link.href} 
                className="text-sm text-[#005073] hover:underline block"
              >
                → {link.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
};
```

---

### 6️⃣ `MainLayout.tsx` - Wrapper 75-25 Grid
```tsx
// src/components/Layout/MainLayout.tsx

interface MainLayoutProps {
  children: React.ReactNode;
}

export const MainLayout: FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* Topbar */}
      <Topbar />
      
      {/* Header */}
      <Header />
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          
          {/* LEFT: Main content (75%) */}
          <div className="lg:col-span-3">
            <SectionTitle title="NGHIÊN CỨU KHOA HỌC" />
            {children}
          </div>
          
          {/* RIGHT: Sidebar (25%) */}
          <div className="lg:col-span-1">
            <Sidebar />
          </div>
          
        </div>
      </main>
      
      {/* Footer (optional) */}
      <footer className="bg-gray-900 text-white py-4 text-center mt-8">
        <p>© 2026 Khoa Công Nghệ Thông Tin - Đại học Quốc gia Hà Nội</p>
      </footer>
    </div>
  );
};
```

---

### 7️⃣ `SearchBar.tsx` - STYLING UPDATE

```tsx
// src/components/Search/SearchBar.tsx - CHỈNH SỬA

// ❌ CŨ: rounded-xl border-gray-200 focus:border-blue-500
// ✅ MỚI: 

<div className={`relative ${className}`}>
    <div className="flex items-center gap-2 px-4 py-3 bg-white 
                    rounded-md
                    border border-gray-300 
                    focus-within:border-[#005073]
                    focus-within:ring-2 
                    focus-within:ring-[#E8F3FA]
                    transition-all duration-300 
                    shadow-sm">
        {/* ... rest stays same ... */}
    </div>
</div>
```

---

## 🎨 COLOR CONSTANTS - THEME CONFIG

```tsx
// src/config/theme.config.ts

export const VNU_COLORS = {
  primary: "#005073",           // Xanh chính
  primaryLight: "#E8F3FA",      // Xanh nhạt (focus ring)
  secondary: "#2C3E50",         // Xám đậm (topbar)
  
  text: {
    dark: "#1F2937",           // Chữ chính
    light: "#6B7280",          // Chữ phụ
  },
  
  border: {
    light: "#E5E7EB",          // Border nhạt
    medium: "#D1D5DB",         // Border trung bình
  },
  
  bg: {
    white: "#FFFFFF",
    gray: "#F9FAFB",
  }
};

// Tailwind config mapping
export const tailwindConfig = {
  colors: {
    vnu: {
      primary: VNU_COLORS.primary,
      'primary-light': VNU_COLORS.primaryLight,
    }
  }
};
```

---

## 📝 APP.TSX UPDATE

```tsx
// src/App.tsx - CHỈNH SỬA

import React, { useState, useEffect } from 'react';
import { MainLayout } from './components/Layout/MainLayout';  // NEW
import { SearchBar } from './components/Search/SearchBar';
import { SearchFiltersArea } from './components/Search/SearchFilters';
import { ProjectCard } from './components/ProjectCard';
import { useSearch } from './hooks/useSearch';
import { getFiltersData } from './services/searchService';
import type { SearchFilters } from './types';
import './App.css';

function App() {
  const [filters, setFilters] = useState<SearchFilters>({});
  const [filterOptions, setFilterOptions] = useState({ 
    fields: [], 
    years: [], 
    audiences: [],
    docTypes: []  // NEW
  });

  const { query, setQuery, results, loading, error } = useSearch(filters);

  useEffect(() => {
    const fetchFilters = async () => {
      const data = await getFiltersData();
      setFilterOptions(data);
    };
    fetchFilters();
  }, []);

  return (
    <MainLayout>  {/* NEW: Wrap everything */}
      {/* Tìm kiếm */}
      <SearchBar
        query={query}
        setQuery={setQuery}
        loading={loading}
        className="mb-8"
      />

      {/* Bộ lọc */}
      <SearchFiltersArea
        filters={filters}
        setFilters={setFilters}
        filterOptions={filterOptions}
      />

      {/* Kết quả */}
      <div className="mt-8">
        {error && (
          <div className="p-4 bg-red-50 text-red-600 rounded-lg mb-6">
            Có lỗi xảy ra trong quá trình tìm kiếm
          </div>
        )}
        
        <div className="grid grid-cols-1 gap-4">
          {results.map(item => (
            <ProjectCard key={item.id} project={item} />
          ))}
        </div>
      </div>
    </MainLayout>  {/* NEW */}
  );
}

export default App;
```

---

## ✅ IMPORT STATEMENTS - PHẢI THÊM

```tsx
// src/components/Layout/index.ts (NEW - export all Layout components)
export { Topbar } from './Topbar';
export { Header } from './Header';
export { Navigation } from './Navigation';
export { Sidebar } from './Sidebar';
export { SectionTitle } from './SectionTitle';
export { MainLayout } from './MainLayout';

// Usage trong App.tsx
import { MainLayout } from './components/Layout';
```

---

## 📋 TODO CHECKLIST

Components cần tạo/sửa:

- [ ] Tạo `/src/components/Layout/Topbar.tsx`
- [ ] Tạo `/src/components/Layout/Header.tsx`
- [ ] Tạo `/src/components/Layout/Navigation.tsx`
- [ ] Tạo `/src/components/Layout/Sidebar.tsx`
- [ ] Tạo `/src/components/Layout/SectionTitle.tsx`
- [ ] Tạo `/src/components/Layout/MainLayout.tsx`
- [ ] Tạo `/src/components/Layout/index.ts` (exports)
- [ ] Tạo `/src/config/theme.config.ts` (colors)
- [ ] Sửa `/src/components/Search/SearchBar.tsx` (styling)
- [ ] Sửa `/src/components/Search/SearchFilters.tsx` (thêm docType)
- [ ] Sửa `/src/App.tsx` (wrap with MainLayout)
- [ ] Test responsive design
- [ ] Build & deploy test

---

**Tiếp theo:** Chọn bắt đầu từ Backend (SQL + API) hay Frontend (Layout) trước?
