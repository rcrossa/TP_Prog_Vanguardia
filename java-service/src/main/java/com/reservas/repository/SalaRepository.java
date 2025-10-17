package com.reservas.repository;

import com.reservas.model.Sala;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repositorio para la entidad Sala
 */
@Repository
public interface SalaRepository extends JpaRepository<Sala, Long> {
    
    /**
     * Encuentra salas disponibles
     */
    List<Sala> findByDisponibleTrue();
    
    /**
     * Encuentra salas por nombre (búsqueda parcial)
     */
    List<Sala> findByNombreContainingIgnoreCase(String nombre);
    
    /**
     * Encuentra salas por capacidad mínima
     */
    List<Sala> findByCapacidadGreaterThanEqual(Integer capacidad);
    
}
