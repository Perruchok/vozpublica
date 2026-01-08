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

# Iniciar backend
echo "📦 Iniciando backend (FastAPI en puerto 8000)..."
cd /workspaces/vozpublica
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Esperar un momento para que el backend inicie
sleep 3

# Iniciar frontend
echo "⚛️  Iniciando frontend (Next.js en puerto 3000)..."
cd /workspaces/vozpublica/frontend
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
