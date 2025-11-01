# 🧹 Estándares de Formato de Código

## 📋 Configuración de Calidad de Código

El proyecto mantiene altos estándares de calidad de código mediante herramientas automatizadas y configuraciones específicas.

## 🛠️ Herramientas Configuradas

### 1. `.editorconfig`
Configuración automática para editores:
```ini
root = true

[*]
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_style = space
indent_size = 4
```

### 2. `pyproject.toml`
Configuración de herramientas de desarrollo:
```toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 88
known_first_party = ["app"]

[flake8]
max-line-length = 88
```

### 3. Script de Verificación
`scripts/check_code_quality.sh` - Herramienta de verificación que:
- ✅ Verifica trailing whitespace
- ✅ Prueba imports de módulos
- ✅ Valida que la aplicación FastAPI funcione
- 🧹 Ofrece limpieza automática de formato

## 🚀 Uso de Herramientas

### Verificación Manual
```bash
# Ejecutar script de verificación
./scripts/check_code_quality.sh
```

### Formateo Automático (Opcional)
```bash
# Instalar herramientas (opcional)
pip install black isort flake8

# Formatear código
black app/
isort app/

# Verificar estilo
flake8 app/
```

## � Estándares del Proyecto

### Documentación
- **Módulos**: Todos tienen docstring explicativo al inicio
- **Clases**: Documentadas con propósito y funcionalidad
- **Métodos**: Documentación en métodos públicos importantes

### Formato de Código
- **Líneas**: Máximo 88 caracteres
- **Indentación**: 4 espacios para Python
- **Imports**: Organizados con isort
- **Sin trailing whitespace**: Limpieza automática

### Estructura
```
app/
├── models/          # Modelos SQLAlchemy documentados
├── schemas/         # Esquemas Pydantic documentados
├── repositories/    # Capa de acceso a datos
├── services/        # Lógica de negocio
└── api/            # Endpoints REST
```

## 🎯 Beneficios

- ✅ **Código limpio y consistente**
- ✅ **Documentación completa**
- ✅ **Configuración automatizada**
- ✅ **Fácil mantenimiento**
- ✅ **Listo para colaboración**