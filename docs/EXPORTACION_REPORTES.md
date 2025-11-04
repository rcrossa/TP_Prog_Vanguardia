# 📊 Exportación de Reportes

Sistema de exportación de reportes del Dashboard en múltiples formatos.

## 🎯 Formatos Disponibles

### 1️⃣ JSON
- **Uso:** Integración con otras aplicaciones, análisis programático
- **Contenido:** Datos completos con metadata, métricas y listado de reservas
- **Tamaño:** ~5-50 KB dependiendo del período
- **Ventajas:** 
  - Estructura completa con todos los datos
  - Fácil de procesar programáticamente
  - Incluye metadata con fecha de generación

### 2️⃣ CSV (Comma-Separated Values)
- **Uso:** Excel, Google Sheets, análisis de datos
- **Contenido:** Listado de reservas en formato tabular
- **Tamaño:** ~2-20 KB dependiendo del período
- **Ventajas:**
  - Compatible con cualquier hoja de cálculo
  - Fácil de importar en bases de datos
  - Peso ligero

### 3️⃣ Excel (.xlsx)
- **Uso:** Análisis detallado, presentaciones, informes
- **Contenido:** Múltiples hojas con métricas, reservas e información
- **Tamaño:** ~10-100 KB dependiendo del período
- **Ventajas:**
  - Formato profesional
  - Múltiples hojas organizadas
  - Compatible con Microsoft Excel y LibreOffice

---

## 🚀 Cómo Usar

### Desde el Dashboard Web

1. **Acceder al Dashboard:**
   ```
   http://localhost:8000/dashboard
   ```

2. **Hacer clic en el botón "Exportar"** (esquina superior derecha)

3. **Seleccionar el formato deseado:**
   - JSON
   - CSV
   - Excel

4. **El archivo se descargará automáticamente** con el nombre:
   - `reporte_YYYYMMDD_HHMMSS.json`
   - `reporte_YYYYMMDD_HHMMSS.csv`
   - `reporte_YYYYMMDD_HHMMSS.xlsx`

### Desde la API REST

**Endpoint:** `GET /api/v1/analytics/export-report`

**Parámetros:**
- `export_format`: Formato de exportación (`json`, `csv`, `excel`)
- `days`: Período de días hacia atrás (1-365, default: 30)

**Autenticación:** JWT Bearer Token (requerido)

**Ejemplos:**

```bash
# Exportar en JSON (últimos 30 días)
curl -X GET "http://localhost:8000/api/v1/analytics/export-report?export_format=json&days=30" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o reporte.json

# Exportar en CSV (últimos 7 días)
curl -X GET "http://localhost:8000/api/v1/analytics/export-report?export_format=csv&days=7" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o reporte.csv

# Exportar en Excel (últimos 90 días)
curl -X GET "http://localhost:8000/api/v1/analytics/export-report?export_format=excel&days=90" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o reporte.xlsx
```

---

## 📋 Estructura de los Reportes

### JSON
```json
{
  "metadata": {
    "fecha_generacion": "2025-11-04T10:30:00-03:00",
    "periodo_dias": 30,
    "fecha_inicio": "2025-10-05T10:30:00-03:00",
    "fecha_fin": "2025-11-04T10:30:00-03:00"
  },
  "metricas_generales": {
    "total_reservas": 45,
    "ocupacion_promedio": 75.5,
    "salas_mas_usadas": [...]
  },
  "reservas": [
    {
      "id": 1,
      "fecha_inicio": "2025-10-20T10:00:00",
      "fecha_fin": "2025-10-20T12:00:00",
      "id_persona": 5,
      "id_sala": 2,
      "estado": "activa"
    }
  ]
}
```

### CSV
```csv
id,fecha_inicio,fecha_fin,id_persona,id_sala,estado
1,2025-10-20T10:00:00,2025-10-20T12:00:00,5,2,activa
2,2025-10-21T14:00:00,2025-10-21T16:00:00,3,1,activa
```

### Excel
**Hoja 1 - Métricas:**
| Campo | Valor |
|-------|-------|
| total_reservas | 45 |
| ocupacion_promedio | 75.5 |

**Hoja 2 - Reservas:**
| id | fecha_inicio | fecha_fin | id_persona | id_sala | estado |
|----|--------------|-----------|------------|---------|--------|
| 1 | 2025-10-20 10:00:00 | 2025-10-20 12:00:00 | 5 | 2 | activa |

**Hoja 3 - Info:**
| Campo | Valor |
|-------|-------|
| fecha_generacion | 2025-11-04T10:30:00-03:00 |
| periodo_dias | 30 |

---

## 🔧 Implementación Técnica

### Backend (FastAPI)

