#!/bin/bash
# Script para ejecutar el servicio Java con la versión correcta de Java

echo "🔧 Configurando Java 21..."
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
echo "✅ Usando Java: $JAVA_HOME"
echo ""

echo "🚀 Iniciando servicio Java en puerto 8080..."
mvn spring-boot:run
