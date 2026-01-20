# ============================================
# Stage 1: Builder - Compilar dependencias
# ============================================
FROM python:3.12-slim AS builder

# Instalar dependencias del sistema necesarias para compilación
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias Python en directorio de usuario
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================
# Stage 2: Runtime - Imagen final optimizada
# ============================================
FROM python:3.12-slim

# Metadata
LABEL maintainer="VozPública Team"
LABEL version="1.0.0"
LABEL description="VozPública API - Backend FastAPI"

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar solo runtime dependencies (no build tools)
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Copiar dependencias Python compiladas desde builder
COPY --from=builder /root/.local /home/appuser/.local

# Copiar código de la aplicación
COPY --chown=appuser:appuser backend ./backend
COPY --chown=appuser:appuser requirements.txt .

# Agregar .local/bin al PATH
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Por defecto en producción, pero puede ser overrideado
ARG ALLOWED_ORIGINS=""
ENV ALLOWED_ORIGINS=${ALLOWED_ORIGINS}

# Cambiar a usuario no-root
USER appuser

# Health check disabled for Azure Web App
# Azure manages health checks via Application Settings
# Use /health or /health/detailed endpoints manually if needed

# Exponer puerto
EXPOSE 8000

# Comando de inicio con configuración optimizada para producción
CMD ["uvicorn", "backend.app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4", \
     "--timeout-keep-alive", "75", \
     "--access-log", \
     "--log-level", "info"]
