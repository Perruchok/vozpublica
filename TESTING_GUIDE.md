# 🧪 Guía de Pruebas - Frontend VozPública

## Configuración Inicial

### 1. Instalar dependencias del frontend (si no lo has hecho)
```bash
cd /workspaces/vozpublica/frontend
npm install
```

### 2. Iniciar los servicios

**Opción A: Script automático (recomendado)**
```bash
cd /workspaces/vozpublica
./start-dev.sh
```

**Opción B: Manual en terminales separadas**

Terminal 1 - Backend:
```bash
cd /workspaces/vozpublica
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2 - Frontend:
```bash
cd /workspaces/vozpublica/frontend
npm run dev
```

## 🔗 URLs de Prueba

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## ✅ Checklist de Pruebas

### Nivel 1: Pruebas Básicas

- [ ] **Página principal carga correctamente**
  - Abre http://localhost:3000
  - Debes ver "VozPública" como título
  - Verifica que hay 3 tarjetas de características

- [ ] **Backend responde**
  - Abre http://localhost:8000/health
  - Debes ver: `{"status": "ok"}`

- [ ] **Documentación API accesible**
  - Abre http://localhost:8000/docs
  - Debes ver la interfaz Swagger UI

### Nivel 2: Navegación

- [ ] **Navegación a Análisis Narrativo**
  - En la página principal, haz clic en "Explorar Análisis"
  - Debes ir a la página `/narrative`

- [ ] **Estilos CSS cargan correctamente**
  - Verifica que los colores y diseños se ven bien
  - No hay errores de estilo en la consola del navegador

### Nivel 3: Integración Frontend-Backend

- [ ] **Prueba de API desde el frontend**
  
  En la página `/narrative`, debes poder:
  1. Ingresar un concepto (ej: "seguridad pública")
  2. Seleccionar fechas
  3. Ver gráficos de evolución semántica
  4. Ver explicaciones generadas por IA

### Nivel 4: Herramientas de Desarrollo

- [ ] **Console del navegador**
  - Abre DevTools (F12)
  - Ve a la pestaña Console
  - No debes ver errores rojos (warnings amarillos están OK)

- [ ] **Network tab**
  - Abre DevTools → Network
  - Realiza una búsqueda
  - Verifica que las llamadas a `http://localhost:8000/api/*` tienen status 200

- [ ] **React DevTools** (opcional)
  - Instala la extensión React DevTools
  - Inspecciona componentes y su estado

## 🐛 Debugging: Problemas Comunes

### El frontend no carga

```bash
# Verifica que Node.js está instalado
node --version

# Reinstala dependencias
cd /workspaces/vozpublica/frontend
rm -rf node_modules package-lock.json
npm install
```

### Error de CORS

Si ves errores como "blocked by CORS policy":
- Verifica que el backend esté corriendo en puerto 8000
- El backend ya tiene CORS configurado para localhost:3000

### Error: Cannot connect to backend

1. Verifica que el backend esté corriendo:
   ```bash
   curl http://localhost:8000/health
   ```

2. Verifica la configuración de API_BASE_URL:
   - Está en `frontend/lib/constants.js`
   - Debe ser: `http://localhost:8000`

### El puerto está ocupado

```bash
# Para backend (puerto 8000)
lsof -ti:8000 | xargs kill -9

# Para frontend (puerto 3000)
lsof -ti:3000 | xargs kill -9
```

## 🔍 Pruebas de API con cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Semantic Evolution
```bash
curl -X POST http://localhost:8000/api/semantic-evolution \
  -H "Content-Type: application/json" \
  -d '{
    "concept": "seguridad pública",
    "granularity": "month",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "similarity_threshold": 0.6
  }'
```

### Explain Drift
```bash
curl -X POST http://localhost:8000/api/explain-drift \
  -H "Content-Type: application/json" \
  -d '{
    "concept": "seguridad pública",
    "from_period": "2024-01-01",
    "to_period": "2024-06-01",
    "similarity_threshold": 0.6
  }'
```

## 📊 Monitoreo en Tiempo Real

### Logs del Backend
```bash
# Los logs aparecen automáticamente en la terminal donde corriste uvicorn
# Busca líneas como:
# INFO:     127.0.0.1:xxxxx - "POST /api/semantic-evolution HTTP/1.1" 200 OK
```

### Logs del Frontend
```bash
# Next.js muestra logs en su terminal
# Busca líneas como:
# ○ Compiling /narrative ...
# ✓ Compiled successfully
```

### Browser Console
```javascript
// En la consola del navegador, puedes probar manualmente:
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log)
```

## 🎯 Pruebas Recomendadas para Aprender

### 1. Modificar un componente
- Edita `frontend/app/page.jsx`
- Cambia el texto del tagline
- Guarda el archivo
- El navegador debe recargarse automáticamente (Hot Reload)

### 2. Ver el flujo de datos
- Abre DevTools → Network
- En `/narrative`, realiza una búsqueda
- Observa la llamada POST a `/api/semantic-evolution`
- Inspecciona el Request y Response

### 3. Agregar un console.log
En `frontend/lib/api.js`, agrega:
```javascript
export async function fetchSemanticEvolution(params) {
  console.log('📤 Enviando request:', params);
  const result = await fetchAPI('/api/semantic-evolution', {
    method: 'POST',
    body: JSON.stringify({...}),
  });
  console.log('📥 Respuesta recibida:', result);
  return result;
}
```

## 📚 Recursos de Aprendizaje

- **Next.js Docs**: https://nextjs.org/docs
- **React Docs**: https://react.dev
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Fetch API**: https://developer.mozilla.org/es/docs/Web/API/Fetch_API

## 🎓 Ejercicios Sugeridos

1. **Agregar un nuevo botón** en la página principal
2. **Crear un nuevo componente** en `frontend/components/common/`
3. **Agregar un nuevo campo** al formulario de búsqueda
4. **Cambiar los colores** en `frontend/styles/globals.css`
5. **Agregar validación** a los inputs del formulario
