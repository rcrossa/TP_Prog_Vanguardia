# Dockerfile para el servicio Python FastAPI
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación (sin __pycache__ gracias a .dockerignore)
COPY app/ ./app/
COPY templates/ ./templates/
COPY static/ ./static/
COPY main.py .
COPY pyproject.toml* .

# Crear directorios necesarios
RUN mkdir -p /app/logs

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
# Nota: --reload se debe activar solo en desarrollo con volúmenes montados
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
