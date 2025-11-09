# Referencia de API

Este documento lista todos los endpoints de los servicios Python y Java, agrupados por módulo y funcionalidad.

## Python Service (Port 8000)

### 🔐 Autenticación (`/api/v1/auth`)

#### Registro y Login
- **POST** `/api/v1/auth/register` - Registrar nuevo usuario
- **POST** `/api/v1/auth/login` - Iniciar sesión (retorna JWT)
- **GET** `/api/v1/auth/me` - Obtener perfil del usuario autenticado
- **POST** `/api/v1/auth/logout` - Cerrar sesión

#### Gestión de Contraseñas
- **POST** `/api/v1/auth/request-password-reset` - Solicitar reseteo de contraseña
- **POST** `/api/v1/auth/reset-password` - Resetear contraseña con token

#### Roles y Permisos
- **GET** `/api/v1/auth/users` - Listar usuarios (requiere admin)
- **PATCH** `/api/v1/auth/users/{user_id}/role` - Actualizar rol de usuario (requiere admin)

### 👥 Personas (`/api/v1/personas`)

#### CRUD Básico
- **POST** `/api/v1/personas/` - Crear nueva persona
- **GET** `/api/v1/personas/` - Listar todas las personas
- **GET** `/api/v1/personas/{persona_id}` - Obtener persona por ID
- **GET** `/api/v1/personas/email/{email}` - Obtener persona por email
- **PUT** `/api/v1/personas/{persona_id}` - Actualizar persona
- **DELETE** `/api/v1/personas/{persona_id}` - Eliminar persona

#### Autenticación (endpoints legacy)
- **POST** `/api/v1/personas/login` - Login (legacy, usar `/auth/login`)
- **POST** `/api/v1/personas/web-login` - Login desde web
- **GET** `/api/v1/personas/me` - Obtener perfil actual

#### Estadísticas
- **GET** `/api/v1/personas/count/total` - Contar total de personas

### 🏢 Salas (`/api/v1/salas`)

#### CRUD Básico
- **POST** `/api/v1/salas/` - Crear nueva sala
- **GET** `/api/v1/salas/` - Listar todas las salas
- **GET** `/api/v1/salas/{sala_id}` - Obtener sala por ID
- **PUT** `/api/v1/salas/{sala_id}` - Actualizar sala
- **DELETE** `/api/v1/salas/{sala_id}` - Eliminar sala

#### Estadísticas
- **GET** `/api/v1/salas/count/total` - Contar total de salas

### 📦 Artículos (`/api/v1/articulos`)

#### CRUD Básico
- **POST** `/api/v1/articulos/` - Crear nuevo artículo
- **GET** `/api/v1/articulos/` - Listar todos los artículos
- **GET** `/api/v1/articulos/{articulo_id}` - Obtener artículo por ID
- **PUT** `/api/v1/articulos/{articulo_id}` - Actualizar artículo
- **DELETE** `/api/v1/articulos/{articulo_id}` - Eliminar artículo

#### Disponibilidad
- **GET** `/api/v1/articulos/disponibles` - Listar artículos disponibles
- **GET** `/api/v1/articulos/disponibilidad` - Consultar disponibilidad con filtros
- **GET** `/api/v1/articulos/disponibilidad/actual` - Disponibilidad actual de todos
- **PATCH** `/api/v1/articulos/{articulo_id}/toggle-disponibilidad` - Cambiar estado de disponibilidad

#### Estadísticas e Inventario
- **GET** `/api/v1/articulos/estadisticas/inventario` - Estadísticas de inventario
- **GET** `/api/v1/articulos/count/total` - Contar total de artículos
- **GET** `/api/v1/articulos/{articulo_id}/reservas` - Obtener reservas de un artículo

### 📅 Reservas (`/api/v1/reservas`)

#### CRUD Básico
- **POST** `/api/v1/reservas/` - Crear nueva reserva
- **GET** `/api/v1/reservas/` - Listar todas las reservas
- **GET** `/api/v1/reservas/{reserva_id}` - Obtener reserva por ID
- **PUT** `/api/v1/reservas/{reserva_id}` - Actualizar reserva
- **DELETE** `/api/v1/reservas/{reserva_id}` - Eliminar reserva

#### Consultas Filtradas
- **GET** `/api/v1/reservas/persona/{persona_id}` - Reservas de una persona
- **GET** `/api/v1/reservas/sala/{sala_id}` - Reservas de una sala
- **GET** `/api/v1/reservas/articulo/{articulo_id}` - Reservas de un artículo
- **GET** `/api/v1/reservas/fechas/rango` - Reservas en rango de fechas

#### Disponibilidad
- **GET** `/api/v1/reservas/sala/{sala_id}/disponibilidad` - Disponibilidad de sala

#### Gestión de Artículos en Reservas
- **GET** `/api/v1/reservas/{reserva_id}/articulos` - Artículos de una reserva
- **POST** `/api/v1/reservas/{reserva_id}/articulos/{articulo_id}` - Agregar artículo a reserva
- **DELETE** `/api/v1/reservas/{reserva_id}/articulos/{articulo_id}` - Quitar artículo de reserva

#### Estadísticas
- **GET** `/api/v1/reservas/count/total` - Contar total de reservas

### 📊 Estadísticas (`/api/v1/stats`)

#### Actividad
- **GET** `/api/v1/stats/actividad_detallada` - Actividad detallada del sistema
- **GET** `/api/v1/stats/actividad` - Actividad general

