package com.reservas.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

/**
 * DTO para representar datos de una Persona del servicio Python.
 * 
 * Este DTO se usa para deserializar respuestas del servicio Python
 * cuando se validan tokens JWT o se obtienen datos de usuarios.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PersonaDTO {
    
    private Long id;
    
    private String nombre;
    
    private String email;
    
    private String rol;
}
