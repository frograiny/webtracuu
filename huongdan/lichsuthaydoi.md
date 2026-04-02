--- CẬP NHẬT MỚI NHẤT ---

commit (chưa commit)
Date:   Wed Apr 2 20:45:00 2026 +0700

    fix: Hỗ trợ tìm kiếm tiếng Việt không dấu (unaccent search)

    Vấn đề: Khi gõ tiếng Việt không dấu (vd: "vat lieu", "nguyen van an"),
    hệ thống FTS không trả về kết quả vì to_tsvector('simple') chỉ so khớp
    chính xác ký tự — 'vat' ≠ 'vật'.

    Giải pháp: Thêm cơ chế tìm kiếm 2 tầng:
    - Tầng 1: Giữ nguyên FTS cho trường hợp gõ đúng dấu (nhanh, có ranking)
    - Tầng 2 (fallback): Khi FTS không có kết quả, dùng ILIKE + translate()
      để bỏ dấu tiếng Việt ở CẢ phía SQL (translate()) và Python (unicodedata)
      rồi so khớp. KHÔNG cần cài Extension, KHÔNG cần thay đổi schema DB.

    Kỹ thuật dùng:
    - Python: unicodedata.normalize('NFD') + lọc combining characters
    - SQL: PostgreSQL translate() với bảng mapping 89 ký tự VN có dấu → không dấu
    - Logic AND: tất cả từ khóa đều phải khớp để tránh kết quả nhiễu

 backend/app/api/v1/search.py | 94 +++++++++++++++++++++++++++++++++++++++----
 1 file changed, 86 insertions(+), 8 deletions(-)

---

commit 6b0b7714e2b3eaec84320d66aff2c717de2da42f
Author: TruongAn <truongan1203.hp@gmail.com>
Date:   Tue Mar 17 19:38:45 2026 +0700

    chore: ignore vite_log.txt


 .gitignore | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)

commit 4c81030a63151f6f5f3ef4a43ed675f2c69e347e
Author: TruongAn <truongan1203.hp@gmail.com>
Date:   Tue Mar 17 19:24:05 2026 +0700

    Fix linting and typing issues in backend and frontend

 backend/alembic/env.py                                    | 12 ++++++------
 backend/app/api/v1/filters.py                             |  4 ++--
 backend/app/api/v1/search.py                              |  4 ++--
 frontend/vnu-frontend/src/app/core/services/httpClient.ts |  1 +
 4 files changed, 11 insertions(+), 10 deletions(-)

commit 3592bf6f5aab20b5330c680198414ce4354a96ff
Author: TruongAn <truongan1203.hp@gmail.com>
Date:   Tue Mar 17 19:21:12 2026 +0700

    Remove redundant vnu-frontend root directory

 vnu-frontend/package-lock.json | 6 ------
 1 file changed, 6 deletions(-)

commit de71d2871cbf44c2affdf9e443104e691e3f94cc
Author: TruongAn <truongan1203.hp@gmail.com>
Date:   Tue Mar 17 13:33:11 2026 +0700

    Refactor backend to modular architecture with config and Alembic

 backend/Dockerfile                                 |  31 +-
 backend/ai_search_api_fixed.py                     | 134 ------
 backend/alembic.ini                                | 149 ++++++
 backend/alembic/README                             |   1 +
 backend/alembic/env.py                             |  85 ++++
 backend/alembic/script.py.mako                     |  28 ++
 .../versions/c27d480ad638_initial_schema.py        |  32 ++
 backend/app.py                                     | 518 ---------------------
 backend/app/__init__.py                            |   0
 backend/app/api/__init__.py                        |   0
 backend/app/api/v1/__init__.py                     |   0
 backend/app/api/v1/filters.py                      |  30 ++
 backend/app/api/v1/search.py                       |  95 ++++
 backend/app/core/__init__.py                       |   0
 backend/app/core/config.py                         |   9 +
 backend/app/db/__init__.py                         |   0
 backend/app/db/session.py                          |  14 +
 backend/app/main.py                                |  32 ++
 backend/app/models/__init__.py                     |   0
 backend/app/models/project.py                      |  17 +
 backend/requirements.txt                           |   4 +
 backend/{ => scripts}/check_db.py                  |   8 +-
 backend/{ => scripts}/recreate_db.py               |   0
 backend/scripts/seed_data.py                       |  56 +++
 huongdan/baocao_refactor.md                        |  32 ++
 25 files changed, 614 insertions(+), 661 deletions(-)

