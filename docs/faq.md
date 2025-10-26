# Preguntas Frecuentes (FAQ)

## ¿Qué versiones de Python y Java necesito?
- Python 3.11+
- Java 17+

## ¿Cómo creo el usuario admin?
- Ejecuta `python scripts/create_admin.py` (desarrollo)
- Para producción, usa `python scripts/create_admin_secure.py`

## ¿Cómo inicio los servicios?
- Python: `python main.py`
- Java: `cd java-service && mvnw.cmd spring-boot:run` (Windows) o `./mvnw spring-boot:run` (Linux/Mac)
- Base de datos: `cd docker && ./start-db-only.sh`

## ¿Dónde están los endpoints de la API?
- Ver `docs/api_reference.md`

## ¿Cómo soluciono errores comunes?
- Ver `docs/troubleshooting.md`

## ¿Cómo importo la colección de Postman?
- Abrir Postman, importar `postman/Sistema_Completo_API_Collection.postman_collection.json`, crear environment con variables.

## ¿Dónde están los estándares de código?
- Ver `docs/formato_codigo.md`

## ¿Cómo reporto un bug?
- Contacta al equipo de desarrollo (ver README principal)

---

**Última actualización:** 26 de octubre de 2025
