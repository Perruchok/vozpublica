# 🏗️ VozPública Architecture

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER                                    │
│                      (Web Browser)                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                            │
│                    Port: 3000                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Pages     │  │  Components  │  │    Lib       │           │
│  │             │  │              │  │              │           │
│  │ • page.jsx  │  │ • narrative/ │  │ • api.js     │←─────────┤─ Cliente API
│  │ • narrative/│  │ • common/    │  │ • constants  │           │
│  └─────────────┘  └──────────────┘  └──────────────┘           │
│                                            │                     │
└────────────────────────────────────────────┼─────────────────────┘
                                             │
                                             │ fetch()
                                             │ POST/GET
                                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
│                    Port: 8000                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    API Routers                           │   │
│  │  ┌───────────────┐  ┌──────────────┐  ┌─────────────┐  │   │
│  │  │ /semantic-    │  │ /explain-    │  │  /search    │  │   │
│  │  │  evolution    │  │  drift       │  │  /qa        │  │   │
│  │  └───────┬───────┘  └──────┬───────┘  └──────┬──────┘  │   │
│  └──────────┼──────────────────┼─────────────────┼─────────┘   │
│             │                  │                 │              │
│             ▼                  ▼                 ▼              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      Services                            │   │
│  │  • semantic_evolution_service.py                         │   │
│  │  • explain_drift_service.py                              │   │
│  │  • search_service.py                                     │   │
│  │  • qa_service.py                                         │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                    │
│                             ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Analytics                             │   │
│  │  • drift.py - Semantic change analysis                  │   │
│  │  • narrative_evolution.py - Narrative evolution          │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                    │
└─────────────────────────────┼────────────────────────────────────┘
                              │
                              │ SQL Queries
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DATABASE (PostgreSQL)                           │
│                  with pgvector extension                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │  speech_turns    │  │  raw_transcripts │                    │
│  │  • id            │  │  • id            │                    │
│  │  • content       │  │  • content       │                    │
│  │  • embedding     │  │  • metadata      │                    │
│  │  • timestamp     │  │  • date          │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Typical Request Flow

### Example: User searches for semantic evolution of "public security"

```
1. USER
   └─> Enters "public security" in the form
   └─> Selects dates: 2024-01-01 to 2024-12-31
   └─> Clicks "Analyze"

2. FRONTEND (React Component)
   └─> Component captures form submission
   └─> Calls: fetchSemanticEvolution({ 
         concept: "public security",
         start_date: "2024-01-01",
         end_date: "2024-12-31"
       })

3. API CLIENT (frontend/lib/api.js)
   └─> Builds URL: http://localhost:8000/api/semantic-evolution
   └─> Makes fetch() with POST request
   └─> Body: JSON with parameters

4. BACKEND - API ROUTER (backend/app/api/semantic_evolution.py)
   └─> Receives POST request
   └─> Validates parameters with Pydantic models
   └─> Calls service

5. BACKEND - SERVICE (backend/app/services/semantic_evolution_service.py)
   └─> Processes business logic
   └─> Calls analytics functions

6. BACKEND - ANALYTICS (backend/analytics/drift.py)
   └─> Generates concept embedding
   └─> Queries database with temporal filters
   └─> Calculates cosine similarities
   └─> Detects semantic drift

7. DATABASE
   └─> Executes queries with pgvector
   └─> Returns results with embeddings and metadata

8. BACKEND - RESPONSE
   └─> Formats results
   └─> Returns JSON with:
       • Points: [{period, similarity, sample_texts}]
       • Drift: {magnitude, direction, explanation}

9. FRONTEND - API CLIENT
   └─> Receives JSON response
   └─> Parses response
   └─> Returns data to component

10. FRONTEND - COMPONENT
    └─> Updates React state
    └─> Re-renders with new data
    └─> Displays:
        • Evolution charts
        • Drift explanation
        • Text examples
```

## Key Components

### Frontend

| File | Purpose |
|---------|-----------|
| `app/page.jsx` | Main page (landing) |
| `app/layout.jsx` | Global layout with metadata |
| `app/narrative/page.jsx` | Narrative analysis page |
| `lib/api.js` | API Client - makes backend calls |
| `lib/constants.js` | Configuration and constants |
| `components/narrative/*` | Specific UI components |
| `styles/globals.css` | Global styles |

### Backend

| File | Purpose |
|---------|-----------|
| `app/main.py` | Entry point, CORS configuration |
| `app/api/*.py` | Routers - API endpoints |
| `app/services/*.py` | Business logic |
| `app/models/*.py` | Pydantic models (validation) |
| `analytics/*.py` | Analysis algorithms |
| `utils/*.py` | Utilities (DB, text, etc.) |
| `settings.py` | Application configuration |

## Design Patterns Used

### 1. **Separation of Concerns**
- Frontend: only UI and user experience
- Backend: business logic and data access

### 2. **API-First Design**
- The backend exposes a RESTful API
- The frontend consumes the API
- Allows changing frontend without touching backend

### 3. **Layered Architecture** (Backend)
```
API Layer (Routers)
    ↓
Service Layer (Business Logic)
    ↓
Data Access Layer (Utils/DB)
    ↓
Database
```

### 4. **Component-Based Architecture** (Frontend)
- Reusable components
- Local vs global state
- Props for component communication

## Key Technologies

### Frontend Stack
- **Next.js 14**: React framework with SSR
- **React 18**: UI library
- **Fetch API**: Native HTTP client

### Backend Stack
- **FastAPI**: Modern web framework
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
- **PostgreSQL + pgvector**: Vector database

### Communication
- **REST API**: JSON over HTTP
- **CORS**: Enabled for localhost:3000

## Environment Variables

### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend
```env
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
```

## Ports

| Service | Port | URL |
|----------|--------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| Database | 5432 | (local or remote) |

## Next Steps in Your Learning

1. **Understand React lifecycle**
   - useState, useEffect
   - Props and State
   - Event handlers

2. **Learn about Next.js App Router**
   - File-based routing
   - Server vs Client Components
   - Metadata and SEO

3. **Master API calls**
   - async/await
   - Error handling
   - Loading states

4. **Explore React DevTools**
   - Inspect components
   - View state in real-time
   - Performance profiling
