# Tests del Proyecto

Este directorio contiene las pruebas del microservicio Python.

## 📊 Estado Actual

- **Total de tests:** 24
- **Estado:** ✅ Todos pasan
- **Framework:** pytest 7.4.3

## 🏗️ Estructura

```
tests/
├── __init__.py
├── unit/                      # Tests unitarios (24 tests)
│   ├── __init__.py
│   ├── test_models.py         # 6 tests - Modelos Persona y Sala
│   ├── test_auth_service.py   # 5 tests - Servicio de autenticación
│   ├── test_schemas.py        # 6 tests - Esquemas Pydantic
│   └── test_utils.py          # 7 tests - JWT y utilidades
└── integration/               # Tests de integración (futuro)
```

## 🚀 Ejecución Rápida

```bash
# Ejecutar todos los tests
pytest tests/unit/ -v

# Tests específicos
pytest tests/unit/test_models.py -v

# Con cobertura
pytest tests/unit/ --cov=app --cov-report=term
```

## 📚 Documentación Completa

Ver **[docs/testing.md](../docs/testing.md)** para:
- Descripción detallada de cada test
- Configuración de pytest
- Integración con SonarQube
- Cobertura de código
- Troubleshooting

## 🔍 SonarQube

```bash
# Análisis de calidad
sonar-scanner -Dsonar.token=$SONAR_TOKEN

# Dashboard
http://localhost:9000/dashboard?id=tp_prog_vanguardia_python
```

## ✅ Cobertura por Módulo

| Módulo | Tests | Cobertura |
|--------|-------|-----------|
| Modelos | 6 | ~90% |
| Autenticación | 5 | ~85% |
| Esquemas | 6 | ~85% |
| Utilidades | 7 | ~90% |

---

**Última actualización:** Noviembre 2025
