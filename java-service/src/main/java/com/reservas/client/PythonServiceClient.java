package com.reservas.client;

import com.reservas.dto.PersonaDTO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;

import java.util.Optional;

/**
 * Cliente HTTP para comunicación con el servicio Python.
 * 
 * Este cliente maneja todas las llamadas HTTP al microservicio Python
 * que gestiona Autenticación, Usuarios y Reservas.
 */
@Component
public class PythonServiceClient {
    
    private static final Logger logger = LoggerFactory.getLogger(PythonServiceClient.class);
    
    // URL base del servicio Python
    private static final String PYTHON_SERVICE_URL = "http://localhost:8000";
    
    private final RestTemplate restTemplate;
    
    public PythonServiceClient() {
        this.restTemplate = new RestTemplate();
    }
    
    /**
     * Validar un token JWT contra el servicio Python.
     * 
     * @param jwtToken Token JWT a validar (puede incluir "Bearer " o no)
     * @return Optional con datos del usuario si el token es válido, vacío si no
     */
    public Optional<PersonaDTO> validateToken(String jwtToken) {
        try {
            // Asegurar que el token tenga el formato "Bearer "
            String token = jwtToken.startsWith("Bearer ") ? jwtToken : "Bearer " + jwtToken;
            
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", token);
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            
            // Llamar al endpoint /me del servicio Python
            ResponseEntity<PersonaDTO> response = restTemplate.exchange(
                PYTHON_SERVICE_URL + "/api/v1/personas/me",
                HttpMethod.GET,
                entity,
                PersonaDTO.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                PersonaDTO persona = response.getBody();
                String nombreCompleto = "";
                if (persona != null && persona.getNombre() != null) {
                    nombreCompleto = persona.getNombre();
                    if (persona.getApellido() != null && !persona.getApellido().isEmpty()) {
                        nombreCompleto += " " + persona.getApellido();
                    }
                }
                logger.info("✅ Token JWT validado exitosamente para usuario: {}", nombreCompleto);
                return Optional.of(persona);
            } else {
                logger.warn("⚠️ Token JWT inválido: respuesta sin body");
                return Optional.empty();
            }
            
        } catch (HttpClientErrorException.Unauthorized e) {
            logger.warn("⚠️ Token JWT no autorizado: {}", e.getMessage());
            return Optional.empty();
        } catch (HttpClientErrorException e) {
            logger.error("❌ Error HTTP al validar token: {} - {}", e.getStatusCode(), e.getMessage());
            return Optional.empty();
        } catch (ResourceAccessException e) {
            logger.error("🔌 No se pudo conectar con Python Service: {}", e.getMessage());
            return Optional.empty();
        } catch (Exception e) {
            logger.error("❌ Error inesperado al validar token: {}", e.getMessage(), e);
            return Optional.empty();
        }
    }
    
    /**
     * Verificar si un usuario es administrador.
     * 
     * @param jwtToken Token JWT del usuario
     * @return true si el usuario es admin, false en caso contrario
     */
    public boolean isAdmin(String jwtToken) {
        Optional<PersonaDTO> persona = validateToken(jwtToken);
        
        if (persona.isPresent()) {
            boolean esAdmin = "admin".equalsIgnoreCase(persona.get().getRol());
            PersonaDTO p = persona.get();
            String nombreCompleto = p.getNombre();
            if (p.getApellido() != null && !p.getApellido().isEmpty()) {
                nombreCompleto += " " + p.getApellido();
            }
            if (esAdmin) {
                logger.info("✅ Usuario {} es administrador", nombreCompleto);
            } else {
                logger.info("ℹ️ Usuario {} NO es administrador", nombreCompleto);
            }
            return esAdmin;
        }
        
        return false;
    }
    
    /**
     * Verificar si el servicio Python está disponible.
     * 
     * @return true si el servicio responde, false en caso contrario
     */
    public boolean checkHealth() {
        try {
            ResponseEntity<String> response = restTemplate.getForEntity(
                PYTHON_SERVICE_URL + "/api/v1/personas",
                String.class
            );
            
            boolean isHealthy = response.getStatusCode().is2xxSuccessful();
            
            if (isHealthy) {
                logger.info("✅ Python Service está disponible y respondiendo");
            } else {
                logger.warn("⚠️ Python Service respondió con status {}", response.getStatusCode());
            }
            
            return isHealthy;
            
        } catch (Exception e) {
            logger.error("❌ Python Service NO está disponible: {}", e.getMessage());
            return false;
        }
    }
    
    /**
     * Obtener información completa de un usuario por ID.
     * 
     * @param personaId ID de la persona
     * @param jwtToken Token JWT válido
     * @return Optional con datos del usuario si existe
     */
    public Optional<PersonaDTO> getPersonaById(Long personaId, String jwtToken) {
        try {
            String token = jwtToken.startsWith("Bearer ") ? jwtToken : "Bearer " + jwtToken;
            
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", token);
            
            HttpEntity<String> entity = new HttpEntity<>(headers);
            
            ResponseEntity<PersonaDTO> response = restTemplate.exchange(
                PYTHON_SERVICE_URL + "/api/v1/personas/" + personaId,
                HttpMethod.GET,
                entity,
                PersonaDTO.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                logger.info("✅ Datos de persona {} obtenidos desde Python Service", personaId);
                return Optional.of(response.getBody());
            }
            
            return Optional.empty();
            
        } catch (HttpClientErrorException.NotFound e) {
            logger.warn("⚠️ Persona {} no encontrada en Python Service", personaId);
            return Optional.empty();
        } catch (Exception e) {
            logger.error("❌ Error al obtener persona {}: {}", personaId, e.getMessage());
            return Optional.empty();
        }
    }
}
