# 🏗️ Arquitectura del Sistema - Microservicios Integrados

## 📊 Estado Actual del Proyecto

| Componente | Estado | Descripción |
|------------|--------|-------------|
| 🐍 **Python Service** | ✅ Funcional | FastAPI con Auth JWT, Reservas, Frontend Web |
| ☕ **Java Service** | ✅ Funcional | Spring Boot con ABM Salas y Artículos (16 endpoints) |
| 🔗 **Integración HTTP** | ✅ **ACTIVA** | Comunicación bidireccional Python ↔ Java |
| 🗄️ **PostgreSQL** | ✅ Funcional | Base de datos compartida |
| 🎨 **Frontend** | ✅ Funcional | Templates HTML + JavaScript con Auth |

**Progreso:** 🟢 ~75% Completado

---

## 🌐 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│         FRONTEND WEB (Templates HTML + JavaScript)          │
│              http://localhost:8000 (Python)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST
                           ▼
      ┌────────────────────────────┐  🔗 HTTP  ┌───────────────────────────┐
      │   PYTHON SERVICE           │◄─────────►│   JAVA SERVICE            │
      │   FastAPI : 8000           │           │   Spring Boot : 8080      │
      ├────────────────────────────┤           ├───────────────────────────┤
      │ 👤 ABM Usuarios            │           │ 🏢 ABM Salas (8 endpoints)│
      │ 📅 Reservas (integradas)   │──valida──→│ 📦 ABM Artículos (8 ep)   │
      │ 🔐 Auth JWT                │  salas    │                           │
      │ 🎨 Frontend Web            │           │ 🔐 Valida JWT con Python  │
      │ 🔗 JavaServiceClient       │◄─consulta─│ 🔗 PythonServiceClient    │
      │ 📚 Swagger/OpenAPI         │  usuarios │ 📚 Swagger/OpenAPI        │
      └──────────────┬─────────────┘           └───────────────┬───────────┘
                     │                                         │
                     │        Base de Datos Compartida         │
                     └─────────────────┬───────────────────────┘
                                       ▼
                            ┌──────────────────┐
                            │   PostgreSQL     │
                            │   Port 5432      │
                            ├──────────────────┤
                            │ • personas       │
                            │ • salas          │
                            │ • articulos      │
                            │ • reservas       │
                            └──────────────────┘
```

---

## 🔗 Flujos de Integración Implementados

### ✅ Flujo 1: Crear Reserva de Sala (Python → Java)

**¿Qué pasa cuando creas una reserva desde el frontend?**

```
1. 🖥️ Usuario completa formulario de reserva
   └─→ POST /api/v1/reservas
       {
         "id_persona": 1,
         "id_sala": 1,
         "fecha_hora_inicio": "2025-10-20T10:00:00",
         "fecha_hora_fin": "2025-10-20T12:00:00"
       }

2. 🐍 Python recibe la solicitud
   └─→ app/services/reserva_service.py
       └─→ _validate_sala_reservation()

3. 🔗 Python pregunta a Java: "¿Existe esta sala?"
   └─→ JavaServiceClient.validate_sala_exists(1)
       └─→ HTTP GET http://localhost:8080/api/salas/1
           └─→ ☕ Java responde: {"id": 1, "nombre": "Sala A", "disponible": true}

4. ✅ Python verifica disponibilidad en Java
   └─→ JavaServiceClient.check_sala_disponible(1)
       └─→ Sala está disponible = true

5. 🔍 Python verifica conflictos horarios (DB local)
   └─→ No hay solapamientos ✅

6. 💾 Python crea la reserva en PostgreSQL
   └─→ ✅ Reserva creada exitosamente

📊 Logs que verás:
   INFO - ✅ Sala 1 validada contra Java Service
   INFO - ✅ Sala 1 está disponible según Java Service
```

**🔙 Fallback Automático:**
Si Java no responde → Python usa validación local contra PostgreSQL

---

### ✅ Flujo 2: Crear Sala en Java (Java → Python)

**¿Cómo se valida la autenticación?**

```
1. Cliente envía POST a Java con JWT token
   └─→ POST /api/salas
       Header: Authorization: Bearer eyJhbGc...
       Body: {"nombre": "Nueva Sala", "capacidad": 20, ...}

2. ☕ Java extrae el JWT del header
   └─→ SalaController.createSala()

