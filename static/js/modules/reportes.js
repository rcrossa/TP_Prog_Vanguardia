/**
 * Reportes Module - Gestión de reportes y analytics del sistema
 * 
 * Este módulo maneja toda la funcionalidad de la página de reportes:
 * - Verificación de autenticación y permisos de admin
 * - Carga de datos de reportes desde el backend
 * - Renderizado de gráficos y métricas
 * - Exportación de reportes
 */

class ReportesManager {
    constructor() {
        this.isInitialized = false;
        this.reports = [];
        this.charts = {};
        
        // Configuración por defecto
        this.config = {
            autoRefresh: false,
            refreshInterval: 30000, // 30 segundos
            exportFormats: ['PDF', 'Excel', 'CSV']
        };
        
        this.init();
    }

    /**
     * Inicialización del módulo
     */
    init() {
        console.log('📊 Inicializando módulo de reportes...');
        
        // Aplicar seguridad pre-render inmediatamente
        this.applyPreRenderSecurity();
        
        // Esperar a que el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeReports());
        } else {
            this.initializeReports();
        }
    }

    /**
     * 🔒 SEGURIDAD PRE-RENDER: Aplicar clase admin INMEDIATAMENTE
     * Esta función debe ejecutarse antes de que el DOM se renderice completamente
     */
    applyPreRenderSecurity() {
        try {
            const userStr = localStorage.getItem('user');
            if (userStr) {
                const user = JSON.parse(userStr);
                if (user && user.is_admin === true) {
                    document.body.classList.add('is-admin');
                    console.log('🔐 Clase admin aplicada');
                } else {
                    document.body.classList.remove('is-admin');
                }
            } else {
                document.body.classList.remove('is-admin');
            }
        } catch (e) {
            console.error('❌ Error al verificar rol de admin:', e);
            document.body.classList.remove('is-admin');
        }
    }

    /**
     * Inicialización de reportes después de que el DOM esté listo
     */
    initializeReports() {
        console.log('📊 Inicializando reportes...');
        this.checkAuthAndPermissions();
    }

    /**
     * Verificación de autenticación y permisos
     */
    checkAuthAndPermissions() {
        // Esperar a que el AuthManager esté completamente inicializado
        const checkAuth = () => {
            if (!window.authManager) {
                console.log('⏳ Esperando AuthManager...');
                setTimeout(checkAuth, 100);
                return;
            }
            
            // Verificar que el usuario esté autenticado
            if (!window.authManager.isAuthenticated()) {
                console.log('❌ Usuario no autenticado, redirigiendo...');
                window.location.href = '/login';
                return;
            }
            
            // Verificar permisos de admin
            const user = window.authManager.getUser();
            if (!user || !user.is_admin) {
                console.log('❌ Acceso denegado - no es admin');
                this.showError('Acceso denegado. Solo los administradores pueden acceder a esta sección.');
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
                return;
            }
            
            console.log('✅ Autenticación y permisos verificados');
            // Si todo está bien, cargar reportes
            this.loadReports();
        };
        
        // Iniciar verificación
        checkAuth();
    }

    /**
     * Cargar reportes desde el backend
     */
    async loadReports() {
        try {
            console.log('📥 Cargando reportes...');
            
            // Obtener configuración desde template bridge
            const templateConfig = window.templateBridge?.get('reportsConfig', {});
            this.config = { ...this.config, ...templateConfig };
            
            // Cargar datos de reportes
            await this.loadReportData();
            
            // Renderizar reportes
            this.renderReports();
            
            // Configurar auto-refresh si está habilitado
            if (this.config.autoRefresh) {
                this.setupAutoRefresh();
            }
            
            this.isInitialized = true;
            console.log('✅ Reportes cargados correctamente');
            
        } catch (error) {
            console.error('❌ Error cargando reportes:', error);
            this.showError('Error al cargar los reportes. Por favor, intente nuevamente.');
        }
    }

    /**
     * Cargar datos de reportes desde APIs
     */
    async loadReportData() {
        try {
            // Placeholder para futuras APIs de reportes
            // Aquí se conectaría con el microservicio Java
            
            // Primero cargar los datos desde las APIs
            const reservationStats = await this.fetchReservationStats();
            const usageStats = await this.fetchUsageStats();
            
            // Ejemplo de estructura de datos
            this.reports = [
                {
                    id: 'reservas-overview',
                    title: 'Resumen de Reservas',
                    type: 'chart',
                    data: reservationStats
                },
                {
                    id: 'usage-stats',
                    title: 'Estadísticas de Uso',
                    type: 'metrics',
                    data: usageStats
                }
            ];
            
        } catch (error) {
            console.error('❌ Error obteniendo datos de reportes:', error);
            throw error;
        }
    }

    /**
     * Obtener estadísticas de reservas REALES desde la base de datos
     */
    async fetchReservationStats() {
        try {
            console.log('📊 Obteniendo estadísticas de reservas REALES...');
            
            // Obtener reservas reales
            const reservas = await this.apiRequest('/api/v1/reservas/').catch(() => []);
            const reservasArray = Array.isArray(reservas) ? reservas : [];
            

            // Calcular reservas de hoy, activas y futuras
            const now = new Date();
            const hoy = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
            let reservasHoy = 0, reservasActivas = 0, reservasFuturas = 0;
            reservasArray.forEach(reserva => {
                if (!reserva.fecha_hora_inicio) return;
                const inicio = new Date(reserva.fecha_hora_inicio);
                const fechaReserva = `${inicio.getFullYear()}-${String(inicio.getMonth()+1).padStart(2,'0')}-${String(inicio.getDate()).padStart(2,'0')}`;
                if (fechaReserva === hoy) reservasHoy++;
                if (inicio <= now && (!reserva.fecha_hora_fin || new Date(reserva.fecha_hora_fin) >= now)) reservasActivas++;
                if (inicio > now) reservasFuturas++;
            });
            
            // Obtener salas más populares (análisis simplificado)
            const salaCount = {};
            const articuloCount = {};
            
            reservasArray.forEach(reserva => {
                // Contar reservas por tipo
                if (reserva.sala_id) {
                    const salaKey = `Sala ${reserva.sala_id}`;
                    salaCount[salaKey] = (salaCount[salaKey] || 0) + 1;
                }
                if (reserva.articulo_id) {
                    const articuloKey = `Artículo ${reserva.articulo_id}`;
                    articuloCount[articuloKey] = (articuloCount[articuloKey] || 0) + 1;
                }
            });
            
            const salasPopulares = Object.entries(salaCount)
                .sort(([,a], [,b]) => b - a)
                .slice(0, 3)
                .map(([nombre]) => nombre);
            
            // Calcular también estadísticas de artículos
            const articulosPopulares = Object.entries(articuloCount)
                .sort(([,a], [,b]) => b - a)
                .slice(0, 2)
                .map(([nombre]) => nombre);

            console.log('📊 Estadísticas de reservas reales:', {
                total: reservasArray.length,
                hoy: reservasHoy,
                salasPopulares,
                articulosPopulares,
                reservasSalas: Object.keys(salaCount).length,
                reservasArticulos: Object.keys(articuloCount).length
            });
            
            return {
                totalReservas: reservasArray.length,
                reservasHoy,
                reservasActivas,
                reservasFuturas,
                salasPopulares: salasPopulares.length > 0 ? salasPopulares : ['Sin reservas de salas'],
                articulosPopulares: articulosPopulares.length > 0 ? articulosPopulares : ['Sin reservas de artículos'],
                reservasSalas: Object.keys(salaCount).length,
                reservasArticulos: Object.keys(articuloCount).length,
                tendencia: reservasHoy > 0 ? 'up' : 'stable'
            };
        } catch (error) {
            console.error('❌ Error obteniendo stats de reservas reales:', error);
            return {
                totalReservas: 0,
                reservasHoy: 0,
                salasPopulares: ['Datos no disponibles'],
                tendencia: 'unknown',
                error: 'No se pudieron cargar las estadísticas'
            };
        }
    }

    /**
     * Obtener estadísticas de uso REALES desde la base de datos
     */
    async fetchUsageStats() {
        try {
            console.log('📈 Obteniendo estadísticas de uso REALES...');
            
            // Obtener datos reales desde las APIs existentes
            const [usuariosCount, articulosCount, salasCount, reservasCount] = await Promise.all([
                // Para usuarios, manejar el caso de que requiera autenticación
                this.apiRequest('/api/v1/personas/count/total').catch(async () => {
                    console.log('⚠️ API personas/count falló, intentando fallback...');
                    try {
                        // Fallback: obtener lista si está disponible (no forzar [] para distinguir error real)
                        const personas = await this.apiRequest('/api/v1/personas/');
                        const total = Array.isArray(personas) ? personas.length : 'N/A';
                        console.log('📋 Fallback personas lista:', Array.isArray(personas) ? total : 'falló');
                        return { total };
                    } catch {
                        // Si ambos fallan, mostrar que requiere permisos
                        console.log('❌ Ambas APIs de personas fallaron');
                        return { total: 'N/A' };
                    }
                }),
                this.apiRequest('/api/v1/articulos/count/total').catch((e) => {
                    console.log('❌ API artículos/count falló:', e);
                    return { total: 0 };
                }),
                this.apiRequest('/api/v1/salas/count/total').catch((e) => {
                    console.log('❌ API salas/count falló:', e);
                    return { total: 0 };
                }),
                this.apiRequest('/api/v1/reservas/').catch((e) => {
                    console.log('❌ API reservas falló:', e);
                    return [];
                })
            ]);

            console.log('📊 Respuestas de APIs:', {
                usuariosCount,
                articulosCount,
                salasCount,
                reservasCount: Array.isArray(reservasCount) ? `${reservasCount.length} reservas` : 'no es array'
            });

            // Calcular métricas reales
            const reservas = Array.isArray(reservasCount) ? reservasCount : [];
            let totalUsuarios = (typeof usuariosCount.total === 'number') ? usuariosCount.total : null;
            const totalArticulos = articulosCount.total || 0;
            const totalSalas = salasCount.total || 0;

            // Fallback: si no pudimos obtener el count de personas (403, etc.),
            // usar el total de usuarios únicos que reservaron SALAS (persona_id distinto)
            if (totalUsuarios === null) {
                try {
                    const usuariosDesdeReservasSala = new Set(
                        reservas
                            .filter(r => !!r.sala_id && !!r.persona_id)
                            .map(r => r.persona_id)
                    ).size;
                    totalUsuarios = usuariosDesdeReservasSala;
                } catch (_) {
                    totalUsuarios = 0;
                }
            }
            
            // Calcular disponibilidad real basada solo en reservas de SALAS hoy
            // Disponibilidad = salas NO reservadas hoy / total salas
            // Fecha local YYYY-MM-DD (evita desfasajes por UTC)
            const hoyDate2 = new Date();
            const hoy2 = `${hoyDate2.getFullYear()}-${String(hoyDate2.getMonth()+1).padStart(2,'0')}-${String(hoyDate2.getDate()).padStart(2,'0')}`;
            const salaIdsReservadasHoy = new Set(
                reservas
                    .filter(reserva => {
                        if (!reserva.fecha_hora_inicio) return false;
                        const d = new Date(reserva.fecha_hora_inicio);
                        const fechaReserva = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
                        // contar solo reservas de salas
                        return fechaReserva === hoy2 && !!reserva.sala_id;
                    })
                    .map(r => r.sala_id)
            );

            const reservasSalasHoyUnicas = salaIdsReservadasHoy.size;
            const salasLibresHoy = Math.max(0, totalSalas - reservasSalasHoyUnicas);
            const disponibilidadPromedio = totalSalas > 0 ?
                Math.round((salasLibresHoy / totalSalas) * 100) : 0;
            
            console.log('📊 Estadísticas reales calculadas:', {
                totalUsuarios,
                totalArticulos, 
                totalSalas,
                reservasActivas: reservas.length,
                reservasHoy: reservasSalasHoyUnicas,
                disponibilidadPromedio
            });
            
            return {
                usuariosActivos: totalUsuarios,
                articulosReservados: reservas.filter(r => !!r.articulo_id).length,
                disponibilidadPromedio: disponibilidadPromedio,
                satisfaccion: 0, // No tenemos datos de satisfacción aún
                totalSalas: totalSalas,
                totalArticulos: totalArticulos
            };
        } catch (error) {
            console.error('❌ Error obteniendo stats de uso reales:', error);
            
            // Fallback con datos claramente marcados como no disponibles
            return {
                usuariosActivos: 0,
                articulosReservados: 0,
                disponibilidadPromedio: 0,
                satisfaccion: 0,
                error: 'Datos no disponibles'
            };
        }
    }

    /**
     * Renderizar reportes en la página
     */
    renderReports() {
        console.log('🎨 Renderizando reportes...');
        
        const container = document.querySelector('.card-body');
        if (!container) {
            console.error('❌ Contenedor de reportes no encontrado');
            return;
        }
        
        // Limpiar contenido actual
        container.innerHTML = '';
        
        // Crear interfaz de reportes
        const reportsHTML = this.generateReportsHTML();
        container.innerHTML = reportsHTML;
        
        // Inicializar componentes interactivos
        this.initializeCharts();
        this.bindEventHandlers();
    }

    /**
     * Generar HTML para los reportes con datos dinámicos
     */
    generateReportsHTML() {
        const usageData = this.reports.find(r => r.id === 'usage-stats')?.data || {};
        const reservationData = this.reports.find(r => r.id === 'reservas-overview')?.data || {};
        
        return `
            <div class="reports-header mb-4">
                <div class="row align-items-center">
                    <div class="col">
                        <h4><i class="fas fa-chart-bar me-2"></i>Dashboard de Reportes</h4>
                        <p class="textContent mb-0">Métricas y analytics del sistema - <span class="badge bg-success">Datos en tiempo real</span></p>
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-outline-primary btn-sm me-2" onclick="window.reportesManager.refreshReports()">
                            <i class="fas fa-sync-alt me-1"></i>Actualizar
                        </button>
                        <button class="btn btn-primary btn-sm" onclick="window.reportesManager.exportReports()">
                            <i class="fas fa-download me-1"></i>Exportar
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header bg-primary text-white">
                            <h6 class="mb-0"><i class="fas fa-calendar me-1"></i>Reservas</h6>
                        </div>
                        <div class="card-body">
                            <div class="row text-center">
                                <div class="col-4">
                                    <div class="metric-item">
                                        <h3 class="text-primary mb-0">${reservationData.totalReservas || 0}</h3>
                                        <small class="textContent">Total Reservas</small>
                                    </div>
                                </div>
                                <div class="col-4">
                                    <div class="metric-item">
                                        <h3 class="text-success mb-0">${reservationData.reservasActivas || 0}</h3>
                                        <small class="textContent">Activas</small>
                                    </div>
                                </div>
                                <div class="col-4">
                                    <div class="metric-item">
                                        <h3 class="text-info mb-0">${reservationData.reservasFuturas || 0}</h3>
                                        <small class="textContent">Futuras</small>
                                    </div>
                                </div>
                            </div>
                            <hr class="my-3">
                            <div class="recursos-populares">
                                <h6 class="textContent mb-2">Recursos más reservados:</h6>
                                <div class="mb-2">
                                    <small class="text-primary">Salas:</small><br>
                                    ${(reservationData.salasPopulares || ['Sin datos']).map((sala, index) => 
                                        `<span class="badge bg-light text-primary border border-primary me-1">${index + 1}. ${sala}</span>`
                                    ).join('')}
                                </div>
                                ${reservationData.articulosPopulares && reservationData.articulosPopulares.length > 0 ? `
                                <div>
                                    <small class="text-info">Artículos:</small><br>
                                    ${reservationData.articulosPopulares.map((articulo, index) => 
                                        `<span class="badge bg-light text-info border border-info me-1">${index + 1}. ${articulo}</span>`
                                    ).join('')}
                                </div>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card border-0 shadow-sm h-100">
                        <div class="card-header bg-success text-white">
                            <h6 class="mb-0"><i class="fas fa-users me-1"></i>Sistema</h6>
                        </div>
                        <div class="card-body">
                            <div class="row text-center">
                                <div class="col-4">
                                    <div class="metric-item">
                                        <h3 class="text-success mb-0">${usageData.disponibilidadPromedio || 0}%</h3>
                                        <small class="textContent">Disponibilidad</small>
                                    </div>
                                </div>
                                <div class="col-4">
                                    <div class="metric-item">
                                        <h3 class="text-warning mb-0">${usageData.totalSalas || 0}</h3>
                                        <small class="textContent">Total Salas</small>
                                    </div>
                                </div>
                                <div class="col-4">
                                    <div class="metric-item">
                                        <h3 class="text-info mb-0">${usageData.totalArticulos || 0}</h3>
                                        <small class="textContent">Artículos</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        <strong>Datos en Tiempo Real:</strong> 
                        Las métricas se actualizan automáticamente desde la base de datos del sistema.
                        ${usageData.error ? `<br><span class="text-warning">⚠️ Algunos datos no están disponibles: ${usageData.error}</span>` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Inicializar gráficos (placeholder para Charts.js u otra librería)
     */
    initializeCharts() {
        console.log('📊 Inicializando gráficos...');
        // Aquí se inicializarían librerías como Chart.js, D3, etc.
    }

    /**
     * Vincular event handlers
     */
    bindEventHandlers() {
        // Los botones ya tienen onclick handlers
        console.log('🔗 Event handlers vinculados');
    }

    /**
     * Configurar auto-refresh
     */
    setupAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        
        this.refreshTimer = setInterval(() => {
            this.refreshReports();
        }, this.config.refreshInterval);
        
        console.log(`🔄 Auto-refresh configurado cada ${this.config.refreshInterval/1000}s`);
    }

    /**
     * Actualizar reportes
     */
    async refreshReports() {
        console.log('🔄 Actualizando reportes...');
        try {
            await this.loadReportData();
            this.renderReports();
            this.showSuccess('Reportes actualizados correctamente');
        } catch (error) {
            console.error('❌ Error actualizando reportes:', error);
            this.showError('Error al actualizar los reportes');
        }
    }

    /**
     * Exportar reportes
     */
    exportReports() {
        console.log('📥 Exportando reportes...');
        // Implementación futura de exportación
        this.showInfo('Funcionalidad de exportación próximamente disponible');
    }

    /**
     * Realizar petición a la API
     */
    async apiRequest(url) {
        try {
            const headers = {
                'Accept': 'application/json'
            };
            // Incluir Authorization si el AuthManager dispone de token
            try {
                const accessToken = window.authManager?.getAccessToken?.();
                if (accessToken) {
                    headers['Authorization'] = `Bearer ${accessToken}`;
                }
            } catch (_) { /* noop */ }

            const response = await fetch(url, {
                // Enviar cookies de autenticación (JWT HTTP-only) en mismas rutas
                credentials: 'same-origin',
                headers,
                cache: 'no-store'
            });
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`❌ Error en API ${url}:`, error);
            throw error;
        }
    }

    /**
     * Mostrar mensaje de éxito
     */
    showSuccess(message) {
        if (window.showSuccess) {
            window.showSuccess(message);
        } else {
            console.log(`✅ ${message}`);
        }
    }

    /**
     * Mostrar mensaje de error
     */
    showError(message) {
        if (window.showError) {
            window.showError(message);
        } else {
            console.error(`❌ ${message}`);
            alert(message); // Fallback
        }
    }

    /**
     * Mostrar mensaje de información
     */
    showInfo(message) {
        if (window.showInfo) {
            window.showInfo(message);
        } else {
            console.log(`ℹ️ ${message}`);
        }
    }

    /**
     * Destruir instancia (cleanup)
     */
    destroy() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        this.isInitialized = false;
    }
}

// Funciones globales para compatibilidad con onclick en HTML
window.refreshReports = function() {
    if (window.reportesManager) {
        window.reportesManager.refreshReports();
    }
};

window.exportReports = function() {
    if (window.reportesManager) {
        window.reportesManager.exportReports();
    }
};

// Auto-inicializar cuando se carga el módulo
// Nota: La inicialización real se hace en el constructor, que maneja el timing del DOM
window.reportesManager = new ReportesManager();

console.log('📊 Reportes module loaded');

// Export para módulos ES6 si se necesita
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReportesManager;
}