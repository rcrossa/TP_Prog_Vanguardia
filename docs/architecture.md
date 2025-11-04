# 🏗️ Arquitectura del Sistema - Microservicios Integrados

## 📊 Estado Actual del Proyecto

| Componente | Estado | Descripción |
|------------|--------|-------------|
| 🐍 **Python Service** | ✅ Funcional | FastAPI con Auth JWT, Reservas, Frontend Web integrado |
| ☕ **Java Service** | ✅ Funcional | Spring Boot con ABM Salas (8 endpoints) + ABM Artículos/Inventario (8 endpoints) |
| 🔗 **Integración HTTP** | ✅ **ACTIVA** | Comunicación bidireccional Python ↔ Java (salas + artículos) |
| 🗄️ **PostgreSQL** | ✅ Funcional | Base de datos compartida (personas, salas, artículos, reservas) |
| 🎨 **Frontend** | ✅ Funcional | Templates HTML + JS con Gestión de Salas, Inventario, Reservas y Auth |

**Progreso:** 🟢 ~75% Completado

**✨ Destacado:**
- ✅ Sistema de inventario completo con gestión de stock en tiempo real
- ✅ Frontend interactivo para administración de artículos
- ✅ Validación cruzada de disponibilidad de salas y artículos
- ✅ Cálculo dinámico de stock considerando solo reservas futuras

---

## 🌐 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              FRONTEND WEB (Templates HTML + JavaScript)                     │
│                      http://localhost:8000 (Python)                         │
│  📋 Reservas │ 👥 Personas │ 🏢 Salas │ 📦 Inventario │ 📊 Reportes │ 🔐 Login │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                │ HTTP/REST
                                ▼
      ┌────────────────────────────────┐  🔗 HTTP  ┌─────────────────────────────┐
      │   PYTHON SERVICE               │◄─────────►│   JAVA SERVICE              │
      │   FastAPI : 8000               │           │   Spring Boot : 8080        │
      ├────────────────────────────────┤           ├─────────────────────────────┤
      │ 👤 ABM Usuarios                │           │ 🏢 ABM Salas (8 endpoints)  │
      │ 📅 Reservas (integradas)       │──valida──→│   • CRUD Salas              │
      │    • Valida salas con Java     │  salas    │   • Disponibilidad          │
      │    • Valida artículos con Java │           │   • Capacidad               │
      │ � Auth JWT (Login/Tokens)     │           │                             │
      │ 🎨 Frontend Web (Templates)    │           │ �📦 ABM Artículos (8 ep)     │
      │ � JavaServiceClient           │──valida──→│   • CRUD Inventario         │
      │    • Valida salas              │ artículos │   • Stock disponible        │
      │    • Valida artículos          │           │   • Estado (activo/inactivo)│
      │ 📚 Swagger/OpenAPI             │           │                             │
      │                                │           │ 🔐 Valida JWT con Python    │
      │                                │◄─consulta─│ 🔗 PythonServiceClient      │
      │                                │  usuarios │    • Validación de tokens   │
      │                                │           │ 📚 Swagger/OpenAPI          │
      └────────────────┬───────────────┘           └─────────────┬───────────────┘
                       │                                         │
                       │            Base de Datos Compartida     │
                       └─────────────────┬───────────────────────┘
                                         ▼
                              ┌──────────────────────┐
                              │   PostgreSQL         │
                              │   Port 5432          │
                              ├──────────────────────┤
                              │ • personas           │
                              │ • salas              │
                              │ • articulos          │
                              │ • reservas           │
                              │ • reservas_articulos │
                              └──────────────────────┘
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

### ✅ Flujo 3: Gestión de Inventario/Artículos (Java Service)

**¿Cómo funciona el sistema de inventario?**

```
1. 🖥️ Usuario solicita artículos disponibles
   └─→ GET /api/articulos/disponibles

2. ☕ Java Service procesa la consulta
   └─→ ArticuloController.getArticulosDisponibles()
       └─→ ArticuloService.findDisponibles()

3. 🔍 Java consulta PostgreSQL
   └─→ SELECT * FROM articulos 
       WHERE disponible = true 
       AND estado = 'activo'

4. 📊 Java calcula stock real considerando reservas futuras
   └─→ Para cada artículo:
       • Stock total configurado
       • Reservas activas (solo futuras)
       • Stock disponible = total - reservadas_futuras

5. ✅ Respuesta con artículos y disponibilidad real
   └─→ [
       {
         "id": 1,
         "nombre": "Proyector HD",
         "stock_total": 5,
         "stock_disponible": 3,
         "disponible": true
       }
     ]

📊 Logs que verás:
   INFO - Consultando artículos disponibles
   INFO - Encontrados 15 artículos activos
   INFO - Calculando stock disponible considerando reservas futuras
```

