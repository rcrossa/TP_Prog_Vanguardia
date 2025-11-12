# Scripts de Setup y Gestión

## 📋 Descripción

Este proyecto incluye scripts automatizados para configurar e iniciar la plataforma de reservas en diferentes sistemas operativos y modos de ejecución.

## 🚀 Scripts Principales

### Setup (Configuración Inicial)

| Script | Sistema | Descripción |
|--------|---------|-------------|
| `setup_inicia_todo.sh` | Mac/Linux | Configuración completa con selección de modo |
| `setup_inicia_todo.bat` | Windows | Configuración completa con selección de modo |

### Gestión de Servicios

| Script | Sistema | Descripción |
|--------|---------|-------------|
| `start_services.bat` | Windows | Inicia Python y Java en modo DB-only |
| `docker/stop-all.sh` | Mac/Linux | Detiene todos los servicios (Docker + locales) |
| `docker/stop-all.bat` | Windows | Detiene todos los servicios (Docker + locales) |

## 🔧 Modos de Ejecución

### 1. DB-only (Base de datos en Docker)

**Características:**
- ✅ PostgreSQL en contenedor Docker
- ✅ PgAdmin en contenedor Docker
- ✅ Python (FastAPI) ejecutándose localmente
- ✅ Java (Spring Boot) ejecutándose localmente

**Cuándo usar:**
- Desarrollo activo con debugging
- Necesitas modificar código frecuentemente
- Quieres ver logs directamente en la terminal

**Cómo iniciar:**
```bash
# Mac/Linux
./setup_inicia_todo.sh
# Seleccionar opción 1

# Windows
setup_inicia_todo.bat
# Seleccionar opción 1
```

### 2. Full Docker (Todo en contenedores)

**Características:**
- ✅ PostgreSQL en contenedor Docker
- ✅ PgAdmin en contenedor Docker
- ✅ Python (FastAPI) en contenedor Docker
- ✅ Java (Spring Boot) en contenedor Docker

**Cuándo usar:**
- Ambiente de producción
- Testing de integración
- Quieres ambiente aislado completo

**Cómo iniciar:**
```bash
# Mac/Linux
./setup_inicia_todo.sh
# Seleccionar opción 2

# Windows
setup_inicia_todo.bat
# Seleccionar opción 2
```

## 📝 Guías de Uso

### Primera vez (Mac/Linux)

```bash
# 1. Dar permisos de ejecución
chmod +x setup_inicia_todo.sh

# 2. Ejecutar setup
./setup_inicia_todo.sh

# 3. Seleccionar modo (1 o 2)
```

### Primera vez (Windows)

```cmd
REM 1. Ejecutar setup
setup_inicia_todo.bat

REM 2. Seleccionar modo (1 o 2)
```

### Modo DB-only: Iniciar servicios locales

**Mac/Linux:**
```bash
# Terminal 1 - Python
source venv/bin/activate
python main.py

# Terminal 2 - Java
cd java-service
./mvnw spring-boot:run
```

**Windows:**
```cmd
REM Opción 1: Script automático
start_services.bat

REM Opción 2: Manual
REM Terminal 1 - Python
venv\Scripts\activate
python main.py

REM Terminal 2 - Java
cd java-service
mvnw.cmd spring-boot:run
```

### Detener todos los servicios

**Mac/Linux:**
```bash
./docker/stop-all.sh
```

**Windows:**
```cmd
docker\stop-all.bat
```

## 🔄 Cache Busting

Ambos scripts de setup generan automáticamente una versión de caché (`STATIC_VERSION`) basada en timestamp para invalidar la caché del browser:

- **Mac/Linux**: `STATIC_VERSION=$(date +%s)`
- **Windows**: `STATIC_VERSION=%dt:~0,14%`

Esta versión se agrega a `.env` y `docker/.env`, y se usa en todas las plantillas HTML para forzar la recarga de archivos estáticos (CSS/JS).

## 📊 Servicios y Puertos

| Servicio | Puerto | URL |
|----------|--------|-----|
| PostgreSQL | 5432 | `localhost:5432` |
| PgAdmin | 5050 | `http://localhost:5050` |
| API Python | 8000 | `http://localhost:8000/docs` |
| API Java | 8080 | `http://localhost:8080/swagger-ui.html` |

## ⚙️ Variables de Entorno

Los scripts configuran automáticamente:

- `STATIC_VERSION`: Timestamp para cache busting
- `USE_DOCKER_FULL`: `true` o `false` según modo seleccionado
- Credenciales de PostgreSQL y PgAdmin (desde `.env.example`)

## 🐛 Troubleshooting

### Error: Docker no está ejecutándose

**Solución:**
1. Inicia Docker Desktop
2. Espera a que esté completamente iniciado
3. Vuelve a ejecutar el script

### Error: Python no encontrado

**Solución:**
1. Instala Python 3.11+ desde [python.org](https://www.python.org/downloads/)
2. Verifica: `python --version`
3. Vuelve a ejecutar el script

### Servicios no inician en modo DB-only

**Mac/Linux:**
```bash
# Verificar virtualenv
source venv/bin/activate
which python  # Debe apuntar a venv/bin/python

# Verificar dependencias
pip list | grep fastapi
```

**Windows:**
```cmd
REM Verificar virtualenv
venv\Scripts\activate
where python  REM Debe apuntar a venv\Scripts\python.exe

REM Verificar dependencias
pip list | findstr fastapi
```

### Caché del browser no se limpia

**Solución:**
1. Verifica que `.env` tenga `STATIC_VERSION=<timestamp>`
2. Reinicia el servicio Python
3. Hard refresh en browser: `Ctrl+Shift+R` (Windows/Linux) o `Cmd+Shift+R` (Mac)

## 📚 Documentación Relacionada

- [Arquitectura del Sistema](docs/architecture.md)
- [Guía de Docker](docs/docker_guide.md)
- [Configuración de Entorno](docs/configuracion_entorno.md)
- [Cache Busting](docs/cache_busting.md)

## 💡 Tips

1. **Desarrollo activo**: Usa modo DB-only para debugging
2. **Testing completo**: Usa modo Full Docker antes de commits
3. **Cambios de código**: En Full Docker, reconstruye con `docker-compose up -d --build`
4. **Logs en Full Docker**: `docker-compose -f docker/docker-compose.full.yml logs -f`
5. **Limpiar todo**: `./docker/stop-all.sh` y `docker system prune -a` (cuidado!)
