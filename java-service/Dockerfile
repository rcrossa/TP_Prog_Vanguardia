# Multi-stage build para el servicio Java Spring Boot

# Stage 1: Build
FROM maven:3.9-eclipse-temurin-21 AS build

WORKDIR /app

# Copiar pom.xml y descargar dependencias
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copiar código fuente y compilar
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copiar JAR desde el stage de build
COPY --from=build /app/target/reservas-service-1.0.0.jar app.jar

# Exponer el puerto
EXPOSE 8080

# Variables de entorno (serán sobreescritas por docker-compose)
ENV SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/reservas
ENV SPRING_DATASOURCE_USERNAME=reservas_user
ENV SPRING_DATASOURCE_PASSWORD=reservas_password

# Comando para ejecutar la aplicación
ENTRYPOINT ["java", "-jar", "app.jar"]