**🔑 Lógica de Stock:**
- Solo considera **reservas futuras** (no bloquea por reservas pasadas)
- Artículos con `disponible=false` no aparecen en `/disponibles`
- El stock se calcula en tiempo real desde la base de datos

---

### ✅ Flujo 4: Crear Artículo desde Frontend (Frontend → Python → Java)

**¿Cómo se crea un artículo nuevo?**

```
1. 🖥️ Admin accede a la sección "Inventario" en el frontend
   └─→ http://localhost:8000/inventario
       └─→ Frontend carga artículos desde Java Service

2. 👤 Admin completa formulario de nuevo artículo
   └─→ Nombre: "Pizarra Digital"
       Descripción: "Pantalla interactiva 65 pulgadas"
       Stock: 2
       Disponible: Sí

3. 🔗 Frontend envía petición directa a Java Service
   └─→ POST http://localhost:8080/api/articulos
       Header: Authorization: Bearer eyJhbGc... (JWT de Python)
       Body: {
         "nombre": "Pizarra Digital",
         "descripcion": "Pantalla interactiva 65 pulgadas",
         "stock": 2,
         "disponible": true
       }

4. ☕ Java extrae y valida el JWT
   └─→ PythonServiceClient.validateToken(token)
       └─→ HTTP GET http://localhost:8000/api/v1/personas/me
           └─→ 🐍 Python responde: {"id": 1, "nombre": "Admin", "is_admin": true}

5. 🔐 Java verifica permisos de administrador
   └─→ if (!persona.isAdmin()) → 403 Forbidden
       └─→ Admin confirmado ✅

6. 💾 Java crea el artículo en PostgreSQL
   └─→ INSERT INTO articulos (nombre, descripcion, stock, disponible)
       └─→ ✅ Artículo creado con ID: 16

7. 🎨 Frontend recibe respuesta y actualiza la tabla
   └─→ Nuevo artículo aparece en la lista del inventario

📊 Logs que verás:
   INFO - ✅ Token JWT validado para usuario: Admin
   INFO - ✅ Usuario es administrador, permitiendo creación de artículo
   INFO - ✅ Artículo 'Pizarra Digital' creado exitosamente
```

**❌ Si no es admin:** `403 Forbidden: Solo los administradores pueden crear artículos`

**🔙 Fallback del Frontend:**
Si Java no responde, el frontend muestra error y sugiere verificar que el servicio Java esté corriendo.

---

## 🐍 Python Service (Port 8000)

### Responsabilidades

| Funcionalidad | Estado | Descripción |
|---------------|--------|-------------|
| 👤 ABM Usuarios | ✅ Implementado | CRUD + Auth JWT + Roles |
| 📅 Reservas | ✅ **Integrado con Java** | Valida salas y artículos contra Java Service |
| 🔐 Autenticación | ✅ Implementado | Login, JWT, cookies, roles |
| 🎨 Frontend Web | ✅ Implementado | Templates + JS + Auth (Salas, Inventario, Reservas) |
| 🔗 Cliente Java | ✅ Implementado | HTTP client (`java_client.py`) para salas y artículos |
| 🤖 ML/Analytics | ⏳ Pendiente | Predicción y análisis |
| 📊 Reportes | ⏳ Pendiente | PDF/Excel |

### Archivos Clave de Integración

**Python → Java:**
- `app/services/java_client.py` - Cliente HTTP asíncrono para llamadas a Java Service
  - `validate_sala_exists()` - Valida si una sala existe
  - `check_sala_disponible()` - Verifica disponibilidad de sala
  - `validate_articulo_exists()` - Valida si un artículo existe
  - `check_articulo_disponible()` - Verifica stock disponible de artículo
