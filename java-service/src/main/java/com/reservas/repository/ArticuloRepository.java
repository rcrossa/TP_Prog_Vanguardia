package com.reservas.repository;

import com.reservas.model.Articulo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repositorio para la entidad Articulo
 */
@Repository
public interface ArticuloRepository extends JpaRepository<Articulo, Long> {
    
    /**
     * Encuentra artículos disponibles
     */
    List<Articulo> findByDisponibleTrue();
    
    /**
     * Encuentra artículos por categoría
     */
    List<Articulo> findByCategoria(String categoria);
    
    /**
     * Encuentra artículos por nombre (búsqueda parcial)
     */
    List<Articulo> findByNombreContainingIgnoreCase(String nombre);
    
    /**
     * Encuentra artículos con cantidad mayor o igual a un valor
     */
    List<Articulo> findByCantidadGreaterThanEqual(Integer cantidad);
    
}
