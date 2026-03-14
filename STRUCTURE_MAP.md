# 📊 CẤU TRÚC DỰ ÁN MỚI - VISUAL MAP

**Thời gian:** 15/03/2026  
**Trạng thái:** ✅ RESTRUCTURE COMPLETE

---

## 🗂️ CẤU TRÚC HIỆN TẠI (SAU KHI SỬA)

```
d:\nghich\webtruong/
│
├── 📄 README.md ..................... Project overview (NEW)
├── 📄 docker-compose.yml ........... Docker orchestration (NEW - root level)
├── 📄 .gitignore ................... Git config
│
│
├── 📂 frontend/ .................... FRONTEND APPLICATION
│   └── vnu-frontend/
│       ├── 📄 package.json
│       ├── 📄 vite.config.ts
│       ├── 📄 tsconfig.json
│       ├── 📄 index.html
│       ├── 📄 Dockerfile
│       ├── 📂 public/
│       ├── 📂 dist/                 (build output, gitignored)
│       ├── 📂 node_modules/         (gitignored)
│       │
│       └── 📂 src/ ................. FRONTEND SOURCE
│           ├── 📄 main.tsx ........... Entry point (UPDATED path)
│           │
│           ├── 📂 app/ ............... Application root
│           │   ├── App.tsx .......... Main component (MOVED from root)
│           │   └── App.css .......... Styles (MOVED from root)
│           │
│           ├── 📂 layout/ ........... Layout components (NEW FOLDER)
│           │   ├── Topbar.tsx ....... (TO CREATE)
│           │   ├── Header.tsx ....... (TO CREATE)
│           │   ├── Navigation.tsx ... (TO CREATE)
│           │   ├── Sidebar.tsx ...... (TO CREATE)
│           │   ├── SectionTitle.tsx  (TO CREATE)
│           │   └── MainLayout.tsx ... (TO CREATE)
│           │
│           ├── 📂 components/ ....... Reusable components
│           │   ├── 📂 Search/
│           │   │   ├── SearchBar.tsx
│           │   │   └── SearchFilters.tsx
│           │   └── ProjectCard.tsx
│           │
│           ├── 📂 features/ ......... Feature-specific (EMPTY - NEW)
│           │   └── (folder for future features)
│           │
│           ├── 📂 hooks/ ........... Custom hooks
│           │   ├── useSearch.ts
│           │   └── useDebounce.ts
│           │
│           ├── 📂 services/ ........ API clients
│           │   ├── httpClient.ts
│           │   └── searchService.ts
│           │
│           ├── 📂 types/ .......... TypeScript interfaces
│           │   ├── api.ts
│           │   ├── index.ts
│           │   └── project.ts
│           │
│           ├── 📂 config/ ........ App configuration
│           │   └── theme.config.ts  (TO CREATE)
│           │
│           ├── 📂 utils/ ......... Utility functions
│           │   └── ...
│           │
│           ├── 📂 styles/ ........ Global styles (NEW FOLDER)
│           │   └── index.css ..... (MOVED from root)
│           │
│           ├── 📂 assets/ ....... Images & media
│           │   └── ...
│           │
│           └── (other files)
│
│
├── 📂 backend/ ..................... BACKEND APPLICATION
│   ├── 📄 app.py ................... FastAPI application (MOVED)
│   ├── 📄 requirements.txt ......... Dependencies (MOVED)
│   ├── 📄 test_app.py ............. Tests (MOVED)
│   ├── 📄 test_fastapi.py ......... FastAPI tests (MOVED)
│   ├── 📄 ai_search_api_fixed.py .. AI search (MOVED)
│   ├── 📄 Dockerfile .............. Docker config (MOVED)
│   ├── 📄 docker-compose.yml ...... (backup) (MOVED)
│   ├── 📂 nckh_db/ ................ Database storage
│   │   ├── chroma.sqlite3
│   │   └── (vector db folders)
│   └── 🐘 __pycache__/ ............ Python cache (gitignored)
│
│
├── 📂 huongdan/ ................... DOCUMENTATION & GUIDES
│   ├── 📖 QUICK_SUMMARY.md ....... Quick reference (MOVED)
│   ├── 📖 IMPLEMENTATION_PLAN.md . Step-by-step plan (MOVED)
│   ├── 📖 PROJECT_ASSESSMENT.md . System evaluation (MOVED)
│   ├── 📖 COMPONENT_REFACTORING_PLAN.md . Components guide (MOVED)
│   ├── 📖 CHANGES_FOR_CONSISTENCY.md . Changes log (MOVED)
│   └── 📖 fe.md .................. Frontend requirements (MOVED)
│
│
├── 📂 venv/ ....................... Python virtual environment (gitignored)
│   └── (Python packages)
│
│
└── 📂 .git/ ....................... Git repository
    └── (version control)
```

---

## 🔄 MIGRATION SUMMARY