- `app/services/reserva_service.py` - Validación de salas y artículos contra Java al crear reservas
- `app/api/v1/endpoints/integration.py` - Endpoints de demostración de integración

**Frontend (Templates):**
- `templates/salas.html` - Gestión de salas (consume Java Service)
- `templates/inventario.html` - Gestión de artículos/inventario (consume Java Service)
- `static/js/inventario.js` - JavaScript para comunicación con Java Service

**Funcionalidades:**
- Validación de existencia de salas y artículos consultando Java Service
- Verificación de disponibilidad de recursos (salas y stock de artículos)
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
| 🏢 ABM Salas | ✅ Implementado | 8 endpoints REST completos + validación de disponibilidad |
| 📦 ABM Artículos/Inventario | ✅ Implementado | 8 endpoints REST + gestión de stock en tiempo real |
| 🔐 Validación JWT | ✅ **Integrado con Python** | Valida tokens contra Python en cada operación |
| 🔗 Cliente Python | ✅ Implementado | HTTP client (`PythonServiceClient.java`) |
| 📚 Swagger | ✅ Implementado | Documentación interactiva en `/swagger-ui.html` |
| 🧪 Testing | ⏳ Pendiente | Tests unitarios/integración |

### Archivos Clave de Integración

**Java → Python:**
- `java-service/.../client/PythonServiceClient.java` - Cliente HTTP para validación JWT
- `java-service/.../controller/SalaController.java` - Validación de autenticación en endpoints de salas
- `java-service/.../controller/ArticuloController.java` - Validación de permisos de admin en artículos

**Gestión de Inventario:**
- `java-service/.../service/ArticuloService.java` - Lógica de negocio de artículos
  - Cálculo de stock disponible en tiempo real
  - Considera solo reservas futuras (no pasadas)
  - Filtrado por estado activo/disponible
- `java-service/.../repository/ArticuloRepository.java` - Acceso a datos de artículos

**Funcionalidades:**
- Validación de tokens JWT contra Python Service
- Verificación de roles de usuario (admin/user)
- CRUD completo de salas con control de capacidad y disponibilidad
- CRUD completo de artículos/inventario con gestión de stock
- Cálculo de disponibilidad en tiempo real considerando reservas
- Solo administradores pueden crear/modificar/eliminar salas y artículos
- Health checks entre servicios
- Autenticación centralizada en Python

### Endpoints (16 total)

**🏢 Salas (8 endpoints):**
- `POST /api/salas` - Crear sala (requiere admin + validación JWT)
- `GET /api/salas` - Listar todas las salas
- `GET /api/salas/{id}` - Obtener sala por ID
- `GET /api/salas/disponibles` - Listar salas disponibles
- `GET /api/salas/search?nombre=X` - Buscar salas por nombre
- `GET /api/salas/capacidad/{min}` - Filtrar por capacidad mínima
- `PUT /api/salas/{id}` - Actualizar sala (requiere admin + validación JWT)
- `DELETE /api/salas/{id}` - Eliminar sala (requiere admin + validación JWT)

**📦 Artículos/Inventario (8 endpoints):**
- `POST /api/articulos` - Crear artículo (requiere admin + validación JWT)
- `GET /api/articulos` - Listar todos los artículos del inventario
- `GET /api/articulos/{id}` - Obtener artículo por ID
- `GET /api/articulos/disponibles` - Listar artículos con stock disponible
- `GET /api/articulos/search?nombre=X` - Buscar artículos por nombre
- `GET /api/articulos/categoria/{cat}` - Filtrar por categoría
- `PUT /api/articulos/{id}` - Actualizar artículo (requiere admin + validación JWT)
- `DELETE /api/articulos/{id}` - Eliminar artículo (requiere admin + validación JWT)

**🔐 Nota de Seguridad:**
- Todos los endpoints POST, PUT, DELETE validan el JWT contra Python Service
- Solo usuarios con `is_admin=true` pueden modificar salas o artículos
- El stock de artículos se calcula en tiempo real considerando solo reservas futuras

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