commit d74e57b44b506e0f7c05f7f50d12772bee397410
Author: TruongAn <truongan1203.hp@gmail.com>
Date:   Mon Mar 16 18:22:26 2026 +0700

    Disable AI Semantic Search to save system memory

 ResearchProjectDemo.jsx        | 2 ++
 backend/ai_search_api_fixed.py | 2 +-
 2 files changed, 3 insertions(+), 1 deletion(-)

commit 32795b5e09500dda1672f31f897b9d6a51646737
Author: TruongAn <truongan1203.hp@gmail.com>
Date:   Mon Mar 16 18:11:46 2026 +0700

    Fix type checking errors in Python backend files

 backend/ai_search_api_fixed.py                     | 21 ++++-----
 backend/app.py                                     | 35 ++++++++-------
 backend/check_db.py                                | 20 +++++++++
 backend/recreate_db.py                             | 10 +++++
 .../src/app/core/services/httpClient.ts            |  2 +-
 huongdan/BaocaoWeb.md                              | 20 +++++++++
 huongdan/baocao.md                                 | 52 ++++++++++++++++++++++
 package-lock.json                                  |  6 +++
 8 files changed, 138 insertions(+), 28 deletions(-)

commit 09576ce6b482604f205ccda59cb85d232d822df4
Author: TruongAn <truongan1203.hp@gmail.com>
Date:   Sun Mar 15 22:04:19 2026 +0700

    X├│a test files & cß║¡p nhß║¡t webtracuu theo y├¬u cß║ºu HUS

 backend/test_app.py     | Bin 34 -> 0 bytes
 backend/test_fastapi.py |   8 --------
 2 files changed, 8 deletions(-)

commit aee3ada74583cfa2a9a3e2bed0b9eec8094c09ba
Author: TruongAn <email@domain.com>
Date:   Sun Mar 15 20:30:13 2026 +0700

    docs: Add REFACTORED_STRUCTURE.md explaining new Angular-style folder organization

 huongdan/REFACTORED_STRUCTURE.md | 147 +++++++++++++++++++++++++++++++++++++++
 1 file changed, 147 insertions(+)

commit df940f83575170cee82339eda48e54597c942751
Author: TruongAn <email@domain.com>
Date:   Sun Mar 15 20:29:18 2026 +0700

    refactor: Restructure frontend to Angular-style folder organization
    
    - Reorganize src/app with core/services, shared/components/hooks/types, features/search, and layouts
    - Update all import paths to match new structure
    - Move components: ProjectCard (shared), SearchBar/SearchFilters (features/search)
    - Move services to core/services, hooks to shared/hooks, types to shared/types
    - Move layouts (Header, MainLayout, Topbar) to app/layouts
    - Remove old flat folder structure (components/, services/, hooks/, types/, layout/)
    - Build passes successfully with new structure

 frontend/vnu-frontend/src/app/App.tsx                      | 14 +++++++-------
 .../vnu-frontend/src/{ => app/core}/services/httpClient.ts |  0
 .../src/{ => app/core}/services/searchService.ts           |  2 +-
 .../features/search/components}/SearchBar.tsx              |  2 +-
 .../features/search/components}/SearchFilters.tsx          |  2 +-
 .../vnu-frontend/src/{layout => app/layouts}/Header.tsx    |  0
 .../src/{layout => app/layouts}/MainLayout.tsx             |  0
 .../vnu-frontend/src/{layout => app/layouts}/Topbar.tsx    |  0
 .../src/{ => app/shared}/components/ProjectCard.tsx        |  2 +-
 .../vnu-frontend/src/{ => app/shared}/hooks/useDebounce.ts |  0
 .../vnu-frontend/src/{ => app/shared}/hooks/useSearch.ts   |  2 +-
 frontend/vnu-frontend/src/{ => app/shared}/types/api.ts    |  0
 frontend/vnu-frontend/src/{ => app/shared}/types/index.ts  |  0
 .../vnu-frontend/src/{ => app/shared}/types/project.ts     |  0
 14 files changed, 12 insertions(+), 12 deletions(-)

