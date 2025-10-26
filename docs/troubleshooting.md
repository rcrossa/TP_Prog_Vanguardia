# Guía de Solución de Problemas

Este documento recopila los problemas más comunes al instalar y ejecutar el sistema, junto con sus soluciones.

## ❌ Puerto 5432 ya en uso
- PostgreSQL local está corriendo.
- Solución: Cambia el puerto en `docker-compose.db-only.yml` y `.env`, o detén el servicio local.

## ❌ Python no reconocido
- Python no está en el PATH.
- Solución: Reinstala Python y marca "Add Python to PATH" o usa `py` en vez de `python`.

## ❌ mvnw no reconocido
- Maven wrapper sin permisos.
- Solución: Usa `.\mvnw.cmd` en Windows o `chmod +x mvnw` en Linux/Mac.

## ❌ Error de conexión a base de datos
- Docker no está corriendo o credenciales incorrectas.
- Solución: Verifica contenedores con `docker ps` y revisa `.env`.

## ❌ Module not found (Python)
- Faltan dependencias.
- Solución: Ejecuta `pip install -r requirements.txt`.

## ❌ Permission denied ./mvnw (Linux/Mac)
- Solución: `chmod +x mvnw`.

## 🛑 Detener el sistema
- Ctrl+C en terminales.
- `docker-compose down` o `./stop-all.sh` en carpeta docker.

---

**Última actualización:** 26 de octubre de 2025
