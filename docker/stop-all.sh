#!/bin/bash

# =========================================================================
# Script para DETENER todos los contenedores
# =========================================================================

echo "🛑 Deteniendo todos los contenedores..."
echo ""

# Cambiar al directorio docker
cd "$(dirname "$0")"

# Detener modo DB-only si está corriendo
echo "Deteniendo modo DB-only..."
docker-compose -f docker-compose.db-only.yml down 2>/dev/null

# Detener modo Full si está corriendo
echo "Deteniendo modo Full..."
docker-compose -f docker-compose.full.yml down 2>/dev/null

echo ""
echo "✅ Todos los contenedores detenidos"
echo ""
echo "💡 Para eliminar también los volúmenes (CUIDADO: borra datos):"
echo "   docker-compose -f docker-compose.db-only.yml down -v"
echo "   docker-compose -f docker-compose.full.yml down -v"
