// Cargar gráfico de actividad detallada (activas y pasadas)
async function loadActividadChart() {
    try {
        const response = await axios.get('/api/v1/stats/actividad_detallada', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const { dias, activas, pasadas } = response.data;

        const ctx = document.getElementById('actividadChart').getContext('2d');
        if (window.actividadChartInstance) {
            window.actividadChartInstance.destroy();
        }
        window.actividadChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dias,
                datasets: [
                    {
                        label: 'Reservas activas',
                        data: activas,
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Reservas pasadas',
                        data: pasadas,
                        backgroundColor: 'rgba(255, 206, 86, 0.5)',
                        borderColor: 'rgba(255, 206, 86, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                    title: {
                        display: true,
                        text: 'Reservas activas y pasadas por día'
                    }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } catch (error) {
        console.error('Error al cargar gráfico de actividad detallada:', error);
    }
}

class DashboardManager {
    constructor() {
        this.charts = {};
        this.refreshInterval = null;
        this.init();
    }

    async init() {
        await this.loadDashboardData();
        await this.loadPredictions(); // Cargar predicciones
        loadActividadChart(); // Cargar gráfico de actividad
        this.startAutoRefresh();
    }

    async loadDashboardData(days = 30) {
        try {
            const response = await fetch(`/api/v1/analytics/dashboard-metrics?days=${days}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.updateDashboard(data);
            }
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        }
    }

    updateDashboard(data) {
        this.updateOcupacionChart(data.ocupacion_salas);
        this.updateTendenciaChart(data.tendencia_reservas);
        this.updateTopUsuarios(data.top_usuarios);
        this.updateMetricas(data.metricas);
    }

    updateMetricas(metricas) {
        // Actualizar métricas principales
        const reservasHoyEl = document.getElementById('reservasHoy');
        if (reservasHoyEl) reservasHoyEl.textContent = metricas.reservas_hoy;

        const ocupacionEl = document.getElementById('ocupacionPromedio');
        if (ocupacionEl) ocupacionEl.textContent = `${metricas.ocupacion_promedio}%`;

        const salasEl = document.getElementById('salasDisponibles');
        if (salasEl) salasEl.textContent = metricas.salas_disponibles;
    }

    updateOcupacionChart(ocupacionData) {
        const ctx = document.getElementById('ocupacionChart');
        if (!ctx) return;

        if (this.charts.ocupacion) {
            this.charts.ocupacion.destroy();
        }

        this.charts.ocupacion = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ocupacionData.map(item => item.sala),
                datasets: [{
                    data: ocupacionData.map(item => item.reservas),
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56',
                        '#4BC0C0', '#9966FF', '#FF9F40'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const item = ocupacionData[context.dataIndex];
                                return `${item.sala}: ${item.reservas} reservas (${item.horas_promedio.toFixed(1)}h promedio)`;
                            }
                        }
                    }
                }
            }
        });
    }

    updateTendenciaChart(tendenciaData) {
        const ctx = document.getElementById('tendenciaChart');
        if (!ctx) return;

        if (this.charts.tendencia) {
            this.charts.tendencia.destroy();
        }

        this.charts.tendencia = new Chart(ctx, {
            type: 'line',
            data: {
                labels: tendenciaData.labels,
                datasets: [{
                    label: 'Reservas por día',
                    data: tendenciaData.values,
                    borderColor: '#36A2EB',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    updateTopUsuarios(topUsuarios) {
        const container = document.getElementById('topUsuariosContainer');
        if (!container) return;

        if (!topUsuarios || topUsuarios.length === 0) {
            container.innerHTML = '<p class="text-muted">No hay datos disponibles</p>';
            return;
        }

        container.innerHTML = topUsuarios.map((usuario, index) => `
            <div class="top-user-item">
                <span class="user-rank">#${index + 1}</span>
                <span class="user-name">${usuario.nombre}</span>
                <span class="user-count">${usuario.reservas} reservas</span>
            </div>
        `).join('');
    }

    async loadPredictions() {
        try {
            console.log('📊 Cargando predicciones...');
            const response = await fetch('/api/v1/analytics/predictions/weekly-demand?dias=7', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            console.log('📊 Response status:', response.status);
            
            if (response.ok) {
                const data = await response.json();
                console.log('📊 Predicciones recibidas:', data);
                console.log('📊 Total predicciones:', data.predicciones?.length);
                
                // Validar que las predicciones existan y no estén vacías
                if (data.predicciones && data.predicciones.length > 0) {
                    this.updatePrediccionChart(data.predicciones);
                    this.updatePrediccionesAlerts(data.predicciones, data.metadata);
                } else {
                    console.warn('📊 No hay predicciones disponibles');
                    const alertsContainer = document.getElementById('prediccionesAlerts');
                    if (alertsContainer) {
                        alertsContainer.innerHTML = `
                            <div class="alert alert-info mb-0">
                                <i class="fas fa-info-circle me-2"></i>
                                No hay suficientes datos históricos para generar predicciones
                            </div>
                        `;
                    }
                }
            } else {
                console.error('📊 Error en respuesta:', response.status, response.statusText);
                const errorText = await response.text();
                console.error('📊 Error details:', errorText);
                
                const alertsContainer = document.getElementById('prediccionesAlerts');
                if (alertsContainer) {
                    alertsContainer.innerHTML = `
                        <div class="alert alert-warning mb-0">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            Error al cargar predicciones (${response.status})
                        </div>
                    `;
                }
            }
        } catch (error) {
            console.error('📊 Error loading predictions:', error);
            const alertsContainer = document.getElementById('prediccionesAlerts');
            if (alertsContainer) {
                alertsContainer.innerHTML = `
                    <div class="alert alert-warning mb-0">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Error al cargar predicciones: ${error.message}
                    </div>
                `;
            }
        }
    }

    updatePrediccionChart(predicciones) {
        console.log('📊 updatePrediccionChart llamado con:', predicciones);
        const ctx = document.getElementById('prediccionChart');
        if (!ctx) {
            console.error('📊 Canvas prediccionChart no encontrado');
            return;
        }

        // Validar que predicciones exista y no esté vacío
        if (!predicciones || predicciones.length === 0) {
            console.warn('📊 No hay predicciones para mostrar en el gráfico');
            return;
        }

        if (this.charts.prediccion) {
            this.charts.prediccion.destroy();
        }

        const labels = predicciones.map(p => `${p.dia_semana} ${p.fecha.split('-')[2]}/${p.fecha.split('-')[1]}`);
        const values = predicciones.map(p => p.demanda_estimada);  // Cambio: prediccion_reservas -> demanda_estimada
        const confidences = predicciones.map(p => p.nivel_confianza);  // Cambio: confianza -> nivel_confianza

        console.log('📊 Labels:', labels);
        console.log('📊 Values:', values);
        console.log('📊 Confidences:', confidences);

        // Colores modernos según nivel de demanda - Paleta vibrante
        const backgroundColors = predicciones.map(p => {
            switch (p.nivel_demanda) {
                case 'muy_alta': return 'rgba(239, 68, 68, 0.85)';    // Rojo vibrante
                case 'alta': return 'rgba(251, 146, 60, 0.85)';       // Naranja cálido
                case 'media': return 'rgba(59, 130, 246, 0.85)';      // Azul brillante
                case 'baja': return 'rgba(16, 185, 129, 0.85)';       // Verde esmeralda
                default: return 'rgba(139, 92, 246, 0.85)';           // Púrpura moderno (muy_baja)
            }
        });

        const borderColors = predicciones.map(p => {
            switch (p.nivel_demanda) {
                case 'muy_alta': return 'rgb(220, 38, 38)';           // Rojo intenso
                case 'alta': return 'rgb(234, 88, 12)';               // Naranja intenso
                case 'media': return 'rgb(37, 99, 235)';              // Azul intenso
                case 'baja': return 'rgb(5, 150, 105)';               // Verde intenso
                default: return 'rgb(124, 58, 237)';                  // Púrpura intenso
            }
        });

        this.charts.prediccion = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Reservas Predichas',
                    data: values,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            afterLabel: (context) => {
                                const pred = predicciones[context.dataIndex];
                                return [
                                    `Confianza: ${(pred.nivel_confianza * 100).toFixed(0)}%`,  // Cambio: confianza -> nivel_confianza
                                    `Demanda: ${pred.nivel_demanda.replace('_', ' ')}`
                                ];
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Número de Reservas'
                        }
                    }
                }
            }
        });
    }

    updatePrediccionesAlerts(predicciones, metadata) {
        console.log('📊 updatePrediccionesAlerts llamado con:', predicciones, metadata);
        const container = document.getElementById('prediccionesAlerts');
        if (!container) {
            console.error('📊 Container prediccionesAlerts no encontrado');
            return;
        }

        // Validar que predicciones exista y no esté vacío
        if (!predicciones || predicciones.length === 0) {
            console.warn('📊 No hay predicciones para mostrar en alerts');
            container.innerHTML = `
                <div class="alert alert-info mb-0">
                    <i class="fas fa-info-circle me-2"></i>
                    No hay suficientes datos históricos para generar predicciones
                </div>
            `;
            return;
        }

        // Filtrar días con alta/muy alta demanda
        const diasAlerta = predicciones.filter(p =>
            p.nivel_demanda === 'alta' || p.nivel_demanda === 'muy_alta'
        );

        let html = '';

        // Mostrar tendencia
        if (metadata && metadata.tendencia_general) {  // Cambio: tendencia -> tendencia_general
            const trendIcon = metadata.tendencia_general === 'creciente' ? 'fa-arrow-trend-up' : 'fa-arrow-trend-down';
            const trendColor = metadata.tendencia_general === 'creciente' ? 'text-success' : 'text-info';
            html += `
                <div class="alert alert-info mb-3">
                    <i class="fas ${trendIcon} me-2 ${trendColor}"></i>
                    <strong>Tendencia ${metadata.tendencia_general}</strong><br>
                    <small>Basado en ${metadata.total_reservas_historicas} reservas históricas</small>
                </div>
            `;
        }

        // Alertas de días con alta demanda
        if (diasAlerta.length > 0) {
            html += '<div class="mb-3"><h6 class="text-danger mb-2">⚠️ Días de Alta Demanda</h6>';
            diasAlerta.forEach(pred => {
                const badgeClass = pred.nivel_demanda === 'muy_alta' ? 'bg-danger' : 'bg-warning';
                html += `
                    <div class="alert alert-warning py-2 px-3 mb-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <span><strong>${pred.dia_semana}</strong> ${pred.fecha}</span>
                            <span class="badge ${badgeClass}">${pred.demanda_estimada}</span>
                        </div>
                        <small class="text-muted">${pred.recomendacion}</small>
                    </div>
                `;
            });
            html += '</div>';
        }

        // Resumen de la semana
        const totalPredicho = predicciones.reduce((sum, p) => sum + p.demanda_estimada, 0);  // Cambio: prediccion_reservas -> demanda_estimada
        const promedioConfianza = predicciones.reduce((sum, p) => sum + p.nivel_confianza, 0) / predicciones.length;  // Cambio: confianza -> nivel_confianza

        html += `
            <div class="card bg-light">
                <div class="card-body p-3">
                    <h6 class="card-subtitle mb-2 text-muted">Resumen Semanal</h6>
                    <div class="d-flex justify-content-between mb-2">
                        <span>Total predicho:</span>
                        <strong>${totalPredicho} reservas</strong>
                    </div>
                    <div class="d-flex justify-content-between mb-2">
                        <span>Promedio/día:</span>
                        <strong>${(totalPredicho / predicciones.length).toFixed(1)}</strong>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span>Confianza promedio:</span>
                        <strong>${(promedioConfianza * 100).toFixed(0)}%</strong>
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    startAutoRefresh() {
        this.refreshInterval = setInterval(() => {
            this.loadDashboardData();
            this.loadPredictions();
        }, 300000); // 5 minutos
    }

    // ...existing code...
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DashboardManager();
});