package com.reservas.service;

import com.reservas.dto.CreateSalaRequest;
import com.reservas.dto.SalaDTO;
import com.reservas.exception.ResourceNotFoundException;
import com.reservas.model.Sala;
import com.reservas.repository.SalaRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Servicio para gestión de Salas
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class SalaService {

    private final SalaRepository salaRepository;

    /**
     * Obtener todas las salas
     */
    @Transactional(readOnly = true)
    public List<SalaDTO> getAllSalas() {
        log.debug("Obteniendo todas las salas");
        return salaRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    /**
     * Obtener sala por ID
     */
    @Transactional(readOnly = true)
    public SalaDTO getSalaById(Long id) {
        log.debug("Obteniendo sala con id: {}", id);
        Sala sala = salaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Sala no encontrada con id: " + id));
        return convertToDTO(sala);
    }

    /**
     * Obtener salas disponibles
     */
    @Transactional(readOnly = true)
    public List<SalaDTO> getSalasDisponibles() {
        log.debug("Obteniendo salas disponibles");
        return salaRepository.findByDisponibleTrue().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    /**
     * Crear nueva sala
     */
    @Transactional
    public SalaDTO createSala(CreateSalaRequest request) {
        log.info("Creando nueva sala: {}", request.getNombre());
        
        Sala sala = Sala.builder()
                .nombre(request.getNombre())
                .capacidad(request.getCapacidad())
                .ubicacion(request.getUbicacion())
                .descripcion(request.getDescripcion())
                .disponible(request.getDisponible() != null ? request.getDisponible() : true)
                .build();
        
        sala = salaRepository.save(sala);
        log.info("Sala creada exitosamente con id: {}", sala.getId());
        
        return convertToDTO(sala);
    }

    /**
     * Actualizar sala existente
     */
    @Transactional
    public SalaDTO updateSala(Long id, CreateSalaRequest request) {
        log.info("Actualizando sala con id: {}", id);
        
        Sala sala = salaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Sala no encontrada con id: " + id));
        
        sala.setNombre(request.getNombre());
        sala.setCapacidad(request.getCapacidad());
        sala.setUbicacion(request.getUbicacion());
        sala.setDescripcion(request.getDescripcion());
        if (request.getDisponible() != null) {
            sala.setDisponible(request.getDisponible());
        }
        
        sala = salaRepository.save(sala);
        log.info("Sala actualizada exitosamente: {}", id);
        
        return convertToDTO(sala);
    }

    /**
     * Eliminar sala
     */
    @Transactional
    public void deleteSala(Long id) {
        log.info("Eliminando sala con id: {}", id);
        
        if (!salaRepository.existsById(id)) {
            throw new ResourceNotFoundException("Sala no encontrada con id: " + id);
        }
        
        salaRepository.deleteById(id);
        log.info("Sala eliminada exitosamente: {}", id);
    }

    /**
     * Buscar salas por nombre
     */
    @Transactional(readOnly = true)
    public List<SalaDTO> searchByNombre(String nombre) {
        log.debug("Buscando salas con nombre: {}", nombre);
        return salaRepository.findByNombreContainingIgnoreCase(nombre).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    /**
     * Buscar salas por capacidad mínima
     */
    @Transactional(readOnly = true)
    public List<SalaDTO> findByCapacidadMinima(Integer capacidad) {
        log.debug("Buscando salas con capacidad mínima: {}", capacidad);
        return salaRepository.findByCapacidadGreaterThanEqual(capacidad).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    /**
     * Convierte entidad a DTO
     */
    private SalaDTO convertToDTO(Sala sala) {
        return SalaDTO.builder()
                .id(sala.getId())
                .nombre(sala.getNombre())
                .capacidad(sala.getCapacidad())
                .ubicacion(sala.getUbicacion())
                .descripcion(sala.getDescripcion())
                .disponible(sala.getDisponible())
                .build();
    }

}
