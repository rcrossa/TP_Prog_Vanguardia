
@echo off
REM setup_win.bat - Instalación automática para Windows

echo.
echo ===== Plataforma de Gestión de Reservas - Setup Windows =====

REM 1. Crear entorno virtual si no existe
if not exist venv (
	python -m venv venv
	echo Entorno virtual creado en venv\
)

REM 2. Activar entorno virtual
call venv\Scripts\activate

REM 3. Instalar dependencias Python
echo Instalando dependencias Python...
pip install --upgrade pip
pip install -r requirements.txt

REM 4. Copiar archivos de entorno si faltan
if not exist .env (
	copy .env.example .env
	echo Archivo .env creado desde plantilla.
)
if not exist docker\.env (
	copy docker\.env.example docker\.env
	echo Archivo docker\.env creado desde plantilla.
)

REM 5. Iniciar base de datos con Docker
cd docker
echo Levantando base de datos con Docker Compose...
docker-compose -f docker-compose.db-only.yml up -d
cd ..

REM 6. Esperar a que la base de datos esté lista
echo Esperando 10 segundos a que PostgreSQL esté listo...
timeout /t 10 >nul

REM 7. Crear usuario admin automáticamente
if exist scripts\create_admin.py (
	echo Creando usuario administrador por defecto...
	python scripts\create_admin.py
)

REM 8. Mostrar credenciales
echo.
echo Credenciales configuradas (docker/.env):
findstr /B /C:"POSTGRES_USER" /C:"POSTGRES_PASSWORD" /C:"PGADMIN_DEFAULT_EMAIL" /C:"PGADMIN_DEFAULT_PASSWORD" docker\.env

echo.
echo Instalación completada. Servicios disponibles:
echo   - PostgreSQL: localhost:5432
echo   - API Python: http://localhost:8000/docs
echo   - API Java:   http://localhost:8080/swagger-ui.html
echo   - PgAdmin:    http://localhost:5050

echo.
echo ===== Próximos pasos =====
echo   1. Ejecuta: python main.py
echo   2. En otra terminal, ejecuta el servicio Java:
echo      cd java-service && mvnw.cmd spring-boot:run
echo   3. Accede a la API y frontend en los puertos indicados.
echo.
