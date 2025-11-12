@echo off
REM stop-all.bat - Detiene todos los servicios (Docker y locales)

echo.
echo 🛑 Deteniendo todos los servicios...
echo.

REM Detener contenedores Docker (Full)
if exist "docker-compose.full.yml" (
    echo 🐳 Deteniendo contenedores Full Docker...
    docker-compose -f docker-compose.full.yml down
)

REM Detener contenedores Docker (DB-only)
if exist "docker-compose.db-only.yml" (
    echo 🐳 Deteniendo contenedores DB-only...
    docker-compose -f docker-compose.db-only.yml down
)

REM Matar procesos locales Python (main.py, uvicorn)
echo 🐍 Deteniendo procesos Python locales...
taskkill /F /FI "WINDOWTITLE eq *Python Service*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq python.exe" /FI "COMMANDLINE eq *main.py*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq python.exe" /FI "COMMANDLINE eq *uvicorn*" >nul 2>&1

REM Matar procesos locales Java (Spring Boot, Maven)
echo ☕ Deteniendo procesos Java locales...
taskkill /F /FI "WINDOWTITLE eq *Java Service*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq java.exe" /FI "COMMANDLINE eq *spring-boot*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq java.exe" /FI "COMMANDLINE eq *maven*" >nul 2>&1

echo.
echo ✅ Todos los servicios detenidos.
echo.
pause
