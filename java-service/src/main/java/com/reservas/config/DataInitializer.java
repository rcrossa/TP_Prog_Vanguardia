package com.reservas.config;

import com.reservas.model.Articulo;
import com.reservas.model.Sala;
import com.reservas.repository.ArticuloRepository;
import com.reservas.repository.SalaRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DataInitializer {
    @Bean
    CommandLineRunner initDatabase(SalaRepository salaRepository, ArticuloRepository articuloRepository) {
        return args -> {
                    // Salas iniciales (según init_db.py)
                    if (salaRepository.count() == 0) {
                        salaRepository.save(Sala.builder()
                                .nombre("Sala de Reuniones 1A")
                                .capacidad(8)
                                .ubicacion("")
                                .disponible(true)
                                .descripcion("")
                                .build());
                        salaRepository.save(Sala.builder()
                                .nombre("Sala de Conferencias B2")
                                .capacidad(20)
                                .ubicacion("")
                                .disponible(true)
                                .descripcion("")
                                .build());
                        salaRepository.save(Sala.builder()
                                .nombre("Aula de Capacitación C3")
                                .capacidad(15)
                                .ubicacion("")
                                .disponible(true)
                                .descripcion("")
                                .build());
                    }
                    // Artículos iniciales (según init_db.py)
                    if (articuloRepository.count() == 0) {
                        articuloRepository.save(Articulo.builder()
                                .nombre("Proyector Epson EB-X05")
                                .descripcion("")
                                .cantidad(1)
                                .categoria("")
                                .disponible(true)
                                .build());
                        articuloRepository.save(Articulo.builder()
                                .nombre("Laptop HP EliteBook")
                                .descripcion("")
                                .cantidad(1)
                                .categoria("")
                                .disponible(false)
                                .build());
                        articuloRepository.save(Articulo.builder()
                                .nombre("Cámara Sony Alpha a6400")
                                .descripcion("")
                                .cantidad(1)
                                .categoria("")
                                .disponible(true)
                                .build());
                    }
        };
    }
}
