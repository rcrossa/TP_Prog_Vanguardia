package com.reservas.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO para respuesta de Artículo
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ArticuloDTO {

    private Long id;
    private String nombre;
    private String descripcion;
    private Integer cantidad;
    private String categoria;
    private Boolean disponible;

}
