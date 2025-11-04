
@echo off
REM setup_win.bat - Instalación automática para Windows
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   Plataforma de Gestión de Reservas - Setup Windows
echo ============================================================
echo.

REM Validar que Docker esté ejecutándose
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no esta ejecutandose. Inicia Docker Desktop antes de continuar.
    exit /b 1
)

REM Validar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado. Instalalo desde python.org
    exit /b 1
)

echo [1/9] Configurando archivos de entorno...
REM Copiar archivos de entorno si faltan
if not exist .env (
    copy .env.example .env >nul
    echo   - .env creado desde plantilla
)
if not exist docker\.env (
    copy docker\.env.example docker\.env >nul
    echo   - docker\.env creado desde plantilla
)

echo.
echo [2/9] Que stack deseas iniciar?
echo   1) Solo base de datos (db-only) - Por defecto
echo   2) Full stack (Python + Java + DB)
set /p stack_option="Selecciona una opcion (1-2, default 1): "
set stack_file=docker-compose.db-only.yml
if "%stack_option%"=="2" set stack_file=docker-compose.full.yml

echo.
echo [3/9] Levantando servicios con %stack_file%...
cd docker
docker-compose -f %stack_file% up -d
if errorlevel 1 (
    echo [ERROR] No se pudo levantar Docker Compose
    cd ..
    exit /b 1
)

REM Esperar a que PostgreSQL esté listo
echo.
echo [4/9] Esperando a que PostgreSQL este listo...
for /L %%i in (1,1,20) do (
    docker-compose exec -T postgres pg_isready -U postgres >nul 2>&1
    if not errorlevel 1 (
        echo   - PostgreSQL esta listo
        goto :postgres_ready
    )
    timeout /t 2 >nul
)
echo   - [ADVERTENCIA] PostgreSQL puede no estar completamente listo
:postgres_ready
cd ..

echo.
echo [5/9] Configurando entorno virtual Python...
REM Crear entorno virtual si no existe
if not exist venv (
    python -m venv venv
    echo   - Entorno virtual creado en venv\
) else (
    echo   - Entorno virtual ya existe
)

REM Activar entorno virtual
call venv\Scripts\activate

echo.
echo [6/9] Instalando dependencias Python...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo   - Dependencias instaladas correctamente

echo.
echo [7/9] Mostrando credenciales configuradas:
findstr /B /C:"POSTGRES_USER" /C:"POSTGRES_PASSWORD" /C:"PGADMIN_DEFAULT_EMAIL" /C:"PGADMIN_DEFAULT_PASSWORD" docker\.env | findstr /V /C:"#"

echo.
echo [8/9] Creando usuario administrador por defecto...
if exist create_admin.py (
    python create_admin.py
    if errorlevel 1 (
        echo   - [ADVERTENCIA] No se pudo crear el admin automaticamente
    )
) else (
    echo   - [ADVERTENCIA] create_admin.py no encontrado
)

echo.
echo [9/9] Servicios disponibles:
echo   - PostgreSQL: localhost:5432
echo   - API Python: http://localhost:8000/docs
echo   - API Java:   http://localhost:8080/swagger-ui.html
echo   - PgAdmin:    http://localhost:5050

echo.
echo ============================================================
echo   Setup completado exitosamente
echo ============================================================
echo.

REM Preguntar si desea iniciar los servicios automáticamente
set /p auto_start="Deseas iniciar los servicios Java y Python automaticamente? (S/N, default N): "
if /i "%auto_start%"=="S" goto :start_services
if /i "%auto_start%"=="s" goto :start_services

echo.
echo Proximos pasos manuales:
echo   1. En una terminal, ejecuta el servicio Java:
echo      cd java-service ^&^& mvnw.cmd spring-boot:run
echo   2. En otra terminal, ejecuta el servicio Python:
echo      venv\Scripts\activate ^&^& python main.py
echo   3. Accede a la API y frontend en los puertos indicados
echo.
goto :end

:start_services
echo.
echo Iniciando servicios en ventanas separadas...

REM Crear script temporal para Java
set JAVA_SCRIPT=%CD%\.vscode_start_java.bat
(
echo @echo off
echo cd /d "%CD%\java-service"
echo echo.
echo echo ============================================================
echo echo   Servicio Java - Spring Boot
echo echo ============================================================
echo echo   URL: http://localhost:8080
echo echo   Documentacion: http://localhost:8080/swagger-ui.html
echo echo   Para detener: Ctrl+C
echo echo ============================================================
echo echo.
echo mvnw.cmd spring-boot:run
) > "%JAVA_SCRIPT%"

REM Crear script temporal para Python
set PYTHON_SCRIPT=%CD%\.vscode_start_python.bat
(
echo @echo off
echo cd /d "%CD%"
echo call venv\Scripts\activate
echo echo.
echo echo ============================================================
echo echo   Servicio Python - FastAPI
echo echo ============================================================
echo echo   URL: http://localhost:8000
echo echo   Documentacion: http://localhost:8000/docs
echo echo   Para detener: Ctrl+C
echo echo ============================================================
echo echo.
echo python main.py
) > "%PYTHON_SCRIPT%"

REM Iniciar Java primero (tarda más en arrancar)
echo   - Abriendo terminal para servicio Java...
start "Java Service - Spring Boot" cmd /k "%JAVA_SCRIPT%"
timeout /t 2 >nul

REM Luego Python
echo   - Abriendo terminal para servicio Python...
start "Python Service - FastAPI" cmd /k "%PYTHON_SCRIPT%"

echo.
echo Servicios iniciados en ventanas separadas:
echo   1. Java Service (Spring Boot) - Tarda ~30-60s en arrancar
echo   2. Python Service (FastAPI) - Tarda ~5-10s en arrancar
echo.
echo Los scripts de inicio estan en:
echo   - %JAVA_SCRIPT%
echo   - %PYTHON_SCRIPT%
echo   (Puedes eliminarlos cuando quieras)
echo.

:end
endlocal
