# 🚀 Inicio Rápido - VozPública

## ⚡ Para Empezar AHORA (3 pasos)

### 1. Instala las dependencias del frontend (solo primera vez)
```bash
cd /workspaces/vozpublica/frontend
npm install
```

### 2. Inicia ambos servicios
```bash
cd /workspaces/vozpublica
./start-dev.sh
```

### 3. Abre tu navegador
- Frontend: **http://localhost:3000**
- API Docs: **http://localhost:8000/docs**

## 🎯 Tu Primera Prueba

1. Abre http://localhost:3000
2. Haz clic en "Explorar Análisis"
3. Ingresa: "seguridad pública"
4. Presiona "Analizar"
5. ¡Observa los resultados!

## 📖 Más Información

- **Guía de Pruebas Completa**: Ver [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Arquitectura del Sistema**: Ver [ARCHITECTURE.md](ARCHITECTURE.md)

## 🔧 Comandos Útiles

### Detener los servicios
```bash
# Presiona Ctrl+C en la terminal donde corriste start-dev.sh
```

### Reiniciar solo el frontend
```bash
cd /workspaces/vozpublica/frontend
npm run dev
```

### Reiniciar solo el backend
```bash
cd /workspaces/vozpublica
uvicorn backend.app.main:app --reload
```

### Ver logs en tiempo real
Los logs aparecen automáticamente en las terminales donde corren los servicios.

## 🆘 ¿Problemas?

### Puerto ocupado
```bash
# Liberar puerto 3000 (frontend)
lsof -ti:3000 | xargs kill -9

# Liberar puerto 8000 (backend)
lsof -ti:8000 | xargs kill -9
```

### No se conecta al backend
1. Verifica que el backend esté corriendo:
   ```bash
   curl http://localhost:8000/health
   ```
2. Debes ver: `{"status":"ok"}`

## 📚 Recursos de Aprendizaje

- [Next.js Tutorial](https://nextjs.org/learn)
- [React Docs](https://react.dev/learn)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
