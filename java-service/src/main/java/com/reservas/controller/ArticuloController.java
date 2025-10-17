package com.reservas.controller;

import com.reservas.dto.ArticuloDTO;
import com.reservas.dto.CreateArticuloRequest;
import com.reservas.service.ArticuloService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
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
@Tag(name = "Artículos", description = "API para gestión de artículos e inventario")
@CrossOrigin(origins = {"http://localhost:8000", "http://127.0.0.1:8000"})
public class ArticuloController {

    private final ArticuloService articuloService;

    @Operation(summary = "Obtener todos los artículos")
    @ApiResponse(responseCode = "200", description = "Lista de artículos obtenida exitosamente")
    @GetMapping
    public ResponseEntity<List<ArticuloDTO>> getAllArticulos() {
        return ResponseEntity.ok(articuloService.getAllArticulos());
    }

    @Operation(summary = "Obtener artículo por ID")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Artículo encontrado"),
            @ApiResponse(responseCode = "404", description = "Artículo no encontrado")
    })
    @GetMapping("/{id}")
    public ResponseEntity<ArticuloDTO> getArticuloById(@PathVariable Long id) {
        return ResponseEntity.ok(articuloService.getArticuloById(id));
    }

    @Operation(summary = "Obtener artículos disponibles")
    @ApiResponse(responseCode = "200", description = "Lista de artículos disponibles")
    @GetMapping("/disponibles")
    public ResponseEntity<List<ArticuloDTO>> getArticulosDisponibles() {
        return ResponseEntity.ok(articuloService.getArticulosDisponibles());
    }

    @Operation(summary = "Crear nuevo artículo")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "201", description = "Artículo creado exitosamente"),
            @ApiResponse(responseCode = "400", description = "Datos de entrada inválidos")
    })
    @PostMapping
    public ResponseEntity<ArticuloDTO> createArticulo(@Valid @RequestBody CreateArticuloRequest request) {
        ArticuloDTO createdArticulo = articuloService.createArticulo(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdArticulo);
    }

    @Operation(summary = "Actualizar artículo existente")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Artículo actualizado exitosamente"),
            @ApiResponse(responseCode = "404", description = "Artículo no encontrado"),
            @ApiResponse(responseCode = "400", description = "Datos de entrada inválidos")
    })
    @PutMapping("/{id}")
    public ResponseEntity<ArticuloDTO> updateArticulo(
            @PathVariable Long id,
            @Valid @RequestBody CreateArticuloRequest request) {
        return ResponseEntity.ok(articuloService.updateArticulo(id, request));
    }

    @Operation(summary = "Eliminar artículo")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "204", description = "Artículo eliminado exitosamente"),
            @ApiResponse(responseCode = "404", description = "Artículo no encontrado")
    })
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteArticulo(@PathVariable Long id) {
        articuloService.deleteArticulo(id);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Buscar artículos por categoría")
    @ApiResponse(responseCode = "200", description = "Artículos de la categoría")
    @GetMapping("/categoria/{categoria}")
    public ResponseEntity<List<ArticuloDTO>> findByCategoria(@PathVariable String categoria) {
        return ResponseEntity.ok(articuloService.findByCategoria(categoria));
    }

    @Operation(summary = "Buscar artículos por nombre")
    @ApiResponse(responseCode = "200", description = "Resultados de búsqueda")
    @GetMapping("/search")
    public ResponseEntity<List<ArticuloDTO>> searchByNombre(@RequestParam String nombre) {
        return ResponseEntity.ok(articuloService.searchByNombre(nombre));
    }

}