#### Reservas
- **GET** `/api/v1/stats/reservas` - Estadísticas de reservas
- **GET** `/api/v1/stats/reservas_activas` - Reservas activas

#### Uso
- **GET** `/api/v1/stats/uso` - Estadísticas de uso del sistema

### 📈 Analytics (`/api/v1/analytics`)

#### Dashboard y Métricas
- **GET** `/api/v1/analytics/dashboard-metrics` - Métricas principales del dashboard
- **GET** `/api/v1/analytics/inventario-metrics` - Métricas de inventario
- **GET** `/api/v1/analytics/ocupacion-prediccion` - Predicción de ocupación

#### Predicciones (Análisis de Patrones)
- **GET** `/api/v1/analytics/predictions/weekly-demand` - Demanda semanal predicha
- **GET** `/api/v1/analytics/predictions/peak-hours` - Horarios pico detectados
- **GET** `/api/v1/analytics/predictions/anomalies` - Detección de anomalías
- **GET** `/api/v1/analytics/predictions/capacity-recommendations` - Recomendaciones de capacidad

#### Exportación
- **GET** `/api/v1/analytics/export-report` - Exportar reportes (PDF/Excel)

### 🔗 Integración Java-Python (`/api/v1/integration`)

#### Health Check
- **GET** `/api/v1/integration/health` - Estado del servicio Java

#### Sincronización
- **GET** `/api/v1/integration/salas-desde-java` - Obtener salas desde servicio Java
- **GET** `/api/v1/integration/sala/{sala_id}/validar` - Validar sala con servicio Java
- **GET** `/api/v1/integration/articulo/{articulo_id}/validar` - Validar artículo con servicio Java

#### Demo
- **GET** `/api/v1/integration/demo` - Endpoint de demostración de integración

### 🌐 Interfaz Web

#### Rutas de Plantillas HTML
- **GET** `/` - Página principal / Dashboard
- **GET** `/login` - Página de login
- **GET** `/salas` - Interfaz de gestión de salas
- **GET** `/reservas` - Interfaz de gestión de reservas
- **GET** `/personas` - Interfaz de gestión de personas
- **GET** `/inventario` - Interfaz de gestión de inventario
- **GET** `/reportes` - Interfaz de reportes y analytics
- **GET** `/configuracion` - Interfaz de configuración
- **GET** `/documentacion` - Documentación integrada

---

## Java Service (Port 8080)

### 🏢 Salas (`/api/salas`)

#### CRUD Básico
- **GET** `/api/salas` - Listar todas las salas
- **GET** `/api/salas/{id}` - Obtener sala por ID
- **POST** `/api/salas` - Crear nueva sala
- **PUT** `/api/salas/{id}` - Actualizar sala
- **DELETE** `/api/salas/{id}` - Eliminar sala

#### Consultas Especializadas
- **GET** `/api/salas/disponibles` - Listar salas disponibles
- **GET** `/api/salas/search?nombre={nombre}` - Buscar salas por nombre
- **GET** `/api/salas/capacidad/{minCapacidad}` - Salas con capacidad mínima

### 📦 Artículos (`/api/articulos`)

#### CRUD Básico
- **GET** `/api/articulos` - Listar todos los artículos
- **GET** `/api/articulos/{id}` - Obtener artículo por ID
- **POST** `/api/articulos` - Crear nuevo artículo
- **PUT** `/api/articulos/{id}` - Actualizar artículo
- **DELETE** `/api/articulos/{id}` - Eliminar artículo

#### Consultas Especializadas
- **GET** `/api/articulos/disponibles` - Listar artículos disponibles
- **GET** `/api/articulos/categoria/{categoria}` - Artículos por categoría
- **GET** `/api/articulos/search?nombre={nombre}` - Buscar artículos por nombre

### 📚 Documentación

#### Swagger UI
- **GET** `/swagger-ui.html` - Interfaz interactiva de Swagger
- **GET** `/swagger-ui/index.html` - Interfaz alternativa de Swagger
- **GET** `/v3/api-docs` - Especificación OpenAPI 3.0 (JSON)
- **GET** `/v3/api-docs.yaml` - Especificación OpenAPI 3.0 (YAML)

---

## Notas Importantes

### Autenticación
- La mayoría de los endpoints requieren autenticación JWT
- Usar header: `Authorization: Bearer <token>`
- Los tokens se obtienen mediante `/api/v1/auth/login` o `/api/v1/personas/login`

### Roles y Permisos
- **admin**: Acceso completo a todos los endpoints
- **user**: Acceso limitado a operaciones de consulta y reservas propias
- **guest**: Solo lectura en endpoints públicos

### Formato de Respuestas
- Todas las respuestas son en formato JSON
- Códigos HTTP estándar: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Internal Server Error)

### Paginación
- Muchos endpoints GET soportan parámetros de paginación:
  - `skip`: Número de elementos a omitir (default: 0)
  - `limit`: Número máximo de elementos (default: 100)

### CORS
- El servicio Python tiene CORS configurado para desarrollo
- En producción, ajustar los orígenes permitidos en `app/core/config.py`

### Documentación Interactiva
- **Python**: http://localhost:8000/docs (Swagger UI automático de FastAPI)
- **Java**: http://localhost:8080/swagger-ui.html (Swagger UI configurado)

---

**Última actualización:** 9 de noviembre de 2025
