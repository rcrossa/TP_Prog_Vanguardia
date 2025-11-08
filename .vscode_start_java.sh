#!/bin/bash
cd "/Users/robertorossa/Desktop/Unicaba/Tercer cuatrimestre/Programacion de vanguardia/Python/TP_Prog_Vanguardia/java-service"

echo "☕ Iniciando servicio Java en http://localhost:8080"
echo "   Documentación: http://localhost:8080/swagger-ui.html"
echo "   Para detener: Ctrl+C"
echo ""

# Usar mvn21 si existe (wrapper para Java 21), sino mvn normal
if [ -x "./mvn21" ]; then
    ./mvn21 spring-boot:run
else
    mvn spring-boot:run
fi