commit 3902c2a681b2dc18683b6cd2e1cfcbb5154c7792
Author: truon <email@domain.com>
Date:   Sun Mar 15 13:12:57 2026 +0700

    Update project structure and components - push to GitHub

 backend/app.py                                     | 26 +++++++++--
 frontend/vnu-frontend/src/app/App.tsx              | 53 ++++++++--------------
 .../src/components/Search/SearchBar.tsx            | 29 +++++++++---
 frontend/vnu-frontend/src/layout/Header.tsx        | 33 ++++++++++++++
 frontend/vnu-frontend/src/layout/MainLayout.tsx    | 48 ++++++++++++++++++++
 frontend/vnu-frontend/src/layout/Topbar.tsx        | 20 ++++++++
 .../vnu-frontend/src/services/searchService.ts     |  4 ++
 frontend/vnu-frontend/src/types/project.ts         |  2 +
 huongdan/AUTOMATION_MAINTENANCE.md                 | 24 ++++++++++
 .../RESTRUCTURE_COMPLETE.md                        |  0
 STRUCTURE_MAP.md => huongdan/STRUCTURE_MAP.md      |  0
 vnu-frontend/package-lock.json                     |  6 +++
 12 files changed, 199 insertions(+), 46 deletions(-)

commit f3eadcfe840dde9a96724fe96ca7564b995bdb08
Author: truon <email@domain.com>
Date:   Sun Mar 15 00:41:48 2026 +0700

    refactor: restructure project with industry-standard layout
    
    - Reorganize backend files to backend/ folder (Python - FastAPI)
    - Reorganize frontend to frontend/vnu-frontend (React-Vite)
    - Separate documentation to huongdan/ folder
    - Create modular folder structure: app/, layout/, features/, styles/
    - Update import paths for frontend (React - Vite structure)
    - Create comprehensive documentation (README.md, STRUCTURE_MAP.md)
    - Add root-level docker-compose.yml for orchestration
    - Update .gitignore for new structure
    - Prevent file conflicts and improve maintainability

 .gitignore                                         |  68 +-
 README.md                                          | 195 ++++++
 RESTRUCTURE_COMPLETE.md                            | 244 +++++++
 STRUCTURE_MAP.md                                   | 250 +++++++
 backend/Dockerfile                                 |  22 +
 .../ai_search_api_fixed.py                         |   0
 app.py => backend/app.py                           |  19 +-
 backend/docker-compose.yml                         |  51 ++
 backend/requirements.txt                           |   6 +
 test_app.py => backend/test_app.py                 | Bin
 test_fastapi.py => backend/test_fastapi.py         |   0
 docker-compose.yml                                 |  54 ++
 {vnu-frontend => frontend/vnu-frontend}/.gitignore |   0
 {vnu-frontend => frontend/vnu-frontend}/README.md  |   0
 .../vnu-frontend}/eslint.config.js                 |   0
 {vnu-frontend => frontend/vnu-frontend}/index.html |   2 +-
 .../vnu-frontend}/package-lock.json                |  35 +-
 .../vnu-frontend}/package.json                     |   4 +-
 .../vnu-frontend}/public/vite.svg                  |   0
 .../src => frontend/vnu-frontend/src/app}/App.css  |   0
 frontend/vnu-frontend/src/app/App.tsx              | 103 +++
 .../vnu-frontend}/src/assets/react.svg             |   0
 .../vnu-frontend/src/components/ProjectCard.tsx    |  67 ++
 .../src/components/Search/SearchBar.tsx            |  41 ++
 .../src/components/Search/SearchFilters.tsx        |  64 ++
 frontend/vnu-frontend/src/hooks/useDebounce.ts     |  15 +
 frontend/vnu-frontend/src/hooks/useSearch.ts       |  77 ++
 .../main.jsx => frontend/vnu-frontend/src/main.tsx |   4 +-
 frontend/vnu-frontend/src/services/httpClient.ts   |  13 +
 .../vnu-frontend/src/services/searchService.ts     |  69 ++
 .../vnu-frontend/src/styles}/index.css             |   0
 frontend/vnu-frontend/src/types/api.ts             |  13 +
 frontend/vnu-frontend/src/types/index.ts           |   2 +
 frontend/vnu-frontend/src/types/project.ts         |  37 +
 frontend/vnu-frontend/tsconfig.json                |  25 +
 frontend/vnu-frontend/tsconfig.node.json           |  12 +
 .../vnu-frontend/vite.config.ts                    |   0
 huongdan/CHANGES_FOR_CONSISTENCY.md                | 774 +++++++++++++++++++++
 huongdan/COMPONENT_REFACTORING_PLAN.md             | 528 ++++++++++++++
 huongdan/IMPLEMENTATION_PLAN.md                    | 295 ++++++++
 huongdan/PROJECT_ASSESSMENT.md                     | 436 ++++++++++++
 huongdan/QUICK_SUMMARY.md                          | 201 ++++++
 huongdan/fe.md                                     |  31 +
 vnu-frontend/src/App.jsx                           | 548 ---------------
 44 files changed, 3733 insertions(+), 572 deletions(-)

