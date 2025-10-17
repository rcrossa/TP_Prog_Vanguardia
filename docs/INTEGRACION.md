# 🔗 Integración Python ↔ Java - Guía de Pruebas

## 📋 Descripción

Este documento explica cómo probar la **integración HTTP** entre los servicios Python y Java que hemos implementado.

## ✅ Lo que se implementó

### 1. **Python → Java** (Cliente HTTP en Python)

Archivo: `app/services/java_client.py`

**Funcionalidades:**
- ✅ Validar si una sala existe en Java Service
- ✅ Obtener detalles de una sala desde Java
- ✅ Verificar disponibilidad de salas
- ✅ Obtener lista de salas disponibles
- ✅ Validar artículos
- ✅ Health check del servicio Java

**Uso en código:**
```python
from app.services.java_client import JavaServiceClient

# Validar sala
exists = await JavaServiceClient.validate_sala_exists(sala_id=1)

# Obtener detalles
sala = await JavaServiceClient.get_sala_details(sala_id=1)

# Verificar disponibilidad
disponible = await JavaServiceClient.check_sala_disponible(sala_id=1)
```

### 2. **Java → Python** (Cliente HTTP en Java)

Archivo: `java-service/src/main/java/com/reservas/client/PythonServiceClient.java`

**Funcionalidades:**
- ✅ Validar tokens JWT contra Python Service
- ✅ Verificar si un usuario es administrador
- ✅ Obtener información de usuarios
- ✅ Health check del servicio Python

**Uso en código:**
```java
@Autowired
private PythonServiceClient pythonClient;

// Validar token JWT
Optional<PersonaDTO> persona = pythonClient.validateToken(jwtToken);

// Verificar si es admin
boolean esAdmin = pythonClient.isAdmin(jwtToken);
```

### 3. **Endpoints de Demostración**

Archivo: `app/api/v1/endpoints/integration.py`

- `GET /api/v1/integration/health` - Health check de Java Service
- `GET /api/v1/integration/salas-desde-java` - Obtener salas desde Java
- `GET /api/v1/integration/sala/{id}/validar` - Validar sala específica
- `GET /api/v1/integration/articulo/{id}/validar` - Validar artículo
- `GET /api/v1/integration/demo` - Demostración completa

### 4. **Validación JWT en Java Controller**

Archivo: `java-service/src/main/java/com/reservas/controller/SalaController.java`

- ✅ Endpoint `POST /api/salas` ahora valida JWT antes de crear sala
- ✅ Verifica que el usuario sea admin
- ✅ Maneja errores de conexión con Python Service

## 🚀 Cómo Probar la Integración

### Prerequisitos

1. **PostgreSQL** debe estar corriendo (puerto 5432)
2. **Java Service** debe estar corriendo (puerto 8080)
3. **Python Service** debe estar corriendo (puerto 8000)

### Paso 1: Iniciar PostgreSQL

```bash
cd docker
docker-compose -f docker-compose.db-only.yml up -d
```

### Paso 2: Iniciar Java Service

```bash
cd java-service
mvn spring-boot:run
```

Verificar: http://localhost:8080/swagger-ui.html

### Paso 3: Iniciar Python Service

```bash
# En el directorio raíz del proyecto
python main.py
```

Verificar: http://localhost:8000/docs

## 🧪 Pruebas de Integración

### Prueba 1: Health Check de Java desde Python

**Endpoint:** `GET http://localhost:8000/api/v1/integration/health`

```bash
curl http://localhost:8000/api/v1/integration/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "message": "✅ Java Service está disponible y respondiendo",
  "java_service_url": "http://localhost:8080"
}
```

### Prueba 2: Obtener Salas desde Java

**Endpoint:** `GET http://localhost:8000/api/v1/integration/salas-desde-java`

```bash
curl http://localhost:8000/api/v1/integration/salas-desde-java
```

**Respuesta esperada:**
```json
{
  "message": "✅ 5 salas obtenidas desde Java Service",
  "salas": [
    {
      "id": 1,
      "nombre": "Sala de Reuniones A",
      "capacidad": 10,
      "disponible": true
    }
  ],
  "source": "java-service",
  "count": 5
}
```

### Prueba 3: Validar Sala Específica

**Endpoint:** `GET http://localhost:8000/api/v1/integration/sala/1/validar`

```bash
curl http://localhost:8000/api/v1/integration/sala/1/validar
```

**Respuesta esperada:**
```json
{
  "message": "✅ Sala 1 validada exitosamente",
  "exists": true,
  "disponible": true,
  "details": {
    "id": 1,
    "nombre": "Sala de Reuniones A",
    "capacidad": 10,
    "ubicacion": "Piso 2",
    "disponible": true
  },
  "source": "java-service"
}
```

