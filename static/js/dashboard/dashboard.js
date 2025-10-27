
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

document.addEventListener('DOMContentLoaded', function() {
    loadActividadChart();

    // 🔒 SEGURIDAD PRE-RENDER: Aplicar clase admin INMEDIATAMENTE antes de que la página renderice
    (function() {
        try {
            const userStr = localStorage.getItem('user');
            if (userStr) {
                const user = JSON.parse(userStr);
                if (user && user.is_admin === true) {
                    document.body.classList.add('is-admin');
                } else {
                    document.body.classList.remove('is-admin');
                }
            } else {
                document.body.classList.remove('is-admin');
            }
        } catch (e) {
            console.error('Error al verificar rol de admin:', e);
            document.body.classList.remove('is-admin');
        }
    })();

    // 🔒 VERIFICACIÓN DE SEGURIDAD
    // Doble verificación para asegurar que usuarios no-admin no vean contenido admin
    const user = window.authManager?.getUser();
    if (!user || user.is_admin !== true) {
        document.body.classList.remove('is-admin');
        document.querySelectorAll('.admin-only').forEach(el => {
            if (window.getComputedStyle(el).display !== 'none') {
                el.style.setProperty('display', 'none', 'important');
            }
        });
    }

    // Actualizar cada 30 segundos
    // setInterval(checkJavaService, 30000);
});