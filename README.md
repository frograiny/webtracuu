# 🎓 VNU Research Portal - Project Structure

Dự án tìm kiếm NCKH của Đại học Quốc gia Hà Nội

## 📁 Cấu Trúc Thư Mục

```
d:\nghich\webtruong/
│
├── 📂 frontend/                      Frontend Application (React + Vite)
│   └── vnu-frontend/
│       ├── src/
│       │   ├── app/                 Application entry point
│       │   │   ├── App.tsx
│       │   │   ├── App.css
│       │   │   └── main.tsx
│       │   │
│       │   ├── layout/              Layout components
│       │   │   ├── Topbar.tsx       (NEW - to create)
│       │   │   ├── Header.tsx       (NEW - to create)
│       │   │   ├── Navigation.tsx   (NEW - to create)
│       │   │   ├── SectionTitle.tsx (NEW - to create)
│       │   │   ├── Sidebar.tsx      (NEW - to create)
│       │   │   └── MainLayout.tsx   (NEW - to create)
│       │   │
│       │   ├── components/          Reusable components
│       │   │   ├── Search/
│       │   │   │   ├── SearchBar.tsx
│       │   │   │   └── SearchFilters.tsx
│       │   │   └── ProjectCard.tsx
│       │   │
│       │   ├── features/            Feature-specific components
│       │   │   ├── ... (for future features)
│       │   │   └── ...
│       │   │
│       │   ├── hooks/               Custom React hooks
│       │   │   ├── useSearch.ts
│       │   │   └── useDebounce.ts
│       │   │
│       │   ├── services/            API & external services
│       │   │   ├── httpClient.ts
│       │   │   └── searchService.ts
│       │   │
│       │   ├── types/               TypeScript interfaces
│       │   │   ├── api.ts
│       │   │   ├── index.ts
│       │   │   └── project.ts
│       │   │
│       │   ├── config/              Application config
│       │   │   └── theme.config.ts  (NEW - to create)
│       │   │
│       │   ├── utils/               Utility functions
│       │   │   └── ... (helpers)
│       │   │
│       │   ├── styles/              Global styles
│       │   │   └── index.css
│       │   │
│       │   ├── assets/              Images, fonts, etc
│       │   │   └── ...
│       │   │
│       │   └── index.html
│       │
│       ├── package.json
│       ├── vite.config.ts
│       ├── tsconfig.json
│       └── Dockerfile
│
├── 📂 backend/                       Backend Application (Python/FastAPI)
│   ├── app.py                       Main FastAPI application
│   ├── requirements.txt             Python dependencies
│   ├── test_app.py                  Tests for API
│   ├── test_fastapi.py              FastAPI tests
│   ├── ai_search_api_fixed.py       AI search implementation
│   ├── Dockerfile                   Docker configuration
│   ├── docker-compose.yml           (moved here)
│   └── nckh_db/                     Local database
│
├── 📂 huongdan/                      Documentation & Guides
│   ├── QUICK_SUMMARY.md             Quick overview
│   ├── IMPLEMENTATION_PLAN.md       Implementation checklist
│   ├── PROJECT_ASSESSMENT.md        Project evaluation
│   ├── COMPONENT_REFACTORING_PLAN.md Component structure guide
│   ├── CHANGES_FOR_CONSISTENCY.md   Changes log
│   └── fe.md                        Frontend description
│
├── 📂 venv/                         Python virtual environment (ignore in git)
│
├── docker-compose.yml               Docker compose (root level)
├── .gitignore                       Git ignore rules
└── README.md                        This file
```

---

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
# or
uvicorn app:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend/vnu-frontend
npm install
npm run dev
# Runs at http://localhost:5173
```

### 3. Using Docker Compose (both)
```bash
docker-compose up -d
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

---

## 📋 Thay Đổi Cấu Trúc (Breaking Changes)

### Đường dẫn cũ vs mới:
```
OLD:
└── app.py                          → NEW: backend/app.py
└── requirements.txt                → NEW: backend/requirements.txt
└── Dockerfile                      → NEW: backend/Dockerfile
└── docker-compose.yml              → NEW: backend/docker-compose.yml
│                                   → NEW: docker-compose.yml (root)
└── vnu-frontend/src/App.tsx        → NEW: frontend/vnu-frontend/src/app/App.tsx
└── vnu-frontend/src/App.css        → NEW: frontend/vnu-frontend/src/app/App.css
└── vnu-frontend/src/index.css      → NEW: frontend/vnu-frontend/src/styles/index.css
└── vnu-frontend/src/components/Layout/ → NEW: frontend/vnu-frontend/src/layout/
└── *.md files                      → NEW: huongdan/*.md
```

---

## ⚠️ Files Cần Update Sau Restructure

### Backend Files
- [ ] `backend/app.py` - Update database path references if needed
- [ ] Environment variables (Docker): DATABASE_URL paths

### Frontend Files
- [ ] `frontend/vnu-frontend/vite.config.ts` - Verify paths
- [ ] `frontend/vnu-frontend/src/app/App.tsx` - Update import paths
- [ ] `frontend/vnu-frontend/src/main.tsx` - Ensure it imports from new paths

### Git Configuration
- [ ] Update `.gitignore` to include new structure
- [ ] Ensure `nckh_db/` is in backend folder & gitignored

---

## 📚 Documentation Location

All official documentation has been moved to `huongdan/` directory:
- `📖 QUICK_SUMMARY.md` - Start here!
- `📖 IMPLEMENTATION_PLAN.md` - Step-by-step guide
- `📖 PROJECT_ASSESSMENT.md` - System evaluation
- `📖 COMPONENT_REFACTORING_PLAN.md` - Component creation guide
- `📖 CHANGES_FOR_CONSISTENCY.md` - Changes log
- `📖 fe.md` - Frontend requirements

---

## ✅ Benefits of New Structure

1. ✅ **Separation of Concerns** - Backend and Frontend clearly separated
2. ✅ **Scalability** - Easy to add new features in separate folders
3. ✅ **Maintainability** - Clear folder hierarchy
4. ✅ **Consistency** - Matches industry standards (Angular, React patterns)
5. ✅ **Documentation** - All guides in one place
6. ✅ **Docker Ready** - Easy orchestration with docker-compose

---

## 🔄 Next Steps

1. ✅ **Structure Refactor** - COMPLETED
2. ⏭️ **Update Import Paths** - Update all relative paths in code
3. ⏭️ **Test Build** - `npm run build` in frontend
4. ⏭️ **Test Backend** - `python backend/app.py`
5. ⏭️ **Docker Test** - `docker-compose up`
6. ⏭️ **Feature Implementation** - Start with frontend layout components

---

**Last Updated:** March 15, 2026  
**Status:** ✨ Structure Ready for Development
