// JS para dashboard.html
// Aquí se migran funciones como refreshStats, etc.

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

    // Función para actualizar estadísticas
    async function refreshStats() {
        try {
            const response = await axios.get('/stats');
            const stats = response.data;
            
            document.getElementById('total-personas').textContent = stats.personas?.total || 0;
            document.getElementById('total-salas').textContent = stats.salas?.total || 0;
            document.getElementById('reservas-activas').textContent = stats.reservas?.activas || 0;
            
        } catch (error) {
            console.error('Error al actualizar estadísticas:', error);
        }
    }

    // Función para verificar estado del microservicio Java
    async function checkJavaService() {
        try {
            const response = await axios.get('http://localhost:8000/api/v1/personas/me', { 
                timeout: 3000,
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            document.getElementById('java-service-status').innerHTML = `
                <i class="fas fa-check-circle me-2"></i>
                Java Service: Online
            `;
            document.getElementById('java-service-status').className = 'alert alert-success d-flex align-items-center';
            
            // Cargar artículos disponibles
            loadInventoryStats();
            
        } catch (error) {
            document.getElementById('java-service-status').innerHTML = `
                <i class="fas fa-times-circle me-2"></i>
                Java Service: Offline
            `;
            document.getElementById('java-service-status').className = 'alert alert-danger d-flex align-items-center';
            
            document.getElementById('total-articulos').innerHTML = 'N/A';
        }
    }

    // Función para cargar estadísticas de inventario desde Java
    async function loadInventoryStats() {
        try {
            const response = await axios.get('http://localhost:8000/api/v1/articulos/count/total?disponible=true');
            document.getElementById('total-articulos').textContent = response.data.total || 0;
        } catch (error) {
            document.getElementById('total-articulos').textContent = 'Error';
        }
    }

    // Cargar datos al inicio
    document.addEventListener('DOMContentLoaded', function() {
        refreshStats();
        checkJavaService();
        
        // 🔒 VERIFICACIÓN DE SEGURIDAD
        // Doble verificación para asegurar que usuarios no-admin no vean contenido admin
        const user = window.authManager?.getUser();
        
        // Si el usuario NO es admin, forzar ocultamiento
        if (!user || user.is_admin !== true) {
            document.body.classList.remove('is-admin');
            
            // Seguridad adicional: forzar ocultamiento de cualquier elemento admin-only visible
            document.querySelectorAll('.admin-only').forEach(el => {
                if (window.getComputedStyle(el).display !== 'none') {
                    el.style.setProperty('display', 'none', 'important');
                }
            });
        }
        
        // Actualizar cada 30 segundos
        setInterval(checkJavaService, 30000);
    });