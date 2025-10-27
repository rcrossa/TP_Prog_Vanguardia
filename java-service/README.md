# 🏢 Servicio Java - Sistema de Reservas

Microservicio Java Spring Boot para gestión de **Salas** y **Artículos** del sistema de reservas.

## 📋 Descripción

Este servicio forma parte de una arquitectura de microservicios junto con el servicio Python. Se encarga de la gestión transaccional de recursos físicos (salas) y artículos del inventario.


## 🏗️ Arquitectura

- **Framework:** Spring Boot 3.3.0
- **Java Version:** 21
- **Build Tool:** Maven
- **Database:** PostgreSQL (compartida con servicio Python)
- **Puerto:** 8080
- **Documentación API:** Swagger/OpenAPI

## 🔧 Tecnologías

- **Spring Boot Starter Web** - REST APIs
- **Spring Data JPA** - ORM y persistencia
- **PostgreSQL Driver** - Conexión a base de datos
- **Lombok** - Reducción de boilerplate
- **SpringDoc OpenAPI** - Documentación automática (Swagger)
- **Spring Boot Validation** - Validación de datos

## 📦 Estructura del Proyecto

```
java-service/
├── src/
│   ├── main/
# Java Service - Sistema de Reservas

2. **Ejecutar la aplicación (usando script helper):**

   ```bash
   ./run.sh
   ```

3. **O ejecutar manualmente con Maven:**
   ```bash
   JAVA_HOME=$(/usr/libexec/java_home -v 21) mvn spring-boot:run
   ```

4. **O ejecutar el JAR:**
   ```bash
   java -jar target/reservas-service-1.0.0.jar

## 📚 Documentación API

- **URL:** http://localhost:8080/api-docs

## 🔌 Endpoints Principales

### Salas (`/api/salas`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/salas` | Listar todas las salas |
| GET | `/api/salas/{id}` | Obtener sala por ID |
| GET | `/api/salas/disponibles` | Listar salas disponibles |
| POST | `/api/salas` | Crear nueva sala |
| PUT | `/api/salas/{id}` | Actualizar sala |
| DELETE | `/api/salas/{id}` | Eliminar sala |
| GET | `/api/salas/search?nombre=X` | Buscar por nombre |
| GET | `/api/salas/capacidad/{min}` | Buscar por capacidad mínima |

### Artículos (`/api/articulos`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/articulos` | Listar todos los artículos |
| GET | `/api/articulos/{id}` | Obtener artículo por ID |
| GET | `/api/articulos/disponibles` | Listar artículos disponibles |
| POST | `/api/articulos` | Crear nuevo artículo |
| PUT | `/api/articulos/{id}` | Actualizar artículo |
| DELETE | `/api/articulos/{id}` | Eliminar artículo |
| GET | `/api/articulos/categoria/{cat}` | Filtrar por categoría |
| GET | `/api/articulos/search?nombre=X` | Buscar por nombre |

## 🗄️ Modelo de Datos

### Sala
```json
{
  "id": 1,
  "nombre": "Sala de Reuniones A",
  "capacidad": 10,
  "ubicacion": "Piso 2, Ala Norte",
  "descripcion": "Sala equipada con proyector y pizarra",
  "disponible": true
}
```

### Artículo
```json
  "disponible": true
}
```
spring.datasource.url=jdbc:postgresql://localhost:5432/reservas
spring.datasource.username=postgres
spring.datasource.password=postgres
```

### CORS

Configurado para aceptar requests desde:
- `http://localhost:8000` (Servicio Python)

3. **Ejecuta el servicio Java directamente con:**
         ```bash
         ./mvnw spring-boot:run
         ```
      (No es necesario usar `run.sh`, puedes ejecutar el comando anterior en cualquier terminal dentro de `java-service`)
      > **Nota:** El proyecto requiere Java 21. Verifica tu versión con `java -version`.

# ⚠️ Solución de problemas Java

Si ves errores de compilación relacionados con la versión de Java, asegúrate de tener Java 21 instalado y activo:

```bash
java -version
# Debe mostrar: openjdk version "21..."
```

Si tienes varias versiones instaladas, puedes forzar el uso de Java 21 con:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
./mvnw spring-boot:run
```
Este servicio se comunica con el servicio Python (puerto 8000) que maneja:
- Autenticación de usuarios
- Gestión de reservas
- Analytics y ML
- Frontend web

## 🧪 Testing

Ejecutar tests:
```bash
mvn test
```

## 📝 Notas de Desarrollo

- **Patrón Repository**: Separación de lógica de acceso a datos
- **DTOs**: Validación automática con `@Valid`
- **Logging**: Configurado con SLF4J/Logback
- **Manejo de Errores**: GlobalExceptionHandler centralizado
- **Lombok**: Reducción de código boilerplate

## 🤝 Contribución

Este es un proyecto académico para la materia **Programación de Vanguardia**.

## 📄 Licencia

Ver archivo LICENSE en el directorio raíz del proyecto.
