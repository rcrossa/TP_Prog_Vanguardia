package com.reservas.model;

import jakarta.persistence.*;
import lombok.*;

/**
 * Entidad Articulo - Representa un recurso o artículo reservable
 */
@Entity
@Table(name = "articulos")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Articulo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String nombre;

    @Column(length = 500)
    private String descripcion;

    @Column(nullable = false)
    private Integer cantidad;

    @Column(length = 50)
    private String categoria;

    @Builder.Default
    @Column(nullable = false)
    private Boolean disponible = true;

}
