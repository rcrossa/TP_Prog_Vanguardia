#!/bin/bash

# Script para probar la integración Python ↔ Java

echo "🔗 Script de Prueba de Integración Python ↔ Java"
echo "=================================================="
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# URLs
PYTHON_URL="http://localhost:8000"
JAVA_URL="http://localhost:8080"

echo "📡 Verificando servicios..."
echo ""

# Verificar Python Service
echo -n "🐍 Python Service (8000): "
if curl -s -f "$PYTHON_URL/docs" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Disponible${NC}"
    PYTHON_OK=true
else
    echo -e "${RED}❌ NO disponible${NC}"
    PYTHON_OK=false
fi

# Verificar Java Service
echo -n "☕ Java Service (8080): "
if curl -s -f "$JAVA_URL/swagger-ui.html" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Disponible${NC}"
    JAVA_OK=true
else
    echo -e "${RED}❌ NO disponible${NC}"
    JAVA_OK=false
fi

echo ""

if [ "$PYTHON_OK" = false ] || [ "$JAVA_OK" = false ]; then
    echo -e "${RED}⚠️  Uno o más servicios no están disponibles${NC}"
    echo ""
    echo "Por favor, asegúrate de que ambos servicios estén corriendo:"
    echo "  - Python: python main.py"
    echo "  - Java: cd java-service && mvn spring-boot:run"
    exit 1
fi

echo -e "${GREEN}✅ Ambos servicios están disponibles. Procediendo con las pruebas...${NC}"
echo ""
echo "=================================================="
echo ""

# Prueba 1: Health Check
echo "🧪 Prueba 1: Health Check de Java desde Python"
echo "----------------------------------------------"
RESPONSE=$(curl -s "$PYTHON_URL/api/v1/integration/health")
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Prueba 2: Obtener salas desde Java
echo "🧪 Prueba 2: Obtener salas desde Java Service"
echo "----------------------------------------------"
RESPONSE=$(curl -s "$PYTHON_URL/api/v1/integration/salas-desde-java")
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Prueba 3: Validar sala específica
echo "🧪 Prueba 3: Validar sala ID=1"
echo "----------------------------------------------"
RESPONSE=$(curl -s "$PYTHON_URL/api/v1/integration/sala/1/validar")
if echo "$RESPONSE" | grep -q "error" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Sala no encontrada o error${NC}"
else
    echo "$RESPONSE" | python3 -m json.tool
fi
echo ""

# Prueba 4: Demo completa
echo "🧪 Prueba 4: Demo de integración"
echo "----------------------------------------------"
RESPONSE=$(curl -s "$PYTHON_URL/api/v1/integration/demo")
echo "$RESPONSE" | python3 -m json.tool
echo ""

echo "=================================================="
echo ""
echo -e "${GREEN}✅ Pruebas completadas${NC}"
echo ""
echo "📚 Para más información:"
echo "  - Documentación: docs/INTEGRACION.md"
echo "  - Swagger Python: $PYTHON_URL/docs"
echo "  - Swagger Java: $JAVA_URL/swagger-ui.html"
echo ""
