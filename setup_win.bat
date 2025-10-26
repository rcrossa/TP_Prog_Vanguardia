@echo off
REM setup_win.bat - Script de instalación y configuración para Windows

REM 1. Crear entorno virtual de Python
python -m venv venv

REM 2. Activar entorno virtual
call venv\Scripts\activate

REM 3. Instalar dependencias Python
pip install -r requirements.txt

REM 4. Copiar archivo de entorno
copy docker\.env.example .env

REM 5. Iniciar base de datos con Docker
cd docker
call docker-compose -f docker-compose.db-only.yml up -d
cd ..

REM 6. Mensaje de finalización
echo.
echo Instalación completada. Revisa .env para credenciales y ejecuta:
echo   python main.py

echo Para iniciar el servicio Java:
echo   cd java-service && mvnw.cmd spring-boot:run

echo Para crear usuario admin:
echo   python scripts\create_admin.py

echo Listo para usar el sistema en http://localhost:8000
