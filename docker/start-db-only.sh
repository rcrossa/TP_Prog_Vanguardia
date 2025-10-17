#!/bin/bash

# =========================================================================
# Script para MODO HÍBRIDO (Solo Base de Datos)
# =========================================================================
# Este script inicia solo PostgreSQL y pgAdmin en Docker
# Los servicios Python y Java se ejecutan manualmente desde tu IDE
# =========================================================================

# Cambiar al directorio docker
cd "$(dirname "$0")"

# Verificar que existe el archivo .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "📝 Creando .env desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado con valores por defecto"
    echo ""
fi

echo "🚀 Iniciando MODO HÍBRIDO (Solo Base de Datos)..."
echo "================================================"
echo ""
echo "📦 Servicios que se iniciarán:"
echo "  ✓ PostgreSQL (puerto ${POSTGRES_PORT:-5432})"
echo "  ✓ pgAdmin (puerto ${PGADMIN_PORT:-5050})"
echo ""
echo "💡 Luego ejecuta manualmente:"
echo "  • Python: uvicorn main:app --reload"
echo "  • Java: mvn spring-boot:run (desde java-service/)"
echo ""
echo "================================================"
echo ""

# Levantar servicios
docker-compose -f docker-compose.db-only.yml up -d

echo ""
echo "✅ Servicios detenidos"