### ✅ FILES MOVED

| Original Location | New Location | Type |
|------------------|-------------|------|
| `app.py` | `backend/app.py` | Backend |
| `requirements.txt` | `backend/requirements.txt` | Backend config |
| `test_app.py` | `backend/test_app.py` | Backend test |
| `test_fastapi.py` | `backend/test_fastapi.py` | Backend test |
| `ai_search_api_fixed.py` | `backend/ai_search_api_fixed.py` | Backend |
| `Dockerfile` | `backend/Dockerfile` | Docker |
| `docker-compose.yml` | `backend/docker-compose.yml` + `ROOT` | Docker |
| `QUICK_SUMMARY.md` | `huongdan/QUICK_SUMMARY.md` | Guide |
| `IMPLEMENTATION_PLAN.md` | `huongdan/IMPLEMENTATION_PLAN.md` | Guide |
| `PROJECT_ASSESSMENT.md` | `huongdan/PROJECT_ASSESSMENT.md` | Guide |
| `COMPONENT_REFACTORING_PLAN.md` | `huongdan/COMPONENT_REFACTORING_PLAN.md` | Guide |
| `CHANGES_FOR_CONSISTENCY.md` | `huongdan/CHANGES_FOR_CONSISTENCY.md` | Guide |
| `fe.md` | `huongdan/fe.md` | Guide |
| `vnu-frontend/` | `frontend/vnu-frontend/` | Frontend |
| `App.tsx` | `frontend/vnu-frontend/src/app/App.tsx` | Frontend |
| `App.css` | `frontend/vnu-frontend/src/app/App.css` | Frontend |
| `index.css` | `frontend/vnu-frontend/src/styles/index.css` | Frontend |
| `components/Layout/` | `frontend/vnu-frontend/src/layout/` | Frontend |

### ✅ NEW FOLDERS CREATED

| Folder | Purpose |
|--------|---------|
| `frontend/` | Frontend wrapper directory |
| `backend/` | Backend wrapper directory |
| `huongdan/` | Documentation & guides |
| `frontend/vnu-frontend/src/app/` | App entry point |
| `frontend/vnu-frontend/src/styles/` | Global styles |
| `frontend/vnu-frontend/src/layout/` | Layout components |
| `frontend/vnu-frontend/src/features/` | Feature modules (empty, ready for use) |

### ✅ UPDATED PATHS

| File | Old Path | New Path |
|------|----------|----------|
| `main.tsx` | Import from `./index.css` | Import from `./styles/index.css` |
| `main.tsx` | Import from `./App.jsx` | Import from `./app/App.tsx` |
| `App.tsx` | Import components as `./components/...` | Import as `../components/...` |
| `App.tsx` | Import services as `./services/...` | Import as `../services/...` |
| `App.tsx` | Import hooks as `./hooks/...` | Import as `../hooks/...` |
| `App.tsx` | Import types as `./types` | Import as `../types` |

---

## 🎯 ADVANTAGES OF NEW STRUCTURE

### ✅ Organization
- Clean separation: `frontend/` vs `backend/` vs `docs`
- Easy to locate files
- Docker-friendly structure

### ✅ Scalability
- Features folder ready for large applications
- Layout components separated for reusability
- Styles centralized

### ✅ Development
- CI/CD friendly (can build frontend/backend independently)
- Docker Compose at root level for orchestration
- Isolated environments

### ✅ Documentation
- All guides in one place (`huongdan/`)
- Clear README at project root
- Easy onboarding for new developers

### ✅ Prevention of Conflicts
- Separate git folders if needed
- No overlapping file names
- Clear ownership of each module

---

## 🚀 NEXT STEPS

### STEP 1: Verify Structure
```bash
# Check if everything moved correctly
cd d:\nghich\webtruong
dir /s /b
```

### STEP 2: Test Frontend Build
```bash
cd frontend/vnu-frontend
npm install  # Install if needed
npm run build  # Should complete without errors
```

### STEP 3: Test Backend
```bash
cd backend
python app.py  # Should start server
# or
uvicorn app:app --reload --port 8000
```

### STEP 4: Update .gitignore
```
# Ensure these are ignored:
venv/
node_modules/
dist/
__pycache__/
.env
.env.local
```

### STEP 5: Docker Test (Optional)
```bash
docker-compose up -d
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

---

## 📝 IMPORTANT NOTES

✅ **Import Paths Updated** - main.tsx and App.tsx have been updated  
✅ **Structure Complete** - All files organized  
⏭️ **Next: Create Layout Components** - See `huongdan/COMPONENT_REFACTORING_PLAN.md`  
⏭️ **Update Backend Paths** - If any absolute paths in Python code  
⏭️ **Test Build & Runtime** - Both frontend and backend  

---

**Status:** Structure refactoring ✅ COMPLETE  
**Ready for:** Implementation phase  
**Documentation:** See `huongdan/` folder  

