#!/bin/bash

# =========================================================================
# Script para DETENER todos los contenedores Y procesos locales
# =========================================================================

echo "🛑 Deteniendo todos los servicios (Docker y procesos locales)..."
echo ""

# Cambiar al directorio docker
cd "$(dirname "$0")"

# Detener modo DB-only si está corriendo
echo "📦 Deteniendo contenedores modo DB-only..."
docker-compose -f docker-compose.db-only.yml down 2>/dev/null

# Detener modo Full si está corriendo
echo "📦 Deteniendo contenedores modo Full..."
docker-compose -f docker-compose.full.yml down 2>/dev/null

echo ""
echo "🐍 Deteniendo procesos Python locales (uvicorn/FastAPI)..."
# Matar procesos Python que estén corriendo main.py o uvicorn
pkill -f "python.*main.py" 2>/dev/null && echo "   ✅ Proceso Python detenido" || echo "   ℹ️  No hay procesos Python corriendo"
pkill -f "uvicorn.*main:app" 2>/dev/null && echo "   ✅ Uvicorn detenido" || true

echo ""
echo "☕ Deteniendo procesos Java locales (Spring Boot/Maven)..."
# Matar procesos Java (Maven y Spring Boot)
pkill -f "mvn.*spring-boot:run" 2>/dev/null && echo "   ✅ Maven Spring Boot detenido" || echo "   ℹ️  No hay procesos Maven corriendo"
pkill -f "java.*spring-boot" 2>/dev/null && echo "   ✅ Spring Boot detenido" || true

echo ""
echo "✅ Todos los servicios detenidos (Docker + procesos locales)"
echo ""
echo "💡 Para eliminar también los volúmenes de Docker (CUIDADO: borra datos):"
echo "   docker-compose -f docker-compose.db-only.yml down -v"
echo "   docker-compose -f docker-compose.full.yml down -v"
