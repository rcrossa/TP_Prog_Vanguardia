# 🔒 Scripts de Inicialización de Base de Datos

## ⚠️ ADVERTENCIA DE SEGURIDAD

Este directorio contiene scripts SQL de inicialización que se ejecutan automáticamente cuando se crea el contenedor de PostgreSQL.

### 🛡️ Consideraciones de Seguridad

#### Passwords en el Código

**IMPORTANTE:** Los scripts actuales contienen passwords hasheadas con bcrypt para fines de **desarrollo y demostración**.

```sql
-- Ejemplo de hash bcrypt en el script:
'$2b$12$Io25eHPVYkiIp1MD/EdDHeiuvN8Z2GXF5gSzABi7sE1m7gq6ZcY7i'
-- Este hash corresponde a: "admin123"
```

#### ✅ Buenas Prácticas Implementadas

1. **Passwords Hasheadas:** Las contraseñas nunca se almacenan en texto plano, siempre usando bcrypt
2. **Comentarios Informativos:** Los scripts documentan qué password corresponde a cada hash (solo para desarrollo)
3. **Variables de Entorno:** Las credenciales de PostgreSQL se gestionan vía `.env` (no en código)

#### ⚠️ Para Producción

Si vas a usar este sistema en un entorno real:

1. **Eliminar usuarios de ejemplo:**
   ```sql
   -- NO incluir estos INSERT en producción:
   -- INSERT INTO personas (nombre, email, hashed_password, ...) VALUES (...)
   ```

2. **Crear usuarios mediante la API:**
   - Usar el endpoint `/api/v1/auth/register`
   - Cambiar passwords inmediatamente después del primer login

3. **Rotar secrets regularmente:**
   - Actualizar `SECRET_KEY` en `.env`
   - Cambiar password de PostgreSQL
   - Renovar certificados SSL si aplica

4. **Remover comentarios con passwords:**
   ```sql
   -- ❌ NO INCLUIR EN PRODUCCIÓN:
   -- Contraseña para todos los usuarios: "admin123"
   ```

5. **Usar un script de inicialización limpio:**
   - Solo crear estructura de tablas
   - Insertar datos maestros (no usuarios)
   - Configurar índices y constraints

### 📝 Contenido de los Scripts

#### `01-init.sql`

Este script crea:

- ✅ **Estructura de tablas:** personas, articulos, salas, reservas, reserva_articulos
- ✅ **Relaciones:** Foreign keys y constraints
- ✅ **Datos de ejemplo:** 4 usuarios, 3 artículos, 3 salas, 3 reservas (SOLO PARA DESARROLLO)

### 🔄 Regenerar la Base de Datos

Si necesitas recrear la base de datos desde cero:

```bash
# Detener contenedores
./stop-all.sh

# Eliminar volúmenes (¡ESTO BORRA TODOS LOS DATOS!)
docker-compose -f docker-compose.db-only.yml down -v
# o
docker-compose -f docker-compose.full.yml down -v

# Reiniciar
./start-db-only.sh
# o
./start-full.sh
```

### 🧪 Testing

Para pruebas automatizadas, considera:

1. Usar una base de datos separada para testing
2. Seeders con datos aleatorios (faker)
3. Fixtures de pytest/JUnit que no requieran passwords reales

### 📖 Recursos Adicionales

- [Bcrypt Password Hashing](https://en.wikipedia.org/wiki/Bcrypt)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [PostgreSQL Security Best Practices](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)

---

## 🔐 Generación de Hashes (Para Desarrollo)

Si necesitas generar un nuevo hash de password para testing:

### Python (usando bcrypt):

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("tu_password_aqui")
print(hashed)
```

### Node.js (usando bcrypt):

```javascript
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash('tu_password_aqui', 12);
console.log(hash);
```

### Online (solo para desarrollo):

⚠️ **NUNCA uses generadores online para passwords de producción**

---

**Recuerda:** La seguridad es un proceso continuo, no un estado final. Siempre revisa y actualiza tus prácticas de seguridad.