**Archivo:** `app/api/v1/endpoints/analytics.py`

**Dependencias:**
```python
import pandas as pd
from io import BytesIO, StringIO
from fastapi.responses import StreamingResponse
```

**Funcionalidades:**
- Exportación JSON: Retorna diccionario Python como JSON
- Exportación CSV: Usa `pandas.DataFrame.to_csv()`
- Exportación Excel: Usa `pandas.ExcelWriter` con engine `openpyxl`

### Frontend (JavaScript)

**Archivo:** `templates/dashboard.html`

**Función principal:** `exportReports(format)`

**Flujo:**
1. Validar autenticación (JWT token)
2. Realizar petición GET al endpoint
3. Procesar respuesta según formato:
   - JSON: Crear Blob y descargar
   - CSV/Excel: Descargar directamente desde StreamingResponse
4. Mostrar mensaje de éxito/error

---

## 🛡️ Seguridad

- ✅ **Autenticación requerida:** Solo usuarios autenticados pueden exportar
- ✅ **Validación de parámetros:** Formato y días validados con Pydantic
- ✅ **Sin datos sensibles:** No se exportan contraseñas ni tokens
- ✅ **Límite de período:** Máximo 365 días para evitar reportes enormes

---

## 📊 Casos de Uso

### 1. **Reportes Mensuales**
```javascript
// Exportar reporte del mes en Excel
exportReports('excel'); // Con days=30 por defecto
```

### 2. **Análisis de Datos**
```python
# Procesar reporte JSON en Python
import requests
import json

response = requests.get(
    "http://localhost:8000/api/v1/analytics/export-report?export_format=json&days=90",
    headers={"Authorization": f"Bearer {token}"}
)
data = response.json()

# Analizar reservas
reservas = data['reservas']
print(f"Total de reservas: {len(reservas)}")
```

### 3. **Importar en Excel**
1. Exportar en formato CSV o Excel
2. Abrir con Microsoft Excel o LibreOffice Calc
3. Aplicar filtros, tablas dinámicas, gráficos

### 4. **Auditoría**
```bash
# Exportar todos los datos del último año
curl -X GET "http://localhost:8000/api/v1/analytics/export-report?export_format=excel&days=365" \
  -H "Authorization: Bearer $TOKEN" \
  -o auditoria_anual.xlsx
```

---

## 🐛 Troubleshooting

### Error: "Debes iniciar sesión"
**Solución:** Verificar que el token JWT esté en localStorage
```javascript
console.log(localStorage.getItem('token'));
```

### Error: "Error al exportar reporte"
**Posibles causas:**
- Base de datos sin conexión
- No hay datos en el período seleccionado
- Dependencias faltantes (`pandas`, `openpyxl`)

**Solución:**
```bash
pip install -r requirements.txt
```

### Archivo Excel vacío
**Causa:** No hay reservas en el período seleccionado
**Solución:** Aumentar el parámetro `days` o verificar que existan reservas

---

## 📦 Dependencias

```txt
pandas==2.1.3      # Manipulación de datos tabulares
openpyxl==3.1.2    # Lectura/escritura de archivos Excel
xlsxwriter==3.1.9  # Escritura de archivos Excel (alternativa)
```

**Instalación:**
```bash
pip install pandas openpyxl xlsxwriter
```

---

## ✅ Testing

### Test Manual
```bash
# 1. Iniciar servidor
python main.py

# 2. Login y obtener token
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@reservas.com","password":"admin123"}' \
  | jq -r '.token.access_token')

# 3. Exportar reporte
curl -X GET "http://localhost:8000/api/v1/analytics/export-report?export_format=csv&days=7" \
  -H "Authorization: Bearer $TOKEN" \
  -o test_reporte.csv

# 4. Verificar archivo
ls -lh test_reporte.csv
head test_reporte.csv
```

### Test Automatizado
```python
import pytest
from fastapi.testclient import TestClient

def test_export_json(client, auth_token):
    response = client.get(
        "/api/v1/analytics/export-report?export_format=json&days=30",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "metadata" in data
    assert "reservas" in data

def test_export_csv(client, auth_token):
    response = client.get(
        "/api/v1/analytics/export-report?export_format=csv&days=7",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv"
```

---

## 🔮 Futuras Mejoras

- [ ] Exportación PDF con gráficos
- [ ] Filtrado por sala/usuario específico
- [ ] Programación de reportes automáticos (cron)
- [ ] Envío de reportes por email
- [ ] Templates personalizables
- [ ] Compresión ZIP para períodos largos
- [ ] Exportación de predicciones ML

---

**Última actualización:** Noviembre 2025  
**Autor:** Sistema de Reservas - TP Programación de Vanguardia
