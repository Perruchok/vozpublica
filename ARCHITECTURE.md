# 🏗️ Arquitectura VozPública

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                  │
│                      (Navegador Web)                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                            │
│                    Puerto: 3000                                  │
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
│                    Puerto: 8000                                  │
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
│  │  • drift.py - Análisis de cambio semántico              │   │
│  │  • narrative_evolution.py - Evolución narrativa          │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                    │
└─────────────────────────────┼────────────────────────────────────┘
                              │
                              │ SQL Queries
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  BASE DE DATOS (PostgreSQL)                      │
│                  con extensión pgvector                          │
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

## Flujo de una Petición Típica

### Ejemplo: Usuario busca evolución semántica de "seguridad pública"

```
1. USUARIO
   └─> Ingresa "seguridad pública" en el formulario
   └─> Selecciona fechas: 2024-01-01 a 2024-12-31
   └─> Hace clic en "Analizar"

2. FRONTEND (React Component)
   └─> El componente captura el submit del formulario
   └─> Llama a: fetchSemanticEvolution({ 
         concept: "seguridad pública",
         start_date: "2024-01-01",
         end_date: "2024-12-31"
       })

3. API CLIENT (frontend/lib/api.js)
   └─> Construye la URL: http://localhost:8000/api/semantic-evolution
   └─> Hace fetch() con POST request
   └─> Body: JSON con los parámetros

4. BACKEND - API ROUTER (backend/app/api/semantic_evolution.py)
   └─> Recibe el POST request
   └─> Valida los parámetros con Pydantic models
   └─> Llama al service

5. BACKEND - SERVICE (backend/app/services/semantic_evolution_service.py)
   └─> Procesa la lógica de negocio
   └─> Llama a las funciones de analytics

6. BACKEND - ANALYTICS (backend/analytics/drift.py)
   └─> Genera embedding del concepto
   └─> Consulta la base de datos con filtros temporales
   └─> Calcula similitudes coseno
   └─> Detecta drift semántico

7. BASE DE DATOS
   └─> Ejecuta queries con pgvector
   └─> Retorna resultados con embeddings y metadatos

8. BACKEND - RESPONSE
   └─> Formatea los resultados
   └─> Retorna JSON con:
       • Points: [{period, similarity, sample_texts}]
       • Drift: {magnitude, direction, explanation}

9. FRONTEND - API CLIENT
   └─> Recibe la respuesta JSON
   └─> Parsea el response
   └─> Retorna los datos al componente

10. FRONTEND - COMPONENT
    └─> Actualiza el estado de React
    └─> Re-renderiza con los nuevos datos
    └─> Muestra:
        • Gráficos de evolución
        • Explicación del drift
        • Ejemplos de textos
```

## Componentes Clave

### Frontend

| Archivo | Propósito |
|---------|-----------|
| `app/page.jsx` | Página principal (landing) |
| `app/layout.jsx` | Layout global con metadata |
| `app/narrative/page.jsx` | Página de análisis narrativo |
| `lib/api.js` | Cliente API - hace las llamadas al backend |
| `lib/constants.js` | Configuración y constantes |
| `components/narrative/*` | Componentes UI específicos |
| `styles/globals.css` | Estilos globales |

### Backend

| Archivo | Propósito |
|---------|-----------|
| `app/main.py` | Punto de entrada, configuración CORS |
| `app/api/*.py` | Routers - endpoints de la API |
| `app/services/*.py` | Lógica de negocio |
| `app/models/*.py` | Modelos Pydantic (validación) |
| `analytics/*.py` | Algoritmos de análisis |
| `utils/*.py` | Utilidades (DB, texto, etc.) |
| `settings.py` | Configuración de la aplicación |

## Patrones de Diseño Utilizados

### 1. **Separation of Concerns**
- Frontend: solo UI y experiencia de usuario
- Backend: lógica de negocio y acceso a datos

### 2. **API-First Design**
- El backend expone una API RESTful
- El frontend consume la API
- Permite cambiar frontend sin tocar backend

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
- Componentes reutilizables
- Estado local vs global
- Props para comunicación entre componentes

## Tecnologías Clave

### Frontend Stack
- **Next.js 14**: Framework React con SSR
- **React 18**: Librería UI
- **Fetch API**: Cliente HTTP nativo

### Backend Stack
- **FastAPI**: Framework web moderno
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI
- **PostgreSQL + pgvector**: Base de datos vectorial

### Comunicación
- **REST API**: JSON sobre HTTP
- **CORS**: Habilitado para localhost:3000

## Variables de Entorno

### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend
```env
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
```

## Puertos

| Servicio | Puerto | URL |
|----------|--------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| Database | 5432 | (local o remoto) |

## Próximos Pasos en tu Aprendizaje

1. **Entiende el ciclo de vida de React**
   - useState, useEffect
   - Props y State
   - Event handlers

2. **Aprende sobre Next.js App Router**
   - File-based routing
   - Server vs Client Components
   - Metadata y SEO

3. **Domina las llamadas API**
   - async/await
   - Manejo de errores
   - Loading states

4. **Explora React DevTools**
   - Inspeccionar componentes
   - Ver el state en tiempo real
   - Profiling de performance
