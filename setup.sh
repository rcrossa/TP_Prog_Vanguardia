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

# Función para configurar archivos .env
configure_env_files() {
    # Crear archivo .env si no existe
    if [ ! -f ".env" ]; then
        echo "📝 Creando archivo .env desde plantilla..."
        cp .env.example .env
        echo "✅ Archivo .env creado"
    fi

    # Crear archivo .env para Docker si no existe
    if [ ! -f "docker/.env" ]; then
        echo "📝 Creando docker/.env desde plantilla..."
        cp docker/.env.example docker/.env
        echo "✅ Docker .env creado"
    fi
}

# Preguntar al usuario sobre configuración
echo ""
echo "🔧 Opciones de configuración:"
echo "1) Usar configuración por defecto (recomendado para desarrollo)"
echo "2) Configurar credenciales personalizadas"
echo ""
read -p "Selecciona una opción (1-2): " config_option

case $config_option in
    1)
        echo "✅ Usando configuración por defecto para desarrollo"
        configure_env_files
        ;;
    2)
        echo "🔧 Configuración personalizada seleccionada"
        configure_env_files
        echo ""
        echo "⚠️  Por favor, edita los siguientes archivos con tus credenciales:"
        echo "   - .env (configuración de la aplicación)"
        echo "   - docker/.env (configuración de contenedores)"
        echo ""
        read -p "Presiona ENTER cuando hayas terminado de editar los archivos .env..."
        ;;
    *)
        echo "❌ Opción inválida. Usando configuración por defecto."
        configure_env_files
        ;;
esac

# Levantar servicios de Docker
echo "🐳 Iniciando servicios de base de datos..."
cd docker
docker-compose up -d

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que PostgreSQL esté listo..."
sleep 10

# Verificar conexión a base de datos
echo "🔍 Verificando conexión a base de datos..."

# Cargar variables desde docker/.env
if [ -f ".env" ]; then
    source .env 2>/dev/null || true
fi

DB_USER=${POSTGRES_USER:-reservas_user}
DB_NAME=${POSTGRES_DB:-reservas}

if docker exec reservas_db pg_isready -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; then
    echo "✅ Base de datos PostgreSQL lista"
else
    echo "❌ Error: No se puede conectar a PostgreSQL"
    echo "   Verificando credenciales en docker/.env..."
    sleep 5
fi

# Mostrar información de servicios y credenciales
echo ""
echo "🎉 Setup completado exitosamente!"
echo ""
echo "📊 Servicios disponibles:"
echo "   PostgreSQL: localhost:5432"
echo "   PgAdmin:    http://localhost:8080"
echo ""

# Mostrar credenciales desde los archivos .env
echo "📋 Credenciales configuradas:"
if [ -f ".env" ]; then
    echo ""
    echo "🔐 Para PostgreSQL:"
    DB_USER_ACTUAL=$(grep "POSTGRES_USER=" docker/.env 2>/dev/null | cut -d'=' -f2 || echo "reservas_user")
    DB_PASS_ACTUAL=$(grep "POSTGRES_PASSWORD=" docker/.env 2>/dev/null | cut -d'=' -f2 || echo "reservas_password")
    echo "   Usuario: $DB_USER_ACTUAL"
    echo "   Password: $DB_PASS_ACTUAL"
    echo ""
    echo "🔐 Para PgAdmin:"
    PG_EMAIL=$(grep "PGADMIN_DEFAULT_EMAIL=" docker/.env 2>/dev/null | cut -d'=' -f2 || echo "admin@reservas.com")
    PG_PASS=$(grep "PGADMIN_DEFAULT_PASSWORD=" docker/.env 2>/dev/null | cut -d'=' -f2 || echo "admin123")
    echo "   Email: $PG_EMAIL"
    echo "   Password: $PG_PASS"
else
    echo "   Consulta archivos .env y docker/.env para credenciales"
fi

echo ""
echo "🔧 Próximos pasos:"
echo "   1. Instalar dependencias Python: pip install -r requirements.txt"
echo "   2. Ejecutar la aplicación: python main.py"
echo "   3. API disponible en: http://localhost:8000/docs"
echo ""

cd ..