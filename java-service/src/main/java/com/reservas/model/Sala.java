package com.reservas.model;

import jakarta.persistence.*;
import lombok.*;

/**
 * Entidad Sala - Representa un espacio reservable
 */
@Entity
@Table(name = "salas")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Sala {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String nombre;

    @Column(nullable = false)
    private Integer capacidad;

    @Column(length = 200)
    private String ubicacion;

    @Column(nullable = false)
    private Boolean disponible = true;

    @Column(length = 500)
    private String descripcion;

}
