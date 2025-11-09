#!/bin/bash
# Script para ejecutar análisis de SonarQube en el microservicio Java

set -e

echo "🔍 Iniciando análisis de SonarQube para el microservicio Java..."

# Verificar que estamos en el directorio correcto
if [ ! -f "pom.xml" ]; then
    echo "❌ Error: No se encontró pom.xml. Ejecuta este script desde el directorio java-service"
    exit 1
fi

# Verificar que SonarQube está corriendo
if ! curl -s http://localhost:9000 > /dev/null; then
    echo "❌ Error: SonarQube no está ejecutándose en http://localhost:9000"
    exit 1
fi

# Leer token desde .env del proyecto raíz si existe
if [ -f "../.env" ]; then
    export $(grep SONAR_TOKEN ../.env | xargs)
fi

# Verificar que existe el token
if [ -z "$SONAR_TOKEN" ]; then
    echo "⚠️  SONAR_TOKEN no está configurado. Usando análisis sin autenticación..."
    SONAR_ARGS=""
else
    SONAR_ARGS="-Dsonar.token=$SONAR_TOKEN"
fi

echo "📦 Compilando el proyecto..."
mvn clean install -DskipTests

echo "🔍 Ejecutando análisis de SonarQube..."
mvn sonar:sonar \
  -Dsonar.host.url=http://localhost:9000 \
  $SONAR_ARGS

echo "✅ Análisis completado!"
echo "📊 Ver resultados en: http://localhost:9000/dashboard?id=tp_prog_vanguardia_java"
