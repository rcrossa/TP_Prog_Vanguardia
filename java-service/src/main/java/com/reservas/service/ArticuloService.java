package com.reservas.service;

import com.reservas.dto.ArticuloDTO;
import com.reservas.dto.CreateArticuloRequest;
import com.reservas.exception.ResourceNotFoundException;
import com.reservas.model.Articulo;
import com.reservas.repository.ArticuloRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Servicio para gestión de Artículos
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class ArticuloService {

    private final ArticuloRepository articuloRepository;

    /**
     * Obtener todos los artículos
     */
    @Transactional(readOnly = true)
    public List<ArticuloDTO> getAllArticulos() {
        log.debug("Obteniendo todos los artículos");
        return articuloRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    /**
     * Obtener artículo por ID
     */
    @Transactional(readOnly = true)
    public ArticuloDTO getArticuloById(Long id) {
        log.debug("Obteniendo artículo con id: {}", id);
        Articulo articulo = articuloRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Artículo no encontrado con id: " + id));
        return convertToDTO(articulo);
    }

    /**
     * Obtener artículos disponibles
     */
    @Transactional(readOnly = true)
    public List<ArticuloDTO> getArticulosDisponibles() {
        log.debug("Obteniendo artículos disponibles");
        return articuloRepository.findByDisponibleTrue().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    /**
     * Crear nuevo artículo
     */
    @Transactional
    public ArticuloDTO createArticulo(CreateArticuloRequest request) {
        log.info("Creando nuevo artículo: {}", request.getNombre());
        
        Articulo articulo = Articulo.builder()
                .nombre(request.getNombre())
                .descripcion(request.getDescripcion())
                .cantidad(request.getCantidad())
                .categoria(request.getCategoria())
                .disponible(request.getDisponible() != null ? request.getDisponible() : true)
                .build();
        
        articulo = articuloRepository.save(articulo);
        log.info("Artículo creado exitosamente con id: {}", articulo.getId());
        
        return convertToDTO(articulo);
    }

    /**
     * Actualizar artículo existente
     */
    @Transactional
    public ArticuloDTO updateArticulo(Long id, CreateArticuloRequest request) {
        log.info("Actualizando artículo con id: {}", id);
        
        Articulo articulo = articuloRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Artículo no encontrado con id: " + id));
        
        articulo.setNombre(request.getNombre());
        articulo.setDescripcion(request.getDescripcion());
        articulo.setCantidad(request.getCantidad());
        articulo.setCategoria(request.getCategoria());
        if (request.getDisponible() != null) {
            articulo.setDisponible(request.getDisponible());
        }
        
        articulo = articuloRepository.save(articulo);
        log.info("Artículo actualizado exitosamente: {}", id);
        
        return convertToDTO(articulo);
    }

    /**
     * Eliminar artículo
     */
    @Transactional
    public void deleteArticulo(Long id) {
        log.info("Eliminando artículo con id: {}", id);
        
        if (!articuloRepository.existsById(id)) {
            throw new ResourceNotFoundException("Artículo no encontrado con id: " + id);
        }
        
        articuloRepository.deleteById(id);
        log.info("Artículo eliminado exitosamente: {}", id);
    }

    /**
     * Buscar artículos por categoría
     */
    @Transactional(readOnly = true)
    public List<ArticuloDTO> findByCategoria(String categoria) {
        log.debug("Buscando artículos de categoría: {}", categoria);
        return articuloRepository.findByCategoria(categoria).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    /**
     * Buscar artículos por nombre
     */
    @Transactional(readOnly = true)
    public List<ArticuloDTO> searchByNombre(String nombre) {
        log.debug("Buscando artículos con nombre: {}", nombre);
        return articuloRepository.findByNombreContainingIgnoreCase(nombre).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    /**
     * Convierte entidad a DTO
     */
    private ArticuloDTO convertToDTO(Articulo articulo) {
        return ArticuloDTO.builder()
                .id(articulo.getId())
                .nombre(articulo.getNombre())
                .descripcion(articulo.getDescripcion())
                .cantidad(articulo.getCantidad())
                .categoria(articulo.getCategoria())
                .disponible(articulo.getDisponible())
                .build();
    }

}