3. 🔗 Java pregunta a Python: "¿Este token es válido?"
   └─→ PythonServiceClient.validateToken(token)
       └─→ HTTP GET http://localhost:8000/api/v1/personas/me
           └─→ 🐍 Python responde: {"id": 1, "nombre": "Admin", "rol": "admin"}

4. 🔐 Java verifica que el usuario sea admin
   └─→ if (persona.getRol() == "admin") ✅

5. 💾 Java crea la sala en PostgreSQL
   └─→ ✅ Sala creada por usuario autorizado

📊 Logs que verás:
   INFO - ✅ Token JWT validado para usuario: Admin
   INFO - ✅ Sala siendo creada por admin: Admin
```

**❌ Si no es admin:** `403 Forbidden: Solo los administradores pueden crear salas`

---

## 🐍 Python Service (Port 8000)

### Responsabilidades

| Funcionalidad | Estado | Descripción |
|---------------|--------|-------------|
| 👤 ABM Usuarios | ✅ Implementado | CRUD + Auth JWT + Roles |
| 📅 Reservas | ✅ **Integrado con Java** | Valida salas contra Java Service |
| 🔐 Autenticación | ✅ Implementado | Login, JWT, cookies, roles |
| 🎨 Frontend Web | ✅ Implementado | Templates + JS + Auth |
| 🔗 Cliente Java | ✅ Implementado | HTTP client (`java_client.py`) |
| 🤖 ML/Analytics | ⏳ Pendiente | Predicción y análisis |
| 📊 Reportes | ⏳ Pendiente | PDF/Excel |

### Archivos Clave de Integración

**Python → Java:**
- `app/services/java_client.py` - Cliente HTTP asíncrono para llamadas a Java Service
- `app/services/reserva_service.py` - Validación de salas contra Java al crear reservas
- `app/api/v1/endpoints/integration.py` - Endpoints de demostración de integración

**Funcionalidades:**
- Validación de existencia de salas consultando Java Service
- Verificación de disponibilidad de recursos
- Health checks entre servicios
- Fallback automático a base de datos si Java no responde

### Endpoints de Integración

- `/api/v1/integration/health` - Health check de Java
- `/api/v1/integration/salas-desde-java` - Listar salas desde Java
- `/api/v1/integration/sala/{id}/validar` - Validar sala
- `/api/v1/integration/demo` - Demo completa

---

## ☕ Java Service (Port 8080)

### Responsabilidades

| Funcionalidad | Estado | Descripción |
|---------------|--------|-------------|
| 🏢 ABM Salas | ✅ Implementado | 8 endpoints REST completos |
| 📦 ABM Artículos | ✅ Implementado | 8 endpoints REST completos |
| 🔐 Validación JWT | ✅ **Integrado con Python** | Valida tokens contra Python |
| 🔗 Cliente Python | ✅ Implementado | HTTP client (`PythonServiceClient.java`) |
| 📚 Swagger | ✅ Implementado | Documentación interactiva |
| 🧪 Testing | ⏳ Pendiente | Tests unitarios/integración |

### Archivos Clave de Integración

**Java → Python:**
- `java-service/.../client/PythonServiceClient.java` - Cliente HTTP para validación JWT
- `java-service/.../controller/SalaController.java` - Validación de autenticación en endpoints
- `java-service/.../controller/ArticuloController.java` - Validación de permisos de admin

**Funcionalidades:**
- Validación de tokens JWT contra Python Service
- Verificación de roles de usuario (admin/user)
- Health checks entre servicios
- Autenticación centralizada en Python

### Endpoints (16 total)

**Salas (8):**
- `POST /api/salas` - Crear (con validación JWT)
- `GET /api/salas` - Listar todas
- `GET /api/salas/{id}` - Obtener por ID
- `GET /api/salas/disponibles` - Listar disponibles
- `GET /api/salas/search?nombre=X` - Buscar
- `GET /api/salas/capacidad/{min}` - Por capacidad
- `PUT /api/salas/{id}` - Actualizar
- `DELETE /api/salas/{id}` - Eliminar

**Artículos (8):** Similar estructura

---

## 🗄️ Base de Datos PostgreSQL

### Schema Compartido

```sql
-- Gestionada por PYTHON
CREATE TABLE personas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    rol VARCHAR(20) DEFAULT 'usuario'
);

-- Gestionada por JAVA, consultada por Python
CREATE TABLE salas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    capacidad INTEGER,
    ubicacion VARCHAR(200),
    descripcion TEXT,
    disponible BOOLEAN DEFAULT true
);

-- Gestionada por JAVA, consultada por Python
CREATE TABLE articulos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    cantidad INTEGER DEFAULT 0,
    categoria VARCHAR(50),
    disponible BOOLEAN DEFAULT true
);

-- Gestionada por PYTHON, referencia a salas/articulos
CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES personas(id),
    fecha_hora_inicio TIMESTAMP,
    fecha_hora_fin TIMESTAMP,
    id_sala INTEGER REFERENCES salas(id),
    id_articulo INTEGER REFERENCES articulos(id)
);
```

### Patrones de Acceso

| Tabla | Escritura | Lectura | Integración |
|-------|-----------|---------|-------------|
| `personas` | Python | Ambos | Java valida JWT |
| `salas` | Java | Ambos | Python valida vía HTTP |
| `articulos` | Java | Ambos | Python valida vía HTTP |
| `reservas` | Python | Python | Valida con Java |

---

## 🎯 Tecnologías

### Python Stack
- FastAPI, SQLAlchemy 2.0, Pydantic v2
- JWT (python-jose), httpx (HTTP client)
- Jinja2, PostgreSQL

### Java Stack
- Spring Boot 3.3.0, Java 17
- Spring Data JPA, Hibernate
- SpringDoc OpenAPI, Lombok
- PostgreSQL Driver, RestTemplate (HTTP client)
- Maven 3.6+

---

## 🚀 Cómo Ejecutar

### 1. Iniciar PostgreSQL
```bash
cd docker
docker-compose -f docker-compose.db-only.yml up -d
```

### 2. Iniciar Java Service
```bash
cd java-service
mvn spring-boot:run
# http://localhost:8080/swagger-ui.html
```

### 3. Iniciar Python Service
```bash
python main.py
# http://localhost:8000/docs
```

### 4. Probar Integración
```bash
./scripts/test_integration.sh
```

---

## 🧪 Probar la Integración

### Desde el Frontend (Navegador)

1. Abrir: http://localhost:8000
2. Login con: `admin@reservas.com` / `admin123`
3. Ir a "Reservas"
4. Crear nueva reserva de sala
5. Ver en la consola del servidor Python:
   ```
   ✅ Sala 1 validada contra Java Service
   ✅ Sala 1 está disponible según Java Service
   ```

### Desde Swagger (API)

**Python Swagger:** http://localhost:8000/docs
- Probar endpoint: `/api/v1/integration/demo`

**Java Swagger:** http://localhost:8080/swagger-ui.html
- Probar endpoint: `POST /api/salas` (con JWT token)

---

## 📊 Métricas

| Métrica | Python | Java |
|---------|--------|------|
| Endpoints | 30+ | 16 |
| Integración | ✅ Activa | ✅ Activa |
| Swagger | ✅ | ✅ |
| Tests | ⏳ | ⏳ |

---

## 🔒 Seguridad

1. **JWT Tokens**
   - Generados por Python
   - Validados por ambos servicios
   - Roles: admin, usuario

2. **CORS**
   - Python acepta: localhost:8080
   - Java acepta: localhost:8000

3. **Validación Cross-Service**
   - Java valida JWT con Python
   - Python valida recursos con Java

---

## 📈 Próximos Pasos

### Alta Prioridad
- [ ] Tests de integración Python ↔ Java
- [ ] Docker Compose Full Stack
- [ ] Circuit breaker y retry

### Media Prioridad
- [ ] ML/Analytics en Python
- [ ] Reportes PDF/Excel
- [ ] Observabilidad (tracing)

### Baja Prioridad
- [ ] Service Discovery
- [ ] Load balancing
- [ ] CI/CD Pipeline

---

## 📚 Documentación Adicional

- **Guía de Integración:** `docs/INTEGRACION.md`
- **Implementación:** `docs/IMPLEMENTACION_INTEGRACION.md`
- **Python Swagger:** http://localhost:8000/docs
- **Java Swagger:** http://localhost:8080/swagger-ui.html

---

**Última actualización:** 16 de octubre de 2025
**Versión:** 2.0 - Con integración HTTP activa
**Estado:** ✅ Microservicios funcionales e integrados
