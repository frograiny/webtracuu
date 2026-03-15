# 📁 Project Structure Refactoring - Angular-Style Organization

## Overview
Project đã được refactor theo cấu trúc **Angular-style** (giống mim-frontend) để tăng scalability, maintainability và consistency.

## New Structure

```
frontend/vnu-frontend/src/
├── app/
│   ├── core/                    # Core services & utilities
│   │   └── services/
│   │       ├── httpClient.ts    # Axios instance config
│   │       └── searchService.ts # Search API calls
│   │
│   ├── shared/                  # Shared/reusable across app
│   │   ├── components/
│   │   │   └── ProjectCard.tsx
│   │   ├── hooks/
│   │   │   ├── useDebounce.ts
│   │   │   └── useSearch.ts
│   │   ├── types/
│   │   │   ├── api.ts
│   │   │   ├── index.ts
│   │   │   └── project.ts
│   │   └── utils/               # Shared utilities
│   │
│   ├── features/                # Feature-specific modules
│   │   └── search/
│   │       └── components/
│   │           ├── SearchBar.tsx
│   │           └── SearchFilters.tsx
│   │
│   ├── layouts/                 # Layout components
│   │   ├── Header.tsx
│   │   ├── MainLayout.tsx
│   │   └── Topbar.tsx
│   │
│   ├── App.tsx                  # Main app component
│   └── App.css
│
├── assets/                      # Static assets
├── config/                      # Config files
├── styles/                      # Global styles
└── main.tsx
```

## Old Structure (Deprecated)
```
frontend/vnu-frontend/src/
├── components/                  ❌ REMOVED
├── services/                    ❌ REMOVED
├── hooks/                       ❌ REMOVED
├── types/                       ❌ REMOVED
├── layout/                      ❌ REMOVED
├── features/                    ❌ REMOVED (old)
└── utils/                       ❌ REMOVED (old)
```

## Key Changes

| Old Path | New Path | Purpose |
|----------|----------|---------|
| `services/` | `app/core/services/` | Core business logic (API calls) |
| `hooks/` | `app/shared/hooks/` | Shared/reusable React hooks |
| `types/` | `app/shared/types/` | TypeScript type definitions |
| `components/ProjectCard.tsx` | `app/shared/components/ProjectCard.tsx` | Reusable component |
| `components/Search/` | `app/features/search/components/` | Feature-specific components |
| `layout/` | `app/layouts/` | Layout wrappers |

## Benefits

✅ **Scalability**: Clear separation of concerns makes it easy to add new features
✅ **Maintainability**: Consistent folder structure reduces cognitive load
✅ **Reusability**: `shared/` folder clearly shows what can be reused across features
✅ **Feature Isolation**: Each feature has its own folder under `features/`
✅ **Consistency**: Matches industry standard (similar to Angular, NestJS patterns)
✅ **Professional Structure**: Comparable to mim-frontend project architecture

## Import Path Changes

All imports have been updated to reflect new paths. Examples:

```typescript
// OLD
import { SearchBar } from '../components/Search/SearchBar';
import { useSearch } from '../hooks/useSearch';
import { searchProjects } from '../services/searchService';
import type { SearchFilters } from '../types';

// NEW
import { SearchBar } from './features/search/components/SearchBar';
import { useSearch } from './shared/hooks/useSearch';
import { searchProjects } from './core/services/searchService';
import type { SearchFilters } from './shared/types';
```

## Build Status

✅ **Build passes successfully** - All imports resolved correctly
✅ **No runtime errors** - Structure validated through build process
✅ **Ready for development** - Use `npm run dev` to start

## Next Steps

### To extend this structure:

1. **Add new features**: Create folder under `features/`
   ```
   app/features/dashboard/
   ├── components/
   ├── services/
   └── pages/
   ```

2. **Add shared utilities**: Use `shared/` for reusable code
   ```
   app/shared/utils/
   ├── validators.ts
   ├── formatters.ts
   └── helpers.ts
   ```

3. **Add routing** (recommended):
   - Install: `npm install react-router-dom`
   - Create: `app/routes/`
   - Organize by feature

4. **Add state management** (for complex apps):
   - Zustand: `npm install zustand` (lightweight)
   - Redux Toolkit: `npm install @reduxjs/toolkit react-redux`

## Files Overview

- **App.tsx**: Main entry component, orchestrates features
- **core/services/**: HTTP requests, API integration
- **shared/components/**: UI components used across multiple features
- **shared/hooks/**: Custom React hooks (useSearch, useDebounce, etc.)
- **shared/types/**: TypeScript interfaces & types
- **features/search/**: Search functionality module
- **layouts/**: Page layout wrappers (Header, Topbar, MainLayout)

## References

- Similar to: [mim-frontend](https://github.com/Hoo3g/mim-frontend)
- Angular style guide: [Angular Folder Structure Best Practices](https://angular.io/guide/styleguide)
- React patterns: [Bulletproof React](https://github.com/alan2207/bulletproof-react)