commit 37dbb353bcfaa84b2b9ec6156ce317c99a291fae
Author: truon <email@domain.com>
Date:   Thu Mar 12 15:27:48 2026 +0700

    chore: update gitignore

 .gitignore | 7 +++++++
 1 file changed, 7 insertions(+)

commit e93dfff69632d37d23067705c064d186aef019e1
Author: truon <email@domain.com>
Date:   Thu Mar 12 15:10:08 2026 +0700

    feat: integrate ai semantic search and add react frontend

 .gitignore                        |   17 +
 __pycache__/app.cpython-313.pyc   |  Bin 17209 -> 18348 bytes
 ai_search_api_fixed.py            |  133 ++
 app.py                            |  131 +-
 nckh_db/chroma.sqlite3            |  Bin 188416 -> 0 bytes
 test_app.py                       |  Bin 0 -> 34 bytes
 test_fastapi.py                   |    8 +
 vnu-frontend/.gitignore           |   24 +
 vnu-frontend/README.md            |   16 +
 vnu-frontend/eslint.config.js     |   29 +
 vnu-frontend/index.html           |   13 +
 vnu-frontend/package-lock.json    | 3882 +++++++++++++++++++++++++++++++++++++
 vnu-frontend/package.json         |   36 +
 vnu-frontend/public/vite.svg      |    1 +
 vnu-frontend/src/App.css          |   42 +
 vnu-frontend/src/App.jsx          |  548 ++++++
 vnu-frontend/src/assets/react.svg |    1 +
 vnu-frontend/src/index.css        |    1 +
 vnu-frontend/src/main.jsx         |   10 +
 vnu-frontend/vite.config.js       |    8 +
 20 files changed, 4837 insertions(+), 63 deletions(-)

commit 483b29818a07e50d5cf865ce7081dcae7224fbbb
Author: truon <email@domain.com>
Date:   Wed Mar 11 21:25:27 2026 +0700

    Refresh: Ensure all files are pushed

commit dadd664501f5e8ce94b83a62593e627be20808eb
Author: truon <email@domain.com>
Date:   Wed Mar 11 20:45:52 2026 +0700

    Initial commit: Add project files

 ResearchProjectDemo.jsx         | 548 ++++++++++++++++++++++++++++++++++++++++
 __pycache__/app.cpython-313.pyc | Bin 0 -> 17209 bytes
 app.py                          | 495 ++++++++++++++++++++++++++++++++++++
 nckh_db/chroma.sqlite3          | Bin 0 -> 188416 bytes
 4 files changed, 1043 insertions(+)
