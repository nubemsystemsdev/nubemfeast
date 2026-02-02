#!/bin/bash
# Script para verificar disponibilidad de puertos antes de iniciar NubemFeast

BACKEND_PORT=${API_PORT:-8002}
FRONTEND_PORT=5173

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_port() {
    local port=$1
    local service=$2

    if lsof -i :$port > /dev/null 2>&1; then
        echo -e "${RED}[OCUPADO]${NC} Puerto $port ($service)"
        # Mostrar qué proceso lo está usando
        echo -e "         Proceso: $(lsof -i :$port | grep LISTEN | awk '{print $1, $2}' | head -1)"
        return 1
    else
        echo -e "${GREEN}[LIBRE]${NC}   Puerto $port ($service)"
        return 0
    fi
}

verify_nubemfeast() {
    local port=$1
    echo -e "${YELLOW}Verificando si es NubemFeast en puerto $port...${NC}"

    response=$(curl -s "http://localhost:$port/health" 2>/dev/null)
    if echo "$response" | grep -q '"app":"NubemFeast"'; then
        echo -e "${GREEN}[OK]${NC} NubemFeast backend detectado en puerto $port"
        return 0
    elif [ -n "$response" ]; then
        echo -e "${RED}[CONFLICTO]${NC} Hay otra aplicación en puerto $port"
        echo "         Respuesta: $response"
        return 1
    fi
    return 0
}

echo "=========================================="
echo "  NubemFeast - Verificación de Puertos"
echo "=========================================="
echo ""

backend_ok=true
frontend_ok=true

check_port $BACKEND_PORT "Backend API" || backend_ok=false
check_port $FRONTEND_PORT "Frontend" || frontend_ok=false

echo ""

# Si el puerto del backend está ocupado, verificar si es NubemFeast
if [ "$backend_ok" = false ]; then
    verify_nubemfeast $BACKEND_PORT
fi

echo ""
echo "=========================================="

if [ "$backend_ok" = true ] && [ "$frontend_ok" = true ]; then
    echo -e "${GREEN}Todos los puertos están disponibles!${NC}"
    echo ""
    echo "Puedes iniciar la aplicación con:"
    echo "  Backend:  cd backend && uvicorn src.main:app --reload --port $BACKEND_PORT"
    echo "  Frontend: cd frontend && npm run dev"
    exit 0
else
    echo -e "${YELLOW}Algunos puertos están ocupados.${NC}"
    echo ""
    echo "Opciones:"
    echo "  1. Detener las aplicaciones que usan esos puertos"
    echo "  2. Cambiar el puerto del backend: API_PORT=8003 ./scripts/check-ports.sh"
    exit 1
fi
