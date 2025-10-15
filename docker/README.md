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
- **Configuración:** Ver archivo `.env` o valores por defecto en `docker-compose.yml`

#### PgAdmin (Interfaz web para PostgreSQL)
- **URL:** http://localhost:8080
- **Credenciales:** Ver archivo `.env` o valores por defecto en `docker-compose.yml`

### Configuración de Variables de Entorno

Para personalizar las credenciales, crea un archivo `.env` en este directorio:

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tus credenciales
nano .env
```

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