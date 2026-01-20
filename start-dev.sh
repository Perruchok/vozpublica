#!/bin/bash
# Script para iniciar backend y frontend en desarrollo

echo "🚀 Iniciando VozPública en modo desarrollo..."

# Función para manejar Ctrl+C
cleanup() {
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Activar el entorno virtual de Python
if [ -f "/workspaces/vozpublica/venv/bin/activate" ]; then
    source /workspaces/vozpublica/venv/bin/activate
    echo "✅ Python environment activated"
elif [ -f "/workspaces/vozpublica/.venv/bin/activate" ]; then
    source /workspaces/vozpublica/.venv/bin/activate
    echo "✅ Python environment activated"
fi

# Detectar si estamos en GitHub Codespaces y configurar URLs dinámicamente
if [ -n "$CODESPACE_NAME" ] && [ -n "$GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN" ]; then
    BACKEND_URL="https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
    echo "🌐 GitHub Codespaces detectado"
    echo "   Backend URL: $BACKEND_URL"
else
    BACKEND_URL="http://localhost:8000"
    echo "💻 Local development mode"
fi

# Iniciar backend
echo "📦 Iniciando backend (FastAPI en puerto 8000)..."
cd /workspaces/vozpublica
ENVIRONMENT=development uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Esperar un momento para que el backend inicie
sleep 3

# Iniciar frontend con la URL del backend configurada
echo "⚛️  Iniciando frontend (Next.js en puerto 3000)..."
cd /workspaces/vozpublica/frontend

# Actualizar o crear .env.local con la URL correcta
echo "NEXT_PUBLIC_API_URL=$BACKEND_URL" > .env.local
echo "✅ Configurado .env.local con NEXT_PUBLIC_API_URL=$BACKEND_URL"

npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Servicios iniciados:"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Frontend: http://localhost:3000"
echo ""
echo "Presiona Ctrl+C para detener ambos servicios"

# Esperar indefinidamente
wait
