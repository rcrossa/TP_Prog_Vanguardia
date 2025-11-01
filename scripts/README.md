# 🛠️ Scripts del Proyecto

Scripts de utilidad para desarrollo, testing y mantenimiento del sistema.

---

## 📋 Lista de Scripts

### 🔐 Gestión de Usuarios

| Script | Descripción | Uso |
|--------|-------------|-----|
| **create_admin.py** | ⚠️ Crear admin con credenciales hardcodeadas (SOLO DESARROLLO) | `python scripts/create_admin.py` |
| **create_admin_secure.py** | ✅ Crear admin de forma segura (variables de entorno o interactivo) | Ver instrucciones abajo |

### 🗄️ Base de Datos

| Script | Descripción | Uso |
|--------|-------------|-----|
| **init_db.py** | Inicializar base de datos con datos de ejemplo | `python scripts/init_db.py` |

### 🧪 Testing y Calidad

| Script | Descripción | Uso |
|--------|-------------|-----|
| **test_integration.sh** | Probar integración Python ↔ Java | `./scripts/test_integration.sh` |
| **check_code_quality.sh** | Verificar calidad del código Python | `./scripts/check_code_quality.sh` |

---

## 📖 Guías de Uso

### 🔐 Crear Usuario Administrador

#### Opción 1: Modo Desarrollo (Rápido) ⚠️

**⚠️ SOLO para desarrollo/testing - Credenciales hardcodeadas**

```bash
python scripts/create_admin.py
```

Crea un admin con:
- Email: `admin@test.com`
- Password: `admin123`

#### Opción 2: Modo Seguro ✅ (Recomendado)

**Con variables de entorno:**

```bash
export ADMIN_NAME="Roberto Admin"
export ADMIN_EMAIL="roberto@unicaba.com"
export ADMIN_PASSWORD="contraseña_super_segura_123"

python scripts/create_admin_secure.py
```

**Modo interactivo (sin variables de entorno):**

```bash
python scripts/create_admin_secure.py

# El script te pedirá:
# - Nombre del administrador
# - Email del administrador
# - Contraseña (oculta mientras escribes)
# - Confirmación de contraseña
```

---

### 🗄️ Inicializar Base de Datos

```bash
# Ejecutar desde la raíz del proyecto
python scripts/init_db.py
```

Este script:
- Crea las tablas si no existen
- Carga datos de ejemplo para desarrollo
- Es idempotente (se puede ejecutar múltiples veces)

---

### 🧪 Probar Integración Python ↔ Java

```bash
# Asegúrate de que ambos servicios estén corriendo:
# Terminal 1: python main.py
# Terminal 2: cd java-service && mvn spring-boot:run

# En Terminal 3:
./scripts/test_integration.sh
```

El script verifica:
- ✅ Python Service (puerto 8000)
- ✅ Java Service (puerto 8080)
- ✅ 4 pruebas de integración
- ✅ Salud de ambos servicios

---

### 📊 Verificar Calidad del Código

```bash
./scripts/check_code_quality.sh
```

Ejecuta herramientas de análisis:
- `flake8` - Linting
- `mypy` - Type checking
- `black --check` - Formato
- `isort --check` - Imports

---

## 🔒 Seguridad

### ⚠️ Advertencias Importantes

1. **create_admin.py** contiene credenciales hardcodeadas
   - ❌ NO usar en producción
   - ✅ Solo para desarrollo local
   - ✅ Las credenciales son de ejemplo conocidas

2. **create_admin_secure.py** es la versión segura
   - ✅ Usar variables de entorno
   - ✅ O modo interactivo con getpass
   - ✅ Contraseñas no se ven en historial de comandos

3. **init_db.py** carga datos de ejemplo
   - ⚠️ Solo ejecutar en desarrollo
   - ❌ NO ejecutar en producción
   - 💡 Ver `docker/init-scripts/01-init.sql` para alternativa

---

## 🚀 Permisos de Ejecución

Los scripts Python con shebang (`#!/usr/bin/env python3`) son ejecutables:

```bash
# Si no son ejecutables, hacerlos ejecutables:
chmod +x scripts/*.py
chmod +x scripts/*.sh

# Ahora puedes ejecutarlos directamente:
./scripts/create_admin_secure.py
./scripts/test_integration.sh
```

---

## 📝 Agregar Nuevos Scripts

Al agregar un nuevo script:

1. **Ubicación:** Colocar en `/scripts`
2. **Shebang:** Agregar `#!/usr/bin/env python3` o `#!/bin/bash` al inicio
3. **Permisos:** `chmod +x scripts/tu_script.py`
4. **Documentación:** Actualizar este README
5. **Seguridad:** NO incluir credenciales hardcodeadas

---

## 🔗 Enlaces Relacionados

- [Documentación Principal](../README.md)
- [Arquitectura del Sistema](../docs/architecture.md)
- [Guía de Integración](../docs/INTEGRACION.md)
- [Scripts de Docker](../docker/README.md)

---

**Última actualización:** 16 de octubre de 2025
**Mantenedor:** Equipo de desarrollo
