#!/bin/bash
# setup.sh - Solo para Mac y Linux
set -e

echo "\n🚀 Configurando Plataforma de Gestión de Reservas (Mac/Linux)"

# Configurar Java 21 para Maven (necesario para compilar el servicio Java)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: Buscar Java 21 automáticamente
    JAVA_21_HOME=$(/usr/libexec/java_home -v 21 2>/dev/null || echo "")
    if [ -n "$JAVA_21_HOME" ]; then
        export JAVA_HOME="$JAVA_21_HOME"
        echo "✅ Java 21 configurado: $JAVA_HOME"
    else
        echo "⚠️  Java 21 no encontrado. El servicio Java puede fallar al compilar."
        echo "   Instala Java 21 desde: https://aws.amazon.com/corretto/"
    fi
else
    # Linux: Intentar encontrar Java 21
    if command -v java &>/dev/null; then
        JAVA_VERSION=$(java -version 2>&1 | head -n 1 | awk -F '"' '{print $2}' | cut -d'.' -f1)
        if [ "$JAVA_VERSION" == "21" ]; then
            echo "✅ Java 21 detectado"
        else
            echo "⚠️  Java $JAVA_VERSION detectado. Se recomienda Java 21 para este proyecto."
        fi
    fi
fi

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

# Generar timestamp para cache busting
CACHE_VERSION=$(date +%s)
echo "🔄 Generando versión de caché: $CACHE_VERSION"

# Actualizar o agregar STATIC_VERSION en .env
if grep -q "^STATIC_VERSION=" .env; then
    # Si existe, reemplazarla
    sed -i.bak "s/^STATIC_VERSION=.*/STATIC_VERSION=$CACHE_VERSION/" .env
    rm -f .env.bak
else
    # Si no existe, agregarla
    echo "STATIC_VERSION=$CACHE_VERSION" >> .env
fi

if [ ! -f "docker/.env" ]; then
    echo "📝 Creando docker/.env desde plantilla..."
    cp docker/.env.example docker/.env
fi

# Actualizar o agregar STATIC_VERSION en docker/.env también
if grep -q "^STATIC_VERSION=" docker/.env; then
    sed -i.bak "s/^STATIC_VERSION=.*/STATIC_VERSION=$CACHE_VERSION/" docker/.env
    rm -f docker/.env.bak
else
    echo "STATIC_VERSION=$CACHE_VERSION" >> docker/.env
fi

# Selección de stack a levantar
echo "\n🔧 ¿Qué stack deseas iniciar?"
echo "1) Solo base de datos (db-only) - Python y Java correrán localmente"
echo "2) Full stack (Python + Java + DB) - Todo en Docker"
read -p "Selecciona una opción (1-2, default 1): " stack_option
stack_file="docker-compose.db-only.yml"
USE_DOCKER_FULL=false

if [ "$stack_option" == "2" ]; then
    stack_file="docker-compose.full.yml"
    USE_DOCKER_FULL=true
fi

cd docker
echo "\n🐳 Levantando servicios con $stack_file ..."
docker-compose -f $stack_file up -d

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que PostgreSQL esté listo..."
for i in {1..20}; do
    if docker-compose -f $stack_file exec -T postgres pg_isready -U $(grep POSTGRES_USER .env | cut -d'=' -f2) > /dev/null 2>&1; then
        echo "✅ PostgreSQL está listo."
        break
    fi
    sleep 2
done

cd ..

# Solo configurar entorno Python local si NO es modo Full Docker
if [ "$USE_DOCKER_FULL" = false ]; then
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
fi

# Mostrar credenciales
echo "\n📋 Credenciales configuradas (docker/.env):"
grep -E 'POSTGRES_USER|POSTGRES_PASSWORD|PGADMIN_DEFAULT_EMAIL|PGADMIN_DEFAULT_PASSWORD' docker/.env | sed 's/^/   /'

# Crear usuario admin solo si NO es modo Full Docker
if [ "$USE_DOCKER_FULL" = false ]; then
    echo "\n👤 Creando usuario administrador por defecto..."
    if [ -f "create_admin.py" ]; then
        python create_admin.py || echo "⚠️  No se pudo crear el admin automáticamente. Puedes crearlo manualmente luego."
    else
        echo "⚠️  create_admin.py no encontrado."
    fi
fi

if [ "$USE_DOCKER_FULL" = true ]; then
    echo "\n🎉 Setup completado (Modo Full Docker). Servicios disponibles:"
    echo "   - PostgreSQL: localhost:5432"
    echo "   - API Python: http://localhost:8000/docs (en Docker)"
    echo "   - API Java:   http://localhost:8080/swagger-ui.html (en Docker)"
    echo "   - PgAdmin:    http://localhost:5050"
    echo ""
    echo "✅ Todos los servicios están corriendo en contenedores Docker"
    echo "   Para ver logs: docker-compose -f docker/docker-compose.full.yml logs -f"
    echo "   Para detener:  ./docker/stop-all.sh"
