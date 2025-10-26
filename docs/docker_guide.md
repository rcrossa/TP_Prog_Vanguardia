# Guía avanzada de Docker

Este documento explica cómo usar Docker y Docker Compose para levantar la infraestructura del sistema.

## Modos de uso

### 1. Solo base de datos
```bash
cd docker
./start-db-only.sh
```
- Levanta solo PostgreSQL.

### 2. Full stack
```bash
cd docker
./start-full.sh
```
- Levanta Python, Java y PostgreSQL.

### 3. Comandos manuales
- `docker-compose -f docker-compose.db-only.yml up -d`
- `docker-compose -f docker-compose.full.yml up -d`
- `./stop-all.sh` para detener todos los servicios.

## Archivos clave
- `docker-compose.db-only.yml`: Solo base de datos
- `docker-compose.full.yml`: Todo el stack
- `start-db-only.sh`, `start-full.sh`, `stop-all.sh`: Scripts de ayuda
- `.env.example`: Variables de entorno
- `init-scripts/`: Scripts SQL de inicialización

## Tips
- Espera ~30 segundos tras iniciar la base de datos.
- Revisa credenciales en `.env` y `docker/.env.example`.
- Usa `docker ps` para verificar contenedores activos.

---

**Última actualización:** 26 de octubre de 2025
