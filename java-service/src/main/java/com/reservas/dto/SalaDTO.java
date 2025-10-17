package com.reservas.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO para respuesta de Sala
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SalaDTO {

    private Long id;
    private String nombre;
    private Integer capacidad;
    private String ubicacion;
    private String descripcion;
    private Boolean disponible;

}
