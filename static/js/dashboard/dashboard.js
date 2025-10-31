// Dashboard stats loader
async function refreshStats() {
    try {
        // Cargar reservas activas
        const reservasResp = await axios.get('/api/v1/stats/reservas_activas', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const reservasStats = reservasResp.data;
        document.getElementById('reservas-activas').textContent = reservasStats.reservasActivas ?? '...';

        // Cargar unidades disponibles en inventario
        const inventarioResp = await axios.get('/api/v1/articulos/estadisticas/inventario', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const inventarioStats = inventarioResp.data;
        document.getElementById('total-articulos').textContent = inventarioStats.unidades_disponibles ?? '...';
    } catch (error) {
        console.error('Error al cargar estadísticas de reservas:', error);
        document.getElementById('reservas-activas').textContent = '...';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    refreshStats();
});

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
        this.initCharts();
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
        this.updateMetricas(data);
    }

    updateOcupacionChart(ocupacionData) {
        const ctx = document.getElementById('ocupacionChart');
        if (!ctx) return;

        if this.charts.ocupacion) {
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
                labels: tendenciaData.map(item => item.fecha),
                datasets: [{
                    label: 'Reservas por día',
                    data: tendenciaData.map(item => item.cantidad),
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

    async loadPredictions() {
        try {
            const response = await fetch('/api/v1/analytics/ocupacion-prediccion', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                this.updatePrediccionesCard(data.predicciones);
            }
        } catch (error) {
            console.error('Error loading predictions:', error);
        }
    }

    updatePrediccionesCard(predicciones) {
        const container = document.getElementById('prediccionesContainer');
        if (!container) return;

        container.innerHTML = predicciones.map(pred => `
            <div class="prediction-item">
                <div class="prediction-date">${pred.fecha}</div>
                <div class="prediction-value">${pred.prediccion_reservas} reservas</div>
                <div class="prediction-confidence">Confianza: ${(pred.confianza * 100).toFixed(0)}%</div>
            </div>
        `).join('');
    }

    startAutoRefresh() {
        this.refreshInterval = setInterval(() => {
            this.loadDashboardData();
        }, 300000); // 5 minutos
    }

    // ...existing code...
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DashboardManager();
});