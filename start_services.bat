@echo off
REM start_services.bat - Inicia servicios Python y Java en modo DB-only

echo.
echo 🚀 Iniciando servicios locales...
echo.

REM Verificar que no estemos en modo Full Docker
findstr /B "USE_DOCKER_FULL=true" .env >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Estás en modo Full Docker. Los servicios ya están corriendo en contenedores.
    echo    Para ver logs: docker-compose -f docker\docker-compose.full.yml logs -f
    exit /b 0
)

REM Iniciar servicio Python en nueva terminal
start "🐍 Python Service (FastAPI)" cmd /k "venv\Scripts\activate && python main.py"

REM Esperar 2 segundos
timeout /t 2 /nobreak >nul

REM Iniciar servicio Java en nueva terminal
start "☕ Java Service (Spring Boot)" cmd /k "cd java-service && mvnw.cmd spring-boot:run"

echo.
echo ✅ Servicios iniciados en ventanas separadas:
echo    - Python: http://localhost:8000/docs
echo    - Java:   http://localhost:8080/swagger-ui.html
echo.
echo 💡 Para detener todos los servicios, ejecuta: docker\stop-all.bat
echo.
pause
