package com.reservas.controller;

import com.reservas.client.PythonServiceClient;
import com.reservas.dto.CreateSalaRequest;
import com.reservas.dto.PersonaDTO;
import com.reservas.dto.SalaDTO;
import com.reservas.service.SalaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.Parameter;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

/**
 * Controlador REST para gestión de Salas
 */
@RestController
@RequestMapping("/api/salas")
@RequiredArgsConstructor
@Tag(name = "Salas", description = "API para gestión de salas reservables")
@CrossOrigin(origins = {"http://localhost:8000", "http://127.0.0.1:8000"})
public class SalaController {

    private static final Logger logger = LoggerFactory.getLogger(SalaController.class);
    
    private final SalaService salaService;
    private final PythonServiceClient pythonClient;

    @Operation(summary = "Obtener todas las salas")
    @ApiResponse(responseCode = "200", description = "Lista de salas obtenida exitosamente")
    @GetMapping
    public ResponseEntity<List<SalaDTO>> getAllSalas() {
        return ResponseEntity.ok(salaService.getAllSalas());
    }

    @Operation(summary = "Obtener sala por ID")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Sala encontrada"),
            @ApiResponse(responseCode = "404", description = "Sala no encontrada")
    })
    @GetMapping("/{id}")
    public ResponseEntity<SalaDTO> getSalaById(@PathVariable Long id) {
        return ResponseEntity.ok(salaService.getSalaById(id));
    }

    @Operation(summary = "Obtener salas disponibles")
    @ApiResponse(responseCode = "200", description = "Lista de salas disponibles")
    @GetMapping("/disponibles")
    public ResponseEntity<List<SalaDTO>> getSalasDisponibles() {
        return ResponseEntity.ok(salaService.getSalasDisponibles());
    }

    @Operation(
        summary = "Crear nueva sala",
        description = "🔗 INTEGRACIÓN: Valida el token JWT contra Python Service antes de crear la sala"
    )
    @ApiResponses(value = {
            @ApiResponse(responseCode = "201", description = "Sala creada exitosamente"),
            @ApiResponse(responseCode = "400", description = "Datos de entrada inválidos"),
            @ApiResponse(responseCode = "401", description = "Token JWT inválido o no proporcionado"),
            @ApiResponse(responseCode = "403", description = "Usuario no tiene permisos de administrador")
    })
    @PostMapping
    public ResponseEntity<?> createSala(
            @Valid @RequestBody CreateSalaRequest request,
            @Parameter(description = "Token JWT en formato 'Bearer {token}'")
            @RequestHeader(value = "Authorization", required = false) String authHeader) {
        
        // 🔗 INTEGRACIÓN CON PYTHON SERVICE: Validar token JWT
        if (authHeader != null && !authHeader.isEmpty()) {
            Optional<PersonaDTO> persona = pythonClient.validateToken(authHeader);
            
            if (persona.isEmpty()) {
                logger.warn("⚠️ Intento de crear sala con token JWT inválido");
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body("Token JWT inválido o expirado");
            }
            
            // Verificar que el usuario es admin
            if (!"admin".equalsIgnoreCase(persona.get().getRol())) {
                PersonaDTO p = persona.get();
                String nombreCompleto = p.getNombre();
                if (p.getApellido() != null && !p.getApellido().isEmpty()) {
                    nombreCompleto += " " + p.getApellido();
                }
                logger.warn("⚠️ Usuario {} intentó crear sala sin permisos de admin", nombreCompleto);
                return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body("Solo los administradores pueden crear salas");
            }
            
            PersonaDTO p = persona.get();
            String nombreCompleto = p.getNombre();
            if (p.getApellido() != null && !p.getApellido().isEmpty()) {
                nombreCompleto += " " + p.getApellido();
            }
            logger.info("✅ Sala siendo creada por admin: {}", nombreCompleto);
        } else {
            logger.warn("⚠️ Intento de crear sala sin token JWT (modo desarrollo)");
            // En desarrollo, permitir creación sin token
            // En producción, descomentar la siguiente línea:
            // return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Token JWT requerido");
        }
        
        SalaDTO createdSala = salaService.createSala(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdSala);
    }

    @Operation(summary = "Actualizar sala existente")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Sala actualizada exitosamente"),
            @ApiResponse(responseCode = "404", description = "Sala no encontrada"),
            @ApiResponse(responseCode = "400", description = "Datos de entrada inválidos")
    })
    @PutMapping("/{id}")
    public ResponseEntity<SalaDTO> updateSala(
            @PathVariable Long id,
            @Valid @RequestBody CreateSalaRequest request) {
        return ResponseEntity.ok(salaService.updateSala(id, request));
    }

    @Operation(summary = "Eliminar sala")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "204", description = "Sala eliminada exitosamente"),
            @ApiResponse(responseCode = "404", description = "Sala no encontrada")
    })
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteSala(@PathVariable Long id) {
        salaService.deleteSala(id);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Buscar salas por nombre")
    @ApiResponse(responseCode = "200", description = "Resultados de búsqueda")
    @GetMapping("/search")
    public ResponseEntity<List<SalaDTO>> searchByNombre(@RequestParam String nombre) {
        return ResponseEntity.ok(salaService.searchByNombre(nombre));
    }

    @Operation(summary = "Buscar salas por capacidad mínima")
    @ApiResponse(responseCode = "200", description = "Salas con capacidad suficiente")
    @GetMapping("/capacidad/{minCapacidad}")
    public ResponseEntity<List<SalaDTO>> findByCapacidad(@PathVariable Integer minCapacidad) {
        return ResponseEntity.ok(salaService.findByCapacidadMinima(minCapacidad));
    }

}
