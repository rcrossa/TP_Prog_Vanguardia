@echo off
REM setup_inicia_todo.bat - Script de setup para Windows
setlocal enabledelayedexpansion

echo.
echo 🚀 Configurando Plataforma de Gestión de Reservas (Windows)
echo.

REM Verificar dependencias mínimas
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Docker no está instalado. Instálalo antes de continuar.
    exit /b 1
)

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python no está instalado. Instálalo antes de continuar.
    exit /b 1
)

REM Verificar que Docker esté ejecutándose
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Docker no está ejecutándose. Inicia Docker Desktop.
    exit /b 1
)

REM Configurar archivos .env si faltan
if not exist ".env" (
    echo 📝 Creando .env desde plantilla...
    copy .env.example .env
)

REM Generar timestamp para cache busting
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "CACHE_VERSION=%dt:~0,14%"
echo 🔄 Generando versión de caché: %CACHE_VERSION%

REM Actualizar o agregar STATIC_VERSION en .env
findstr /B /C:"STATIC_VERSION=" .env >nul 2>&1
if %errorlevel% equ 0 (
    REM Si existe, reemplazarla (usando PowerShell)
    powershell -Command "(Get-Content .env) -replace '^STATIC_VERSION=.*', 'STATIC_VERSION=%CACHE_VERSION%' | Set-Content .env"
) else (
    REM Si no existe, agregarla
    echo STATIC_VERSION=%CACHE_VERSION% >> .env
)

if not exist "docker\.env" (
    echo 📝 Creando docker\.env desde plantilla...
    copy docker\.env.example docker\.env
)

REM Actualizar o agregar STATIC_VERSION en docker\.env también
findstr /B /C:"STATIC_VERSION=" docker\.env >nul 2>&1
if %errorlevel% equ 0 (
    powershell -Command "(Get-Content docker\.env) -replace '^STATIC_VERSION=.*', 'STATIC_VERSION=%CACHE_VERSION%' | Set-Content docker\.env"
) else (
    echo STATIC_VERSION=%CACHE_VERSION% >> docker\.env
)

REM Selección de stack a levantar
echo.
echo 🔧 ¿Qué stack deseas iniciar?
echo 1) Solo base de datos (db-only) - Python y Java correrán localmente
echo 2) Full stack (Python + Java + DB) - Todo en Docker
set /p "stack_option=Selecciona una opción (1-2, default 1): "

set "stack_file=docker-compose.db-only.yml"
set "USE_DOCKER_FULL=false"

if "%stack_option%"=="2" (
    set "stack_file=docker-compose.full.yml"
    set "USE_DOCKER_FULL=true"
)

cd docker
echo.
echo 🐳 Levantando servicios con %stack_file% ...
docker-compose -f %stack_file% up -d

REM Esperar a que la base de datos esté lista
echo ⏳ Esperando a que PostgreSQL esté listo...
timeout /t 5 /nobreak >nul

REM Obtener POSTGRES_USER del .env
for /f "tokens=2 delims==" %%a in ('findstr /B "POSTGRES_USER=" .env') do set "POSTGRES_USER=%%a"

:check_postgres
docker-compose -f %stack_file% exec -T postgres pg_isready -U %POSTGRES_USER% >nul 2>&1
if %errorlevel% neq 0 (
    timeout /t 2 /nobreak >nul
    goto check_postgres
)
echo ✅ PostgreSQL está listo.

cd ..

REM Solo configurar entorno Python local si NO es modo Full Docker
if "%USE_DOCKER_FULL%"=="false" (
    echo.
    echo 🐍 Configurando entorno virtual Python...
    if not exist "venv" (
        python -m venv venv
        echo ✅ Entorno virtual creado en .\venv
    )

    echo.
    echo 📦 Instalando dependencias Python en el virtualenv...
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
)

REM Mostrar credenciales
echo.
echo 📋 Credenciales configuradas (docker\.env):
findstr /B "POSTGRES_USER= POSTGRES_PASSWORD= PGADMIN_DEFAULT_EMAIL= PGADMIN_DEFAULT_PASSWORD=" docker\.env

REM Crear usuario admin solo si NO es modo Full Docker
if "%USE_DOCKER_FULL%"=="false" (
    echo.
    echo 👤 Creando usuario administrador por defecto...
    if exist "create_admin.py" (
        python create_admin.py || echo ⚠️  No se pudo crear el admin automáticamente. Puedes crearlo manualmente luego.
    ) else (
        echo ⚠️  create_admin.py no encontrado.
    )
)

if "%USE_DOCKER_FULL%"=="true" (
    echo.
    echo 🎉 Setup completado (Modo Full Docker^). Servicios disponibles:
    echo    - PostgreSQL: localhost:5432
    echo    - API Python: http://localhost:8000/docs (en Docker^)
    echo    - API Java:   http://localhost:8080/swagger-ui.html (en Docker^)
    echo    - PgAdmin:    http://localhost:5050
    echo.
    echo ✅ Todos los servicios están corriendo en contenedores Docker
    echo    Para ver logs: docker-compose -f docker\docker-compose.full.yml logs -f
    echo    Para detener:  docker\stop-all.bat
) else (
    echo.
    echo 🎉 Setup completado (Modo DB-only^). Servicios disponibles:
    echo    - PostgreSQL: localhost:5432
    echo    - PgAdmin:    http://localhost:5050
    echo.
    echo 🚀 Para iniciar los servicios Python y Java localmente:
    echo.
    echo 📝 Abre DOS terminales separadas (CMD o PowerShell^) y ejecuta:
    echo.
    echo    Terminal 1 - Servicio Python:
    echo    venv\Scripts\activate
    echo    python main.py
    echo.
    echo    Terminal 2 - Servicio Java:
    echo    cd java-service
    echo    mvnw.cmd spring-boot:run
    echo.
    echo 💡 O usa el script de inicio rápido:
    echo    start_services.bat
)

echo.
echo 💡 Para Mac/Linux, usa setup_inicia_todo.sh
echo.
echo ✨ Setup finalizado exitosamente!
echo.
pause
