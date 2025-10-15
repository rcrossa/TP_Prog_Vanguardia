#!/bin/bash

# Script de setup para el proyecto de reservas
set -e

echo "🚀 Configurando proyecto de Plataforma de Gestión de Reservas..."

# Verificar que Docker Desktop esté ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker Desktop no está ejecutándose"
    echo "   Por favor, inicia Docker Desktop e intenta de nuevo"
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env desde plantilla..."
    cp config/.env.example .env
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tus configuraciones reales"
else
    echo "✅ Archivo .env ya existe"
fi

# Levantar servicios de Docker
echo "🐳 Iniciando servicios de base de datos..."
cd docker
docker-compose up -d

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que PostgreSQL esté listo..."
sleep 10

# Verificar conexión a base de datos
echo "🔍 Verificando conexión a base de datos..."
if docker exec -it reservas_db pg_isready -U reservas_user -d reservas > /dev/null 2>&1; then
    echo "✅ Base de datos PostgreSQL lista"
else
    echo "❌ Error: No se puede conectar a PostgreSQL"
    exit 1
fi

# Mostrar información de servicios
echo ""
echo "🎉 Setup completado exitosamente!"
echo ""
echo "📊 Servicios disponibles:"
echo "   PostgreSQL: localhost:5432"
echo "   PgAdmin:    http://localhost:8080"
echo ""
echo "📋 Datos de acceso PgAdmin:"
echo "   Email:      admin@reservas.com"  
echo "   Password:   admin123"
echo ""
echo "🔧 Próximos pasos:"
echo "   1. Instalar dependencias Python: pip install -r requirements.txt"
echo "   2. Verificar configuración en .env"
echo "   3. Ejecutar la aplicación"
echo ""

cd ..