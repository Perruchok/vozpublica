#!/bin/bash
# Script de verificación pre-deployment para VozPública
# Verifica que todo esté listo antes de desplegar a producción

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}VozPública - Pre-Deployment Check${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Función para error
error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ((ERRORS++))
}

# Función para warning
warn() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
    ((WARNINGS++))
}

# Función para success
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# 1. Verificar archivos críticos
echo -e "${YELLOW}1. Verificando archivos críticos...${NC}"

if [ -f "Dockerfile" ]; then
    success "Dockerfile existe"
else
    error "Dockerfile no encontrado"
fi

if [ -f "requirements.txt" ]; then
    success "requirements.txt existe"
else
    error "requirements.txt no encontrado"
fi

if [ -f ".dockerignore" ]; then
    success ".dockerignore existe"
else
    warn ".dockerignore no encontrado (imagen será más grande)"
fi

if [ -f ".env.example" ]; then
    success ".env.example existe"
else
    warn ".env.example no encontrado (falta documentación de variables)"
fi

echo ""

# 2. Verificar .gitignore
echo -e "${YELLOW}2. Verificando .gitignore...${NC}"

if [ -f ".gitignore" ]; then
    if grep -q "^\.env$" .gitignore; then
        success ".env está en .gitignore"
    else
        error ".env NO está en .gitignore (riesgo de exposición de secretos)"
    fi
    
    if grep -q "^__pycache__" .gitignore; then
        success "__pycache__ está en .gitignore"
    else
        warn "__pycache__ no está en .gitignore"
    fi
else
    error ".gitignore no encontrado"
fi

echo ""

# 3. Verificar si .env está commiteado
echo -e "${YELLOW}3. Verificando si .env está en git...${NC}"

if git ls-files --error-unmatch .env 2>/dev/null; then
    error ".env está commiteado en git! Ejecuta: git rm --cached .env"
else
    success ".env no está en git"
fi

echo ""

# 4. Buscar print() en código
echo -e "${YELLOW}4. Buscando print() en código...${NC}"

PRINT_COUNT=$(find backend -name "*.py" -type f -exec grep -l "print(" {} \; 2>/dev/null | wc -l)

if [ "$PRINT_COUNT" -gt 0 ]; then
    warn "Encontrados $PRINT_COUNT archivos con print() (deberían usar logger)"
    echo "   Archivos:"
    find backend -name "*.py" -type f -exec grep -l "print(" {} \; 2>/dev/null | head -5 | sed 's/^/     - /'
    if [ "$PRINT_COUNT" -gt 5 ]; then
        echo "     ... y $((PRINT_COUNT - 5)) más"
    fi
else
    success "No se encontraron print() en código"
fi

echo ""

# 5. Verificar CORS en main.py
echo -e "${YELLOW}5. Verificando configuración CORS...${NC}"

if [ -f "backend/app/main.py" ]; then
    if grep -q 'allow_origins = \["\*"\]' backend/app/main.py; then
        error "CORS permite cualquier origen! Cambiar allow_origins antes de producción"
    elif grep -q "get_allowed_origins" backend/app/main.py; then
        success "CORS usa configuración dinámica"
    else
        warn "No se pudo verificar configuración CORS"
    fi
else
    error "backend/app/main.py no encontrado"
fi

echo ""

# 6. Verificar health checks
echo -e "${YELLOW}6. Verificando health checks...${NC}"

if [ -f "backend/app/api/health.py" ]; then
    success "Módulo health.py existe"
    
    if grep -q "/health/detailed" backend/app/api/health.py; then
        success "Health check detallado implementado"
    else
        warn "Health check detallado no encontrado"
    fi
else
    warn "backend/app/api/health.py no encontrado"
fi

echo ""

# 7. Verificar dependencias
echo -e "${YELLOW}7. Verificando dependencias...${NC}"

if [ -f "requirements.txt" ]; then
    DEP_COUNT=$(grep -v "^#" requirements.txt | grep -v "^$" | wc -l)
    success "$DEP_COUNT dependencias en requirements.txt"
    
    if grep -q "fastapi" requirements.txt; then
        success "fastapi está en requirements.txt"
    else
        error "fastapi no está en requirements.txt"
    fi
    
    if grep -q "uvicorn" requirements.txt; then
        success "uvicorn está en requirements.txt"
    else
        error "uvicorn no está en requirements.txt"
    fi
else
    error "requirements.txt no encontrado"
fi

echo ""

# 8. Verificar estructura de directorios
echo -e "${YELLOW}8. Verificando estructura de directorios...${NC}"

REQUIRED_DIRS=("backend" "backend/app" "backend/app/api" "backend/utils" "frontend")

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        success "Directorio $dir existe"
    else
        error "Directorio $dir no encontrado"
    fi
done

echo ""

# 9. Verificar variables de entorno necesarias
echo -e "${YELLOW}9. Verificando documentación de variables de entorno...${NC}"

if [ -f ".env.example" ]; then
    REQUIRED_VARS=("PGHOST" "PGUSER" "PGPASSWORD" "AZURE_OPENAI_ENDPOINT" "AZURE_OPENAI_API_KEY")
    
    for var in "${REQUIRED_VARS[@]}"; do
        if grep -q "^$var=" .env.example; then
            success "Variable $var documentada en .env.example"
        else
            warn "Variable $var NO documentada en .env.example"
        fi
    done
else
    warn ".env.example no existe (crear para documentar variables)"
fi

echo ""

# 10. Build test (opcional)
echo -e "${YELLOW}10. ¿Hacer build test de Docker? (opcional)${NC}"
read -p "Hacer build test? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Building Docker image..."
    if docker build -t vozpublica-api:precheck . > /dev/null 2>&1; then
        success "Docker build exitoso"
        
        # Verificar tamaño de imagen
        IMAGE_SIZE=$(docker images vozpublica-api:precheck --format "{{.Size}}")
        echo "   Tamaño de imagen: $IMAGE_SIZE"
        
        # Limpiar
        docker rmi vozpublica-api:precheck > /dev/null 2>&1 || true
    else
        error "Docker build falló"
    fi
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Resumen${NC}"
echo -e "${BLUE}========================================${NC}"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ Todo listo para producción!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  $WARNINGS warnings encontrados (revisar pero no bloqueante)${NC}"
    exit 0
else
    echo -e "${RED}❌ $ERRORS errores críticos encontrados${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠️  $WARNINGS warnings adicionales${NC}"
    fi
    echo ""
    echo "Por favor corrige los errores antes de desplegar a producción."
    exit 1
fi
