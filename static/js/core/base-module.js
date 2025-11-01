/**
 * Base Module - Clase base para módulos de templates con funcionalidad común
 *
 * Esta clase proporciona funcionalidad compartida que todos los módulos pueden usar:
 * - Verificación de autenticación y permisos
 * - Seguridad pre-render
 * - Integración con template bridge
 * - Sistema de notificaciones
 * - Manejo de errores
 * - Ciclo de vida del módulo
 */

class BaseModule {
    constructor(moduleName, options = {}) {
        this.moduleName = moduleName;
        this.isInitialized = false;
        this.requiresAuth = options.requiresAuth !== false; // Por defecto requiere auth
        this.requiresAdmin = options.requiresAdmin || false;
        this.autoInit = options.autoInit !== false; // Por defecto auto-inicializa

        // Configuración por defecto
        this.config = {
            debug: false,
            autoRefresh: false,
            refreshInterval: 30000,
            ...options.config
        };

        this.log(`🚀 Inicializando módulo ${this.moduleName}`);

        if (this.autoInit) {
            this.init();
        }
    }

    /**
     * Inicialización del módulo base
     */
    init() {
        // Aplicar seguridad pre-render si se requiere
        if (this.requiresAuth) {
            this.applyPreRenderSecurity();
        }

        // Esperar a que el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeModule());
        } else {
            this.initializeModule();
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
                    this.log('🔐 Clase admin aplicada');
                } else {
                    document.body.classList.remove('is-admin');
                }
            } else {
                document.body.classList.remove('is-admin');
            }
        } catch (e) {
            this.error('Error al verificar rol de admin:', e);
            document.body.classList.remove('is-admin');
        }
    }

    /**
     * Inicialización del módulo después de que el DOM esté listo
     */
    initializeModule() {
        this.log('📄 DOM listo, inicializando módulo...');

        // Cargar configuración del template bridge
        this.loadTemplateConfig();

        if (this.requiresAuth) {
            this.checkAuthAndPermissions();
        } else {
            // Si no requiere auth, ir directo a la inicialización específica
            this.onReady();
        }
    }

    /**
     * Cargar configuración desde template bridge
     */
    loadTemplateConfig() {
        try {
            if (window.templateBridge) {
                const moduleConfig = window.templateBridge.get(`${this.moduleName}Config`, {});
                this.config = { ...this.config, ...moduleConfig };

                // Cargar datos iniciales si existen
                this.initialData = window.templateBridge.get('initialData', {});

                this.log('📋 Configuración cargada desde template bridge');
            }
        } catch (error) {
            this.error('Error cargando configuración del template:', error);
        }
    }

    /**
     * Verificación de autenticación y permisos
     */
    checkAuthAndPermissions() {
        const checkAuth = () => {
            if (!window.authManager) {
                this.log('⏳ Esperando AuthManager...');
                setTimeout(checkAuth, 100);
                return;
            }

            // Verificar que el usuario esté autenticado
            if (!window.authManager.isAuthenticated()) {
                this.log('❌ Usuario no autenticado, redirigiendo...');
                window.location.href = '/login';
                return;
            }

            // Verificar permisos de admin si se requiere
            if (this.requiresAdmin) {
                const user = window.authManager.getUser();
                if (!user || !user.is_admin) {
                    this.log('❌ Acceso denegado - no es admin');
                    this.showError('Acceso denegado. Solo los administradores pueden acceder a esta sección.');
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                    return;
                }
            }

            this.log('✅ Autenticación y permisos verificados');
            this.onReady();
        };

        checkAuth();
    }

    /**
     * Método que se ejecuta cuando el módulo está listo
     * Debe ser sobrescrito por las clases hijas
     */
    onReady() {
        this.log('✅ Módulo listo');
        this.isInitialized = true;

        // Llamar al método específico del módulo si existe
        if (typeof this.initSpecific === 'function') {
            this.initSpecific();
        }
    }

    /**
     * Sistema de logging con prefijo del módulo
     */
    log(...args) {
        if (this.config.debug) {
            console.log(`[${this.moduleName}]`, ...args);
        }
    }

    /**
     * Sistema de logging de errores
     */
    error(...args) {
        console.error(`[${this.moduleName}]`, ...args);
    }

    /**
     * Sistema de logging de warnings
     */
    warn(...args) {
        console.warn(`[${this.moduleName}]`, ...args);
    }

    /**
     * Mostrar mensaje de éxito usando el sistema centralizado
     */
    showSuccess(message) {
        if (window.showSuccess) {
            window.showSuccess(message);
        } else if (window.showToast) {
            window.showToast(message, 'success');
        } else {
            this.log(`✅ ${message}`);
        }
    }

    /**
     * Mostrar mensaje de error usando el sistema centralizado
     */
    showError(message) {
        if (window.showError) {
            window.showError(message);
        } else if (window.showToast) {
            window.showToast(message, 'danger');
        } else {
            this.error(`❌ ${message}`);
            alert(message); // Fallback básico
        }
    }

    /**
     * Mostrar mensaje de información usando el sistema centralizado
     */
    showInfo(message) {
        if (window.showInfo) {
            window.showInfo(message);
        } else if (window.showToast) {
            window.showToast(message, 'info');
        } else {
            this.log(`ℹ️ ${message}`);
        }
    }

    /**
     * Mostrar mensaje de warning usando el sistema centralizado
     */
    showWarning(message) {
        if (window.showWarning) {
            window.showWarning(message);
        } else if (window.showToast) {
            window.showToast(message, 'warning');
        } else {
            this.warn(`⚠️ ${message}`);
        }
    }

    /**
     * Obtener endpoint desde template bridge
     */
    getEndpoint(endpointName) {
        return window.templateBridge?.getEndpoint(endpointName) || null;
    }

    /**
     * Hacer petición HTTP con manejo de errores estándar
     */
    async apiRequest(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            this.error(`Error en petición a ${url}:`, error);
            throw error;
        }
    }

    /**
     * Configurar auto-refresh si está habilitado
     */
    setupAutoRefresh(refreshFunction) {
        if (!this.config.autoRefresh) return;

        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }

        this.refreshTimer = setInterval(() => {
            this.log('🔄 Auto-refresh ejecutándose...');
            refreshFunction.call(this);
        }, this.config.refreshInterval);

        this.log(`🔄 Auto-refresh configurado cada ${this.config.refreshInterval/1000}s`);
    }

    /**
     * Bindear eventos del DOM con manejo de errores
     */
    bindEvents(events) {
        Object.entries(events).forEach(([selector, handler]) => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                element.addEventListener('click', (event) => {
                    try {
                        handler.call(this, event);
                    } catch (error) {
                        this.error(`Error en event handler para ${selector}:`, error);
                    }
                });
            });
        });
    }

    /**
     * Destruir instancia y limpiar recursos
     */
    destroy() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }

        this.isInitialized = false;
        this.log('🧹 Módulo destruido y recursos limpiados');
    }

    /**
     * Obtener información del usuario actual
     */
    getCurrentUser() {
        return window.authManager?.getUser() || null;
    }

    /**
     * Verificar si el usuario actual es admin
     */
    isCurrentUserAdmin() {
        const user = this.getCurrentUser();
        return user && user.is_admin === true;
    }

    /**
     * Formatear fechas de manera consistente
     */
    formatDate(date, format = 'locale') {
        if (!date) return '';

        const d = new Date(date);
        if (isNaN(d.getTime())) return '';

        switch (format) {
            case 'locale':
                return d.toLocaleDateString();
            case 'datetime':
                return d.toLocaleString();
            case 'iso':
                return d.toISOString();
            default:
                return d.toString();
        }
    }

    /**
     * Debounce function para evitar llamadas excesivas
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func.apply(this, args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Export para módulos ES6 si se necesita
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BaseModule;
}

// Hacer disponible globalmente
window.BaseModule = BaseModule;