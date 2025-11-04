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

echo "\n🚀 Iniciando servicios en terminales separadas de VS Code..."

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
mvn spring-boot:run
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

# Intentar iniciar servicios
if [[ "$OSTYPE" == "darwin"* ]]; then
    start_services
else
    echo "⚠️  Inicio automático de terminales solo disponible en macOS"
    echo "\n🔧 Para iniciar los servicios, ejecuta en terminales separadas:"
    echo "   Terminal 1 (Java):   cd java-service && mvn spring-boot:run"
    echo "   Terminal 2 (Python): source venv/bin/activate && python main.py"
fi

echo "\n💡 Para Windows, usa setup_win.bat."

echo "\n� Iniciando servicios en terminales separadas..."

# Obtener la ruta absoluta del directorio actual
WORKSPACE_DIR="$(pwd)"

# Crear un archivo temporal con los comandos para el terminal de Python
PYTHON_CMD_FILE="/tmp/vscode_python_cmd.sh"
cat > "$PYTHON_CMD_FILE" << 'EOF'
#!/bin/bash
cd "$WORKSPACE_DIR"
source venv/bin/activate
echo "🐍 Iniciando servicio Python..."
python main.py
EOF

# Crear un archivo temporal con los comandos para el terminal de Java
JAVA_CMD_FILE="/tmp/vscode_java_cmd.sh"
cat > "$JAVA_CMD_FILE" << 'EOF'
#!/bin/bash
cd "$WORKSPACE_DIR/java-service"
echo "☕ Iniciando servicio Java..."
./mvnw spring-boot:run
EOF

# Reemplazar $WORKSPACE_DIR en los archivos temporales
sed -i.bak "s|\$WORKSPACE_DIR|$WORKSPACE_DIR|g" "$PYTHON_CMD_FILE"
sed -i.bak "s|\$WORKSPACE_DIR|$WORKSPACE_DIR|g" "$JAVA_CMD_FILE"

# Hacer ejecutables los scripts temporales
chmod +x "$PYTHON_CMD_FILE"
chmod +x "$JAVA_CMD_FILE"

# Verificar si estamos ejecutando desde VS Code
if [ -n "$VSCODE_IPC_HOOK_CLI" ] || [ -n "$TERM_PROGRAM" ]; then
    # Ejecutar comandos en terminales de VS Code usando AppleScript (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Terminal para Python
        osascript -e "
        tell application \"Visual Studio Code\"
            activate
        end tell
        " 2>/dev/null
        
        # Usar 'code' CLI para abrir terminales
        code --new-window "$WORKSPACE_DIR" 2>/dev/null || true
        
        # Esperar un poco para que VS Code esté listo
        sleep 1
        
        # Crear terminal de Python
        osascript <<-APPLESCRIPT
        tell application "System Events"
            tell process "Code"
                keystroke "t" using {control down, shift down}
                delay 0.5
            end tell
        end tell
APPLESCRIPT
        
        # Enviar comando de Python
        sleep 0.5
        osascript -e 'tell application "System Events" to keystroke "source venv/bin/activate && python main.py"'
        osascript -e 'tell application "System Events" to keystroke return'
        
        # Esperar un poco
        sleep 1
        
        # Crear terminal de Java
        osascript <<-APPLESCRIPT
        tell application "System Events"
            tell process "Code"
                keystroke "t" using {control down, shift down}
                delay 0.5
            end tell
        end tell
APPLESCRIPT
        
        # Enviar comando de Java
        sleep 0.5
        osascript -e 'tell application "System Events" to keystroke "cd java-service && ./mvnw spring-boot:run"'
        osascript -e 'tell application "System Events" to keystroke return'
        
        echo "✅ Servicios iniciados en terminales separadas de VS Code"
    else
        # Para Linux, usar una aproximación diferente
        echo "⚠️  Inicio automático de terminales solo disponible en macOS"
        echo "   Por favor, abre manualmente dos terminales y ejecuta:"
        echo "   Terminal 1: source venv/bin/activate && python main.py"
        echo "   Terminal 2: cd java-service && ./mvnw spring-boot:run"
    fi
else
    # Si no estamos en VS Code, mostrar instrucciones
    echo "\n🔧 Para iniciar los servicios, ejecuta en terminales separadas:"
    echo "   Terminal 1 (Python): source venv/bin/activate && python main.py"
    echo "   Terminal 2 (Java):   cd java-service && ./mvnw spring-boot:run"
fi

# Limpiar archivos temporales
rm -f "$PYTHON_CMD_FILE" "$PYTHON_CMD_FILE.bak" "$JAVA_CMD_FILE" "$JAVA_CMD_FILE.bak"

echo "\n💡 Para Windows, usa setup_win.bat."