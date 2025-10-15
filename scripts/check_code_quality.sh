#!/bin/bash
# Script de utilidad para mantener la calidad del código

echo "🧹 Verificador y Limpiador de Código - Sistema de Reservas"
echo "========================================================="

PROJECT_DIR="/Users/robertorossa/Desktop/Unicaba/Tercer cuatrimestre/Programacion de vanguardia/Python/TP_Prog_Vanguardia"
cd "$PROJECT_DIR"

# Función para verificar trailing whitespace
check_trailing_whitespace() {
    echo "🔍 Verificando trailing whitespace..."
    files_with_whitespace=$(find ./app ./scripts -name "*.py" -exec grep -l " $" {} \;)
    
    if [ -z "$files_with_whitespace" ]; then
        echo "   ✅ No hay trailing whitespace"
        return 0
    else
        echo "   ⚠️  Archivos con trailing whitespace:"
        echo "$files_with_whitespace"
        return 1
    fi
}

# Función para limpiar trailing whitespace
clean_trailing_whitespace() {
    echo "🧹 Limpiando trailing whitespace..."
    find ./app ./scripts -name "*.py" -exec sed -i '' 's/[[:space:]]*$//' {} \;
    echo "   ✅ Trailing whitespace eliminado"
}

# Función para verificar imports
check_imports() {
    echo "🔍 Verificando imports..."
    ./venv/bin/python -c "
try:
    from app.models import Persona, Articulo, Sala, Reserva
    from app.schemas import PersonaCreate, ArticuloCreate
    from app.core.config import settings
    print('   ✅ Todos los imports funcionan')
except ImportError as e:
    print(f'   ❌ Error de import: {e}')
    exit(1)
"
}

# Función para verificar aplicación
check_app() {
    echo "🔍 Verificando aplicación FastAPI..."
    ./venv/bin/python -c "
from main import app
from fastapi.testclient import TestClient

try:
    client = TestClient(app)
    response = client.get('/')
    if response.status_code == 200:
        print('   ✅ Aplicación FastAPI funcionando')
    else:
        print(f'   ❌ Error en aplicación: {response.status_code}')
        exit(1)
except Exception as e:
    print(f'   ❌ Error: {e}')
    exit(1)
"
}

# Ejecutar verificaciones
echo ""
echo "📋 Ejecutando verificaciones..."
echo ""

check_trailing_whitespace
whitespace_status=$?

check_imports
check_app

echo ""
if [ $whitespace_status -ne 0 ]; then
    echo "🚨 Se encontraron problemas de formato. ¿Quieres limpiarlos? (y/n)"
    read -r response
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        clean_trailing_whitespace
        echo "✅ Problemas de formato corregidos"
    fi
else
    echo "🎉 ¡Código limpio y funcionando correctamente!"
fi

echo ""
echo "💡 Consejos:"
echo "   - Usa .editorconfig en tu editor para prevenir trailing whitespace"
echo "   - Ejecuta este script antes de hacer commits"
echo "   - Mantén los docstrings actualizados"