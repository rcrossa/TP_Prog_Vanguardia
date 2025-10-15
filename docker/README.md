# Setup con Docker

## Configuración de Base de Datos PostgreSQL

### Prerrequisitos
- Docker Desktop instalado y ejecutándose

### Levantar la base de datos

```bash
# Desde la raíz del proyecto, navegar al directorio docker
cd docker

# Levantar los servicios
docker-compose up -d

# Verificar que los contenedores estén corriendo
docker-compose ps
```

### Servicios disponibles

#### PostgreSQL Database
- **URL:** `localhost:5432`
- **Base de datos:** `reservas`
- **Usuario:** `reservas_user`
- **Contraseña:** `reservas_password`

#### PgAdmin (Interfaz web para PostgreSQL)
- **URL:** http://localhost:8080
- **Email:** admin@reservas.com
- **Contraseña:** admin123

### Comandos útiles

```bash
# Ver logs de la base de datos
docker-compose logs postgres

# Parar los servicios
docker-compose down

# Parar y eliminar volúmenes (borra todos los datos)
docker-compose down -v

# Reiniciar servicios
docker-compose restart
```

### Datos iniciales

La base de datos se inicializa automáticamente con:
- 3 personas (Ana, Juan, María)
- 3 artículos (Proyector, Laptop, Cámara)
- 3 salas (Reuniones, Conferencias, Capacitación)
- 3 reservas de ejemplo

Estos datos corresponden exactamente a los especificados en la consigna del proyecto.