#!/bin/bash
# setup.sh - Solo para Mac y Linux
set -e

echo "\n🚀 Configurando Plataforma de Gestión de Reservas (Mac/Linux)"

# Validar dependencias mínimas
for cmd in docker docker-compose python3 pip3; do
    if ! command -v $cmd &>/dev/null; then
        echo "❌ Error: '$cmd' no está instalado. Instálalo antes de continuar."
        exit 1
    fi
done

# Verificar que Docker esté ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está ejecutándose. Inicia Docker Desktop o el servicio docker."
    exit 1
fi

# Configurar archivos .env si faltan
if [ ! -f ".env" ]; then
    echo "📝 Creando .env desde plantilla..."
    cp .env.example .env
fi
if [ ! -f "docker/.env" ]; then
    echo "📝 Creando docker/.env desde plantilla..."
    cp docker/.env.example docker/.env
fi

# Selección de stack a levantar
echo "\n� ¿Qué stack deseas iniciar?"
echo "1) Solo base de datos (db-only)"
echo "2) Full stack (Python + Java + DB)"
read -p "Selecciona una opción (1-2, default 1): " stack_option
stack_file="docker-compose.db-only.yml"
if [ "$stack_option" == "2" ]; then
    stack_file="docker-compose.full.yml"
fi

cd docker
echo "\n🐳 Levantando servicios con $stack_file ..."
docker-compose -f $stack_file up -d

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que PostgreSQL esté listo..."
for i in {1..20}; do
    if docker-compose exec -T postgres pg_isready -U $(grep POSTGRES_USER .env | cut -d'=' -f2) > /dev/null 2>&1; then
        echo "✅ PostgreSQL está listo."
        break
    fi
    sleep 2
done

cd ..


# Crear y activar entorno virtual
echo "\n🐍 Configurando entorno virtual Python..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Entorno virtual creado en ./venv"
fi

# Activar entorno virtual según shell
if [ -n "$ZSH_VERSION" ]; then
    source venv/bin/activate
elif [ -n "$BASH_VERSION" ]; then
    source venv/bin/activate
else
    . venv/bin/activate
fi

echo "\n📦 Instalando dependencias Python en el virtualenv..."
pip install --upgrade pip
pip install -r requirements.txt

# Mostrar credenciales
echo "\n📋 Credenciales configuradas (docker/.env):"
grep -E 'POSTGRES_USER|POSTGRES_PASSWORD|PGADMIN_DEFAULT_EMAIL|PGADMIN_DEFAULT_PASSWORD' docker/.env | sed 's/^/   /'


echo "\n👤 Creando usuario administrador por defecto..."
if [ -f "create_admin.py" ]; then
    python create_admin.py || echo "⚠️  No se pudo crear el admin automáticamente. Puedes crearlo manualmente luego."
else
    echo "⚠️  create_admin.py no encontrado."
fi

echo "\n🎉 Setup completado. Servicios disponibles:"
echo "   - PostgreSQL: localhost:5432"
echo "   - API Python: http://localhost:8000/docs"
echo "   - API Java:   http://localhost:8080/swagger-ui.html"
echo "   - PgAdmin:    http://localhost:5050"

echo "\n🔧 Próximos pasos:"
echo "   1. (Opcional) Edita .env y docker/.env si necesitas credenciales personalizadas."
echo "   2. Activa el entorno virtual en cada terminal: source venv/bin/activate"
echo "   3. Ejecuta el servicio Python: python main.py"
echo "   4. Ejecuta el Java Service en otra terminal:"
echo "      cd java-service && ./mvnw spring-boot:run"
echo "   5. Accede a la API y frontend en los puertos indicados."
echo "\n💡 Para Windows, usa setup_win.bat."