-- Gestionada por JAVA, consultada por Python para validaciones
CREATE TABLE articulos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    stock INTEGER DEFAULT 0,                -- Stock total disponible
    categoria VARCHAR(50),
    disponible BOOLEAN DEFAULT true,        -- Si el artículo está activo
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Gestionada por PYTHON, referencia a salas/articulos
CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES personas(id),
    id_sala INTEGER REFERENCES salas(id),  -- Opcional: reserva de sala
    fecha_hora_inicio TIMESTAMP,
    fecha_hora_fin TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activa',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Relación muchos a muchos: Reservas pueden incluir múltiples artículos
CREATE TABLE reservas_articulos (
    id SERIAL PRIMARY KEY,
    id_reserva INTEGER REFERENCES reservas(id),
    id_articulo INTEGER REFERENCES articulos(id),
    cantidad INTEGER DEFAULT 1,             -- Cantidad de artículos reservados
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Patrones de Acceso

| Tabla | Escritura | Lectura | Integración |
|-------|-----------|---------|-------------|
| `personas` | Python | Ambos | Java valida JWT consultando Python |
| `salas` | Java | Ambos | Python valida existencia/disponibilidad vía HTTP |
| `articulos` | Java | Ambos | Python valida existencia/stock vía HTTP |
| `reservas` | Python | Python | Python valida salas y artículos contra Java antes de crear |
| `reservas_articulos` | Python | Python | Vincula reservas con artículos del inventario |

**🔑 Flujo de Datos:**
1. **Autenticación centralizada**: Python genera y gestiona JWT
2. **Recursos físicos centralizados**: Java gestiona salas y artículos/inventario
3. **Reservas orquestadas**: Python coordina reservas validando contra Java
4. **Validación cruzada**: Cada servicio valida contra el otro según necesidad

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

**1. Gestión de Inventario:**
1. Abrir: http://localhost:8000
2. Login con: `admin@reservas.com` / `admin123`
3. Ir a "Inventario" (📦)
4. Crear nuevo artículo (ej: "Proyector HD", Stock: 5)
5. Ver en la consola del servidor Java:
   ```
   INFO - ✅ Token JWT validado para usuario: Admin
   INFO - ✅ Artículo 'Proyector HD' creado exitosamente
   ```
6. Ver la lista actualizada con el nuevo artículo
7. Observar las estadísticas: "Artículos Disponibles" vs "No Disponibles"

**2. Crear Reserva de Sala:**
1. Ir a "Reservas" (📅)
2. Crear nueva reserva seleccionando una sala
3. Ver en la consola del servidor Python:
   ```
   INFO - ✅ Sala 1 validada contra Java Service
   INFO - ✅ Sala 1 está disponible según Java Service
   INFO - ✅ Reserva creada exitosamente
   ```

**3. Gestión de Salas:**
1. Ir a "Salas" (🏢)
2. Ver listado de salas (cargadas desde Java Service)
3. Crear/editar salas (solo admin)
4. Ver validación de JWT en consola de Java

### Desde Swagger (API)

**Python Swagger:** http://localhost:8000/docs

- **Probar integración completa:**
  - Endpoint: `GET /api/v1/integration/demo`
  - Ver validación de salas y artículos desde Java

- **Crear reserva con validación:**
  - Endpoint: `POST /api/v1/reservas`
  - Body: Incluir `id_sala` y ver validación contra Java

**Java Swagger:** http://localhost:8080/swagger-ui.html

- **Gestión de Inventario:**
  - `GET /api/articulos/disponibles` - Ver artículos con stock
  - `POST /api/articulos` - Crear artículo (requiere JWT de Python)
  - `GET /api/articulos/{id}` - Ver detalle de artículo

- **Gestión de Salas:**
  - `POST /api/salas` - Crear sala (requiere JWT token de admin)
  - `GET /api/salas/disponibles` - Listar salas disponibles

### Desde Terminal (curl)

```bash
# 1. Login en Python (obtener token)
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@reservas.com","password":"admin123"}' \
  | jq -r '.token.access_token')

# 2. Crear artículo en Java con token de Python
curl -X POST http://localhost:8080/api/articulos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Dell",
    "descripcion": "Laptop para presentaciones",
    "stock": 3,
    "categoria": "Tecnología",
    "disponible": true
  }'

# 3. Ver artículos disponibles desde Java
curl http://localhost:8080/api/articulos/disponibles

# 4. Ver artículos desde Python (para comparar integración)
curl http://localhost:8000/api/v1/integration/articulos-desde-java
```

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
