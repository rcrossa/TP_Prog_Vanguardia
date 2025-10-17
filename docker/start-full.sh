#!/bin/bash

# =========================================================================
# Script para MODO COMPLETO (Todo el Stack)
# =========================================================================
# Este script inicia TODO en Docker: Python + Java + PostgreSQL + pgAdmin
# Ideal para demos, testing y deploy
# =========================================================================

# Cambiar al directorio docker
cd "$(dirname "$0")"

# Verificar que existe el archivo .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "� Creando .env desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado con valores por defecto"
    echo ""
fi

echo "�🚀 Iniciando MODO COMPLETO (Stack Completo)..."
echo "================================================"
echo ""
echo "📦 Servicios que se iniciarán:"
echo "  ✓ PostgreSQL (puerto ${POSTGRES_PORT:-5432})"
echo "  ✓ pgAdmin (puerto ${PGADMIN_PORT:-5050})"
echo "  ✓ Python Service (puerto ${PYTHON_SERVICE_PORT:-8000})"
echo "  ✓ Java Service (puerto ${JAVA_SERVICE_PORT:-8080})"
echo ""
echo "💾 Memoria total aproximada: 1.6 GB"
echo "📊 URLs disponibles:"
echo "  • Frontend Python: http://localhost:${PYTHON_SERVICE_PORT:-8000}"
echo "  • API Python Docs: http://localhost:${PYTHON_SERVICE_PORT:-8000}/docs"
echo "  • API Java Docs: http://localhost:${JAVA_SERVICE_PORT:-8080}/swagger-ui.html"
echo "  • pgAdmin: http://localhost:${PGADMIN_PORT:-5050}"
echo ""
echo "⏳ Construyendo imágenes (puede tardar 2-3 min)..."
echo "================================================"
echo ""

# Levantar servicios con build
docker-compose -f docker-compose.full.yml up --build

echo ""
echo "✅ Servicios detenidos"
