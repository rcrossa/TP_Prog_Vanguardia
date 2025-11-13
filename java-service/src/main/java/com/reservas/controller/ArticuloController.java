package com.reservas.controller;

import com.reservas.dto.ArticuloDTO;
import com.reservas.dto.CreateArticuloRequest;
import com.reservas.service.ArticuloService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controlador REST para gestión de Artículos
 */
@RestController
@RequestMapping("/api/articulos")
@RequiredArgsConstructor
@Tag(name = "Artículos", description = "Gestión de artículos e inventario")
@CrossOrigin(origins = {"http://localhost:8000", "http://127.0.0.1:8000"})
public class ArticuloController {

    private final ArticuloService articuloService;

    @Operation(summary = "Listar todos los artículos")
    @GetMapping
    public ResponseEntity<List<ArticuloDTO>> getAllArticulos() {
        return ResponseEntity.ok(articuloService.getAllArticulos());
    }

    @Operation(summary = "Obtener artículo por ID")
    @GetMapping("/{id}")
    public ResponseEntity<ArticuloDTO> getArticuloById(@PathVariable Long id) {
        return ResponseEntity.ok(articuloService.getArticuloById(id));
    }

    @Operation(summary = "Listar artículos disponibles")
    @GetMapping("/disponibles")
    public ResponseEntity<List<ArticuloDTO>> getArticulosDisponibles() {
        return ResponseEntity.ok(articuloService.getArticulosDisponibles());
    }

    @Operation(summary = "Crear artículo")
    @PostMapping
    public ResponseEntity<ArticuloDTO> createArticulo(@Valid @RequestBody CreateArticuloRequest request) {
        ArticuloDTO createdArticulo = articuloService.createArticulo(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdArticulo);
    }

    @Operation(summary = "Actualizar artículo")
    @PutMapping("/{id}")
    public ResponseEntity<ArticuloDTO> updateArticulo(
            @PathVariable Long id,
            @Valid @RequestBody CreateArticuloRequest request) {
        return ResponseEntity.ok(articuloService.updateArticulo(id, request));
    }

    @Operation(summary = "Eliminar artículo")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteArticulo(@PathVariable Long id) {
        articuloService.deleteArticulo(id);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Buscar por categoría")
    @GetMapping("/categoria/{categoria}")
    public ResponseEntity<List<ArticuloDTO>> findByCategoria(@PathVariable String categoria) {
        return ResponseEntity.ok(articuloService.findByCategoria(categoria));
    }

    @Operation(summary = "Buscar por nombre")
    @GetMapping("/search")
    public ResponseEntity<List<ArticuloDTO>> searchByNombre(@RequestParam String nombre) {
        return ResponseEntity.ok(articuloService.searchByNombre(nombre));
    }

}
