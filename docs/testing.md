# 🧪 Documentación de Pruebas

## Índice
- [Descripción General](#descripción-general)
- [Estructura de Tests](#estructura-de-tests)
- [Tests Unitarios](#tests-unitarios)
- [Ejecución de Tests](#ejecución-de-tests)
- [Integración con SonarQube](#integración-con-sonarqube)
- [Cobertura de Código](#cobertura-de-código)

---

## Descripción General

El proyecto implementa **pruebas unitarias** para garantizar la calidad del código y el correcto funcionamiento de los componentes principales del microservicio Python.

### Estadísticas de Tests

- **Total de tests:** 24
- **Estado:** ✅ Todos pasan
- **Framework:** pytest 7.4.3
- **Cobertura:** Modelos, Servicios, Esquemas y Utilidades

---

## Estructura de Tests

```
tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_models.py          # 6 tests - Modelos de datos
│   ├── test_auth_service.py    # 5 tests - Servicio de autenticación
│   ├── test_schemas.py         # 6 tests - Esquemas Pydantic
│   └── test_utils.py           # 7 tests - Utilidades y helpers
└── integration/                # Reservado para tests de integración
```

---

## Tests Unitarios

### 1. Tests de Modelos (`test_models.py`)

**Objetivo:** Verificar que los modelos SQLAlchemy se crean correctamente y tienen el comportamiento esperado.

#### TestPersonaModel (3 tests)

| Test | Descripción | Validación |
|------|-------------|------------|
| `test_persona_creation` | Creación de objeto Persona | Verifica que se asignen correctamente: nombre, apellido, email, is_active, is_admin |
| `test_persona_repr` | Representación en string | Valida el formato del `__repr__()` |
| `test_persona_email_required` | Campo email requerido | Confirma que el atributo email existe |



#### TestSalaModel (3 tests)

| Test | Descripción | Validación |
|------|-------------|------------|
| `test_sala_creation` | Creación de objeto Sala | Verifica: nombre, capacidad, disponible, ubicación, descripción |
| `test_sala_default_values` | Valores por defecto | Valida que los campos opcionales tienen valores por defecto |
| `test_sala_repr` | Representación en string | Valida el formato del `__repr__()` |

---

### 2. Tests de Servicio de Autenticación (`test_auth_service.py`)

**Objetivo:** Validar la lógica de autenticación, hashing de contraseñas y manejo de usuarios.

#### TestAuthService (5 tests)

| Test | Descripción | Validación |
|------|-------------|------------|
| `test_password_hashing` | Hash de contraseñas | Verifica que el hash sea diferente de la contraseña original |
| `test_password_verification_fails_with_wrong_password` | Verificación fallida | Confirma que contraseñas incorrectas no pasan la validación |
| `test_authenticate_user_success` | Autenticación exitosa | Valida login con credenciales correctas (usando mocks) |
| `test_authenticate_user_wrong_password` | Autenticación fallida por contraseña | Verifica que falla con contraseña incorrecta |
| `test_authenticate_user_not_found` | Usuario no encontrado | Valida que retorna None si el usuario no existe |



---

### 3. Tests de Esquemas Pydantic (`test_schemas.py`)

**Objetivo:** Verificar validaciones de datos de entrada/salida usando Pydantic.

#### TestPersonaSchemas (3 tests)

| Test | Descripción | Validación |
|------|-------------|------------|
| `test_persona_create_valid` | Creación válida | Verifica que PersonaCreate acepta datos válidos |
| `test_persona_create_missing_required_fields` | Campos requeridos faltantes | Valida que lanza ValidationError sin campos obligatorios |
| `test_persona_response_valid` | Respuesta válida | Confirma que Persona schema serializa correctamente |

#### TestSalaSchemas (3 tests)

| Test | Descripción | Validación |
|------|-------------|------------|
| `test_sala_create_valid` | Creación válida | Verifica que SalaCreate acepta datos válidos |
| `test_sala_create_invalid_capacidad` | Validación de capacidad | Confirma que rechaza capacidades negativas |
| `test_sala_response_valid` | Respuesta válida | Valida que Sala schema serializa correctamente |


---

### 4. Tests de Utilidades (`test_utils.py`)

**Objetivo:** Verificar funciones helper de JWT y manejo de contraseñas.

#### TestJWTHandler (2 tests)

| Test | Descripción | Validación |
|------|-------------|------------|
| `test_create_access_token` | Creación de token JWT | Verifica que se genera un token válido |
| `test_create_access_token_with_expiration` | Token con expiración | Valida token con tiempo de expiración personalizado |

#### TestPasswordUtilities (5 tests)

| Test | Descripción | Validación |
|------|-------------|------------|
| `test_password_hash_is_different` | Hash diferente de original | Confirma que hash ≠ contraseña |
| `test_same_password_different_hashes` | Diferentes hashes con salt | Verifica que la misma contraseña genera hashes distintos |
| `test_verify_password_correct` | Verificación correcta | Valida que contraseña correcta pasa verificación |
| `test_verify_password_incorrect` | Verificación incorrecta | Confirma que contraseña incorrecta falla |
| `test_verify_password_empty` | Contraseña vacía | Valida manejo de contraseñas vacías |

---

## Ejecución de Tests

### Requisitos Previos

```bash
# Instalar dependencias
pip install pytest pytest-asyncio httpx
```

### Comandos de Ejecución

#### Ejecutar todos los tests
```bash
pytest tests/unit/ -v
```

#### Ejecutar con salida detallada
```bash
pytest tests/unit/ -v --tb=short
```

#### Ejecutar tests específicos
```bash
# Solo tests de modelos
pytest tests/unit/test_models.py -v

# Solo tests de autenticación
pytest tests/unit/test_auth_service.py -v

# Un test específico
pytest tests/unit/test_models.py::TestPersonaModel::test_persona_creation -v
```

#### Ejecutar con marcadores
```bash
# Solo tests unitarios
pytest -m unit -v

# Solo tests de integración (cuando se implementen)
pytest -m integration -v
```


---

## Integración con SonarQube

### Configuración

El proyecto está configurado para análisis con **SonarQube local**.

**Archivo:** `sonar-project.properties`

```properties
sonar.projectKey=tp_prog_vanguardia_python
sonar.sources=app
sonar.tests=tests
sonar.test.inclusions=tests/**/*.py
sonar.exclusions=java-service/**,...
```

### Ejecutar Análisis

```bash
# Con token desde variable de entorno
sonar-scanner -Dsonar.token=$SONAR_TOKEN

# Con token específico
sonar-scanner -Dsonar.token=squ_5d86cca985596b69c90b4a3d7328817025801821
```

### Resultados

SonarQube detectará automáticamente:
- ✅ 24 tests unitarios en `tests/unit/`
- ✅ Cobertura de código (si se genera reporte XML)
- ✅ Calidad del código de los tests
- ✅ Exclusión correcta de `java-service/`

**Acceso al dashboard:**
```
http://localhost:9000/dashboard?id=tp_prog_vanguardia_pythonrd?id=tp_prog_vanguardia_python
```

---

## Cobertura de Código

### Generar Reporte de Cobertura

```bash
# Instalar pytest-cov
pip install pytest-cov

# Ejecutar tests con cobertura
pytest tests/unit/ --cov=app --cov-report=xml --cov-report=term

# Generar reporte HTML
pytest tests/unit/ --cov=app --cov-report=html
```

### Interpretar Resultados

```
Name                              Stmts   Miss  Cover
-----------------------------------------------------
app/models/persona.py                20      2    90%
app/models/sala.py                   15      1    93%
app/services/auth_service.py         45      8    82%
app/auth/jwt_handler.py              25      3    88%
-----------------------------------------------------
TOTAL                               105     14    87%
```

### Cobertura por Módulo

| Módulo | Cobertura Aproximada | Descripción |
|--------|---------------------|-------------|
| `app/models/` | ~90% | Modelos de datos (Persona, Sala) |
| `app/schemas/` | ~85% | Esquemas Pydantic validados |
| `app/auth/jwt_handler.py` | ~90% | Utilidades de autenticación |
| `app/services/auth_service.py` | ~70% | Servicio de autenticación (métodos principales) |


---


## Troubleshooting

### Problema: ModuleNotFoundError

**Solución:**
```bash
# Asegurarse de ejecutar desde la raíz del proyecto
cd /path/to/TP_Prog_Vanguardia
pytest tests/unit/
```

### Problema: Tests fallan por dependencias

**Solución:**
```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

### Problema: Import errors en tests

**Solución:**
```bash
# Añadir el directorio al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/unit/
```


---

## Referencias

- **pytest:** https://docs.pytest.org/
- **pytest-asyncio:** https://pytest-asyncio.readthedocs.io/
- **SonarQube Python:** https://docs.sonarqube.org/latest/analysis/languages/python/
- **Pydantic Testing:** https://docs.pydantic.dev/latest/concepts/testing/

---