else
    echo "\n🎉 Setup completado (Modo DB-only). Servicios disponibles:"
    echo "   - PostgreSQL: localhost:5432"
    echo "   - PgAdmin:    http://localhost:5050"
    echo ""
    echo "🚀 Iniciando servicios Python y Java localmente..."

# Obtener la ruta absoluta del directorio actual
WORKSPACE_DIR="$(pwd)"

# Función para iniciar servicios
start_services() {
    # Verificar si el comando 'code' está disponible
    if ! command -v code &>/dev/null; then
        echo "⚠️  El comando 'code' no está disponible en tu PATH."
        echo "   Instálalo desde VS Code: Cmd+Shift+P > 'Shell Command: Install code command in PATH'"
        echo "\n   Mientras tanto, abre manualmente dos terminales y ejecuta:"
        echo "   Terminal 1: source venv/bin/activate && python main.py"
        echo "   Terminal 2: cd java-service && ./mvnw spring-boot:run"
        return 1
    fi
    
    # Crear scripts temporales para cada servicio
    PYTHON_SCRIPT="$WORKSPACE_DIR/.vscode_start_python.sh"
    JAVA_SCRIPT="$WORKSPACE_DIR/.vscode_start_java.sh"
    
    # Script para Python
    cat > "$PYTHON_SCRIPT" << 'PYTHON_EOF'
#!/bin/bash
cd "WORKSPACE_PLACEHOLDER"
source venv/bin/activate
echo "🐍 Iniciando servicio Python en http://localhost:8000"
echo "   Documentación: http://localhost:8000/docs"
echo "   Para detener: Ctrl+C"
echo ""
python main.py
PYTHON_EOF
    
    # Script para Java
    cat > "$JAVA_SCRIPT" << 'JAVA_EOF'
#!/bin/bash
cd "WORKSPACE_PLACEHOLDER/java-service"

echo "☕ Iniciando servicio Java en http://localhost:8080"
echo "   Documentación: http://localhost:8080/swagger-ui.html"
echo "   Para detener: Ctrl+C"
echo ""

# Usar mvn21 si existe (wrapper para Java 21), sino mvn normal
if [ -x "./mvn21" ]; then
    ./mvn21 spring-boot:run
else
    mvn spring-boot:run
fi
JAVA_EOF
    
    # Reemplazar placeholder con la ruta real
    sed -i.bak "s|WORKSPACE_PLACEHOLDER|$WORKSPACE_DIR|g" "$PYTHON_SCRIPT"
    sed -i.bak "s|WORKSPACE_PLACEHOLDER|$WORKSPACE_DIR|g" "$JAVA_SCRIPT"
    
    # Hacer ejecutables
    chmod +x "$PYTHON_SCRIPT"
    chmod +x "$JAVA_SCRIPT"
    
    # Limpiar backups
    rm -f "$PYTHON_SCRIPT.bak" "$JAVA_SCRIPT.bak"
    
    # Ejecutar en terminales separadas de VS Code
    # Primero Java (tarda más en arrancar)
    echo "   ☕ Abriendo terminal para servicio Java..."
    osascript -e "
    tell application \"Terminal\"
        do script \"cd '$WORKSPACE_DIR/java-service' && bash '$JAVA_SCRIPT'\"
        activate
    end tell
    " 2>/dev/null &
    
    sleep 1
    
    # Luego Python
    echo "   🐍 Abriendo terminal para servicio Python..."
    osascript -e "
    tell application \"Terminal\"
        do script \"cd '$WORKSPACE_DIR' && bash '$PYTHON_SCRIPT'\"
        activate
    end tell
    " 2>/dev/null &
    
    echo "✅ Servicios iniciados en terminales separadas (Java primero, luego Python)"
    echo ""
    echo "📝 Nota: Los scripts de inicio están en:"
    echo "   - $PYTHON_SCRIPT"
    echo "   - $JAVA_SCRIPT"
    echo "   (Puedes eliminarlos cuando quieras)"
}

# Intentar iniciar servicios locales
if [[ "$OSTYPE" == "darwin"* ]]; then
    start_services
else
    echo "⚠️  Inicio automático de terminales solo disponible en macOS"
    echo "\n🔧 Para iniciar los servicios, ejecuta en terminales separadas:"
    echo "   Terminal 1 (Java):   cd java-service && mvn spring-boot:run"
    echo "   Terminal 2 (Python): source venv/bin/activate && python main.py"
fi

fi  # Cierre del if [ "$USE_DOCKER_FULL" = false ]

echo "\n💡 Para Windows, usa setup_inicia_todo.bat"
echo "\n✨ Setup finalizado exitosamente!"