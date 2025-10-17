# 🐳 Guía de Docker - Sistema de Reservas

Esta guía está diseñada para facilitar el uso de Docker en el proyecto, especialmente para personas que no están familiarizadas con contenedores.

## 📋 Tabla de Contenidos

1. [Modos de Uso](#modos-de-uso)
2. [Inicio Rápido](#inicio-rápido)
3. [Configuración de Memoria](#configuración-de-memoria)
4. [URLs de Acceso](#urls-de-acceso)
5. [Comandos Útiles](#comandos-útiles)
6. [Troubleshooting](#troubleshooting)
7. [Guía para Evaluadores](#guía-para-evaluadores)

---

## 🎯 Modos de Uso

El proyecto ofrece **DOS modos de trabajo** con Docker:

### Modo 1: HÍBRIDO (Recomendado para Desarrollo) 🔧

**¿Qué es?** Solo la base de datos corre en Docker. Los servicios (Python/Java) los ejecutas manualmente en tu máquina.

**¿Cuándo usar?**
- ✅ Estás desarrollando código
- ✅ Quieres usar tu IDE favorito (VSCode, IntelliJ, PyCharm)
- ✅ Necesitas hacer debugging
- ✅ Quieres hot-reload automático al guardar archivos

**Memoria requerida:** ~768 MB

**¿Cómo iniciar?**
```bash
./start-db-only.sh
```

Luego ejecuta manualmente:
- **Python:** `uvicorn main:app --reload --port 8000`
- **Java:** Desde tu IDE o `mvn spring-boot:run` en `java-service/`

---

### Modo 2: FULL STACK (Todo en Docker) 🚀

**¿Qué es?** Todo el sistema corre en contenedores: base de datos, Python, Java y pgAdmin.

**¿Cuándo usar?**
- ✅ Quieres demostrar el proyecto funcionando
- ✅ Necesitas un ambiente consistente para evaluación
- ✅ Quieres compartir el proyecto fácilmente
- ✅ No quieres instalar Python/Java en tu máquina

**Memoria requerida:** ~1.6 GB

**¿Cómo iniciar?**
```bash
./start-full.sh
```

Espera ~30 segundos para que todos los servicios inicien correctamente.

---

## 🚀 Inicio Rápido

### Prerrequisitos

1. **Docker Desktop instalado** (versión 20.10 o superior)
   - macOS: [Descargar aquí](https://www.docker.com/products/docker-desktop)
   - Windows: [Descargar aquí](https://www.docker.com/products/docker-desktop)
   - Linux: `sudo apt-get install docker-ce docker-compose`

2. **Verificar instalación:**
   ```bash
   docker --version
   docker-compose --version
   ```

### Primera Vez - Setup Inicial

```bash
# 1. Ir a la carpeta docker
cd docker

# 2. Crear archivo de configuración (IMPORTANTE)
cp .env.example .env

# 3. (Opcional) Editar .env si necesitas cambiar puertos o credenciales
nano .env

# 4. Dar permisos de ejecución a los scripts (solo la primera vez)
chmod +x *.sh

# 5. Elegir tu modo:

# Opción A: Modo Híbrido (desarrollo)
./start-db-only.sh

# Opción B: Modo Full Stack (demo/evaluación)
./start-full.sh
```

### ⚙️ Variables de Entorno (`.env`)

**IMPORTANTE:** El proyecto usa un archivo `.env` para configuración. Este archivo:
- ✅ Permite personalizar puertos, credenciales y límites de memoria
- ✅ Facilita cambiar configuración sin editar docker-compose
- ✅ Es ignorado por Git (no se sube al repositorio por seguridad)

**Valores por defecto** (en `.env.example`):
```bash
# Base de datos
POSTGRES_DB=reservas_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123

# Puertos
POSTGRES_PORT=5432
PYTHON_SERVICE_PORT=8000
JAVA_SERVICE_PORT=8080
PGADMIN_PORT=5050

# Límites de memoria
POSTGRES_MEMORY_LIMIT=512m
PYTHON_MEMORY_LIMIT=384m
JAVA_MEMORY_LIMIT=512m
PGADMIN_MEMORY_LIMIT=256m
```

Para cambiar cualquier valor, edita el archivo `.env` (no `.env.example`).

---

## 💾 Configuración de Memoria

Los contenedores tienen límites de memoria configurables desde el archivo `.env`:

| Servicio | Límite (default) | Reservado | CPU | Variable `.env` |
|----------|------------------|-----------|-----|-----------------|
| **PostgreSQL** | 512 MB | 256 MB | 0.5 | `POSTGRES_MEMORY_LIMIT` |
| **Python Service** | 384 MB | 192 MB | 0.5 | `PYTHON_MEMORY_LIMIT` |
| **Java Service** | 512 MB | 256 MB | 0.5 | `JAVA_MEMORY_LIMIT` |
| **pgAdmin** | 256 MB | 128 MB | 0.25 | `PGADMIN_MEMORY_LIMIT` |
| | | | | |
| **TOTAL Híbrido** | ~768 MB | - | - | DB + pgAdmin |
| **TOTAL Full** | ~1.6 GB | - | - | Todo incluido |

### ¿Por qué estos límites?

- **Prevención:** Evita que Docker consuma toda la RAM de tu computadora
- **Consistencia:** Garantiza que funcione igual en todas las máquinas
- **Eficiencia:** Java con `-Xmx384m` es suficiente para el proyecto
- **Configurabilidad:** Puedes cambiar los límites en `.env` según tu hardware

### Personalizar límites de memoria:

Edita el archivo `.env`:
```bash
# Ejemplo: Aumentar límite de Java a 1GB
JAVA_MEMORY_LIMIT=1024m
JAVA_XMX=768m

# Ejemplo: Reducir límite de Python para laptops con poca RAM
PYTHON_MEMORY_LIMIT=256m
```

### Verificar uso de memoria:

```bash
docker stats
```

---

## 🌐 URLs de Acceso

Una vez iniciado, puedes acceder a:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Python API** | http://localhost:8000 | API FastAPI |
| **Python Docs** | http://localhost:8000/docs | Swagger UI (Python) |
| **Java API** | http://localhost:8080 | API Spring Boot |
| **Java Docs** | http://localhost:8080/swagger-ui.html | Swagger UI (Java) |
| **pgAdmin** | http://localhost:5050 | Administrador de DB |
| **PostgreSQL** | localhost:5432 | Conexión directa DB |

### Credenciales pgAdmin:

- **Email:** `admin@admin.com`
- **Password:** `admin`

### Conexión a PostgreSQL desde pgAdmin:

1. Ir a http://localhost:5050
2. Login con las credenciales arriba
3. Clic derecho en "Servers" → "Create" → "Server"
4. **General tab:**
   - Name: `Reservas DB`
5. **Connection tab:**
   - Host: `postgres` (en modo full) o `localhost` (en modo híbrido)
   - Port: `5432`
   - Database: `reservas_db`
   - Username: `postgres`
   - Password: `postgres123`

---

## 🛠️ Comandos Útiles

### Gestión Básica

```bash
# Iniciar modo híbrido
./start-db-only.sh

# Iniciar modo full stack
./start-full.sh

# Detener TODO (limpia todos los contenedores)
./stop-all.sh

# Ver logs de un servicio específico
docker-compose -f docker-compose.full.yml logs python-service
docker-compose -f docker-compose.full.yml logs java-service
docker-compose -f docker-compose.db-only.yml logs postgres

# Ver logs en tiempo real
docker-compose -f docker-compose.full.yml logs -f python-service
```

### Verificación de Estado

```bash
# Ver contenedores corriendo
docker ps

# Ver uso de recursos (memoria, CPU)
docker stats

# Ver logs de todos los servicios
docker-compose -f docker-compose.full.yml logs

# Verificar salud de servicios
docker-compose -f docker-compose.full.yml ps
```

### Limpieza Avanzada

```bash
# Detener y eliminar contenedores
./stop-all.sh

# Eliminar volúmenes de datos (¡CUIDADO! Borra la DB)
docker volume rm docker_postgres_data

# Eliminar imágenes no usadas
docker image prune -a

# Limpieza completa (libera mucho espacio)
docker system prune -a --volumes
```

---

## 🔧 Troubleshooting

### Problema: "Port already in use"

**Síntoma:** Error al iniciar Docker diciendo que el puerto 5432, 8000 u 8080 está ocupado.

**Solución:**
```bash
# Verificar qué está usando el puerto
lsof -i :5432  # PostgreSQL
lsof -i :8000  # Python
lsof -i :8080  # Java

# Opción 1: Detener el proceso que lo usa
# Opción 2: Cambiar el puerto en .env
nano .env
# Cambia: POSTGRES_PORT=5433 (o cualquier otro puerto libre)
```

---

### Problema: "Cannot find .env file" o variables no se cargan

**Síntoma:** Docker no encuentra las variables de configuración.

**Solución:**
```bash
# Verificar que el archivo .env exista
cd docker
ls -la .env

# Si no existe, crearlo desde el template
cp .env.example .env

# Verificar que Docker Compose lo detecta
docker-compose -f docker-compose.full.yml config | grep POSTGRES_DB
# Debe mostrar: POSTGRES_DB: reservas_db
```

---

### Problema: "Cannot connect to Docker daemon"

**Síntoma:** Error diciendo que Docker no está corriendo.

**Solución:**
1. Abrir Docker Desktop
2. Esperar a que el ícono de Docker en la barra superior diga "Docker is running"
3. Intentar nuevamente

---

### Problema: "Out of memory" o servicios lentos

**Síntoma:** Los contenedores se reinician constantemente o van muy lentos.

**Solución:**
1. Verificar memoria disponible: `docker stats`
2. Cerrar otras aplicaciones pesadas
3. En Docker Desktop → Settings → Resources → Aumentar memoria asignada a Docker
4. Usar modo híbrido si tu máquina tiene poca RAM

---

### Problema: "Database connection refused"

**Síntoma:** Los servicios no pueden conectarse a PostgreSQL.

**Solución en modo FULL:**
```bash
# 1. Verificar que postgres esté corriendo
docker ps | grep postgres

# 2. Ver logs de postgres
docker-compose -f docker-compose.full.yml logs postgres

# 3. Esperar a que postgres esté "ready to accept connections"
# A veces tarda ~10 segundos en iniciar
```

**Solución en modo HÍBRIDO:**
```bash
# Los servicios manuales deben usar localhost:5432, NO postgres:5432
# Verificar en application.properties (Java) o config.py (Python)
```

---

### Problema: "Java service crashes immediately"

**Síntoma:** El contenedor Java se inicia y se detiene enseguida.

**Solución:**
```bash
# Ver logs completos del error
docker-compose -f docker-compose.full.yml logs java-service

# Verificar que el JAR exista
docker-compose -f docker-compose.full.yml run java-service ls -lh /app/

# Reconstruir el JAR
cd ../java-service
mvn clean package
cd ../docker
./start-full.sh
```

---

### Problema: "Python hot reload doesn't work in full mode"

**Síntoma:** Cambias código Python pero no se refleja en el contenedor.

**Explicación:** El modo full usa volúmenes montados, los cambios SÍ deberían reflejarse.

**Solución:**
```bash
# 1. Verificar que el volumen esté montado
docker inspect reservas_python | grep Mounts -A 20

# 2. Si no funciona, reiniciar el servicio
docker-compose -f docker-compose.full.yml restart python-service

# 3. Para desarrollo activo, mejor usa modo híbrido
./stop-all.sh
./start-db-only.sh
uvicorn main:app --reload
```

---

### Problema: Scripts no ejecutan (Permission denied)

**Síntoma:** Al correr `./start-full.sh` dice "Permission denied".

**Solución:**
```bash
chmod +x *.sh
```

---

### Limpieza Completa (Último Recurso)

Si nada funciona, borra todo y empieza de cero:

```bash
# 1. Detener TODO
./stop-all.sh

# 2. Eliminar contenedores, volúmenes e imágenes
docker system prune -a --volumes

# 3. Reiniciar Docker Desktop

# 4. Reconstruir servicios
cd ../java-service
mvn clean package
cd ../docker
./start-full.sh
```

---

## 👨‍🏫 Guía para Evaluadores

Si eres docente/evaluador y quieres ver el proyecto funcionando rápidamente:

### Opción 1: Evaluación Rápida (5 minutos)

```bash
# 1. Clonar repositorio
git clone <URL_DEL_REPO>
cd TP_Prog_Vanguardia/docker

# 2. Iniciar TODO en Docker
./start-full.sh

# 3. Esperar ~30 segundos

# 4. Verificar servicios:
# - Python API: http://localhost:8000/docs
# - Java API: http://localhost:8080/swagger-ui.html
# - Base de datos: http://localhost:5050 (pgAdmin)
```

### Opción 2: Verificación Detallada

```bash
# 1. Verificar que todos los contenedores estén corriendo
docker ps
# Debe mostrar 4 contenedores: postgres, python, java, pgadmin

# 2. Verificar salud de servicios
docker-compose -f docker-compose.full.yml ps
# Todos deben estar "Up" y "healthy"

# 3. Verificar memoria y CPU
docker stats
# Verificar que esté dentro de los límites esperados

# 4. Probar endpoints:
# Python:
curl http://localhost:8000/api/v1/personas
curl http://localhost:8000/api/v1/reservas

# Java:
curl http://localhost:8080/api/salas
curl http://localhost:8080/api/articulos

# 5. Ver logs si algo falla
docker-compose -f docker-compose.full.yml logs
```

### Qué Evaluar

✅ **Arquitectura de Microservicios:**
- Python maneja: Usuarios, Reservas, Auth, Frontend
- Java maneja: Salas, Artículos
- PostgreSQL compartida entre ambos

✅ **Docker Configuration:**
- Límites de memoria configurados
- Health checks implementados
- Networking entre servicios

✅ **Documentación:**
- README claro para principiantes
- Scripts de ayuda (start-db-only.sh, start-full.sh)
- Troubleshooting guide

✅ **Code Quality:**
- Java: Spring Boot 3, Lombok, JPA, Swagger
- Python: FastAPI, SQLAlchemy 2.0, Pydantic v2, JWT

---

## 📚 Recursos Adicionales

- **Documentación del proyecto:** `../README.md`
- **Arquitectura:** `../docs/architecture.md`
- **Postman Collection:** `../postman/`
- **Docker Compose docs:** https://docs.docker.com/compose/

---

## 🆘 Soporte

Si tienes problemas:

1. Lee la sección [Troubleshooting](#troubleshooting)
2. Verifica los logs: `docker-compose logs`
3. Prueba limpieza completa y reinicio
4. Consulta con el equipo de desarrollo

---

**¡Listo! Ahora tienes todo configurado para trabajar con Docker en el proyecto.** 🎉