### Prueba 4: Crear Reserva con Validación Java

**Endpoint:** `POST http://localhost:8000/api/v1/reservas`

Esta reserva ahora valida la sala contra Java Service antes de crearla.

```bash
# 1. Primero hacer login para obtener JWT
curl -X POST http://localhost:8000/api/v1/personas/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@reservas.com",
    "password": "admin123"
  }'

# 2. Guardar el token JWT de la respuesta

# 3. Crear reserva
curl -X POST http://localhost:8000/api/v1/reservas \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {TU_TOKEN_JWT}" \
  -d '{
    "id_persona": 1,
    "id_sala": 1,
    "fecha_hora_inicio": "2025-10-20T10:00:00",
    "fecha_hora_fin": "2025-10-20T12:00:00"
  }'
```

**Logs esperados en Python:**
```
✅ Sala 1 validada contra Java Service
✅ Sala 1 está disponible según Java Service
```

### Prueba 5: Crear Sala con Validación JWT (Java → Python)

**Endpoint:** `POST http://localhost:8080/api/salas`

```bash
# 1. Obtener token JWT desde Python
curl -X POST http://localhost:8000/api/v1/personas/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@reservas.com",
    "password": "admin123"
  }'

# 2. Crear sala en Java con el token
curl -X POST http://localhost:8080/api/salas \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {TU_TOKEN_JWT}" \
  -d '{
    "nombre": "Sala Nueva desde Java",
    "capacidad": 15,
    "ubicacion": "Piso 3",
    "descripcion": "Sala creada con validación JWT",
    "disponible": true
  }'
```

**Logs esperados en Java:**
```
✅ Token JWT validado exitosamente para usuario: Admin User
✅ Sala siendo creada por admin: Admin User
```

### Prueba 6: Demo Completa

**Endpoint:** `GET http://localhost:8000/api/v1/integration/demo`

```bash
curl http://localhost:8000/api/v1/integration/demo
```

Muestra un resumen de todas las capacidades de integración.

## 📊 Verificar Logs

### Logs de Python

```bash
# Al crear una reserva, deberías ver:
INFO - ✅ Sala 1 validada exitosamente desde Java Service
INFO - ✅ Sala 1 está disponible según Java Service
```

### Logs de Java

```bash
# Al crear una sala con JWT, deberías ver:
INFO - ✅ Token JWT validado exitosamente para usuario: Admin User
INFO - ✅ Sala siendo creada por admin: Admin User
```

## 🔧 Troubleshooting

### Error: "Java Service NO está disponible"

**Problema:** Python no puede conectarse a Java

**Solución:**
1. Verificar que Java Service esté corriendo: `curl http://localhost:8080/api/salas`
2. Verificar logs de Java Service
3. Verificar firewall/puertos

### Error: "Token JWT inválido"

**Problema:** Java no puede validar el token contra Python

**Solución:**
1. Verificar que Python Service esté corriendo: `curl http://localhost:8000/api/v1/personas`
2. Verificar que el token sea válido: probar en Swagger de Python
3. Verificar formato del header: debe ser `Bearer {token}`

### Error: "Connection Timeout"

**Problema:** Timeout en la comunicación entre servicios

**Solución:**
1. Aumentar el timeout en `JavaServiceClient` (Python) o `PythonServiceClient` (Java)
2. Verificar que ambos servicios estén en la misma red
3. Verificar recursos del sistema (CPU/RAM)

## 📝 Próximos Pasos

Para completar la integración:

1. ✅ **Implementar manejo de circuit breaker**
   - Usar Resilience4j en Java
   - Usar httpx con retry en Python

2. ✅ **Agregar cache de respuestas**
   - Cachear validaciones de JWT
   - Cachear consultas frecuentes

3. ✅ **Implementar service discovery**
   - Usar Consul o Eureka
   - URLs dinámicas en lugar de hardcoded

4. ✅ **Agregar más tests de integración**
   - Tests end-to-end
   - Tests de carga
   - Tests de failover

5. ✅ **Implementar tracing distribuido**
   - OpenTelemetry
   - Jaeger o Zipkin

## 🎓 Documentación Adicional

- **Swagger Python:** http://localhost:8000/docs
- **Swagger Java:** http://localhost:8080/swagger-ui.html
- **GitHub:** [Ver código fuente](https://github.com/rcrossa/TP_Prog_Vanguardia)

---

**Última actualización:** 16 de octubre de 2025  
**Versión:** 1.0.0
