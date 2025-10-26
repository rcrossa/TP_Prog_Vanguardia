# Referencia de API

Este documento lista los endpoints principales de los servicios Python y Java, agrupados por módulo.

## Python Service (Port 8000)

### Autenticación
- POST /api/v1/personas/login
- POST /api/v1/personas/web-login
- GET /api/v1/personas/me

### Personas
- GET /api/v1/personas
- POST /api/v1/personas
- GET /api/v1/personas/{id}
- PUT /api/v1/personas/{id}
- DELETE /api/v1/personas/{id}

### Salas
- GET /api/v1/salas
- POST /api/v1/salas
- GET /api/v1/salas/{id}
- PUT /api/v1/salas/{id}
- DELETE /api/v1/salas/{id}

### Reservas
- GET /api/v1/reservas
- POST /api/v1/reservas
- GET /api/v1/reservas/{id}
- PUT /api/v1/reservas/{id}
- DELETE /api/v1/reservas/{id}

## Java Service (Port 8080)

### Salas
- GET /api/salas
- GET /api/salas/{id}
- GET /api/salas/disponibles
- GET /api/salas/search?nombre=X
- GET /api/salas/capacidad/{min}
- POST /api/salas
- PUT /api/salas/{id}
- DELETE /api/salas/{id}

### Artículos
- GET /api/articulos
- GET /api/articulos/{id}
- GET /api/articulos/disponibles
- GET /api/articulos/categoria/{cat}
- GET /api/articulos/search?nombre=X
- POST /api/articulos
- PUT /api/articulos/{id}
- DELETE /api/articulos/{id}

### Documentación
- GET /swagger-ui.html
- GET /api-docs

---

**Última actualización:** 26 de octubre de 2025
