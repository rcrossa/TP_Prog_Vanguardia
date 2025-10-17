/**
 * Documentación Module - Gestión de Markmap para documentación del proyecto
 * 
 * Este módulo maneja toda la funcionalidad del mapa mental de documentación:
 * - Inicialización de Markmap
 * - Controles de zoom y navegación
 * - Modo de pantalla completa
 * - Gestión de estados visuales
 */

class DocumentacionManager {
    constructor() {
        this.markmapInstance = null;
        this.isFullscreen = false;
        this.markdownContent = null;
        
        // Configuración por defecto
        this.config = {
            duration: 500,
            maxWidth: 300,
            paddingX: 20,
            autoFit: true,
            initialExpandLevel: 2,
            colors: ['#4285f4', '#34a853', '#fbbc04', '#ea4335', '#9c27b0']
        };
        
        this.init();
    }

    /**
     * Inicialización del módulo
     */
    init() {
        // Obtener datos del template bridge
        this.loadTemplateData();
        
        // Esperar a que el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initMarkmap());
        } else {
            this.initMarkmap();
        }
        
        // Escuchar eventos de fullscreen
        this.setupFullscreenEvents();
    }

    /**
     * Cargar datos desde el template bridge
     */
    loadTemplateData() {
        try {
            this.markdownContent = window.templateBridge.get('markdownContent');
            
            // Merge configuración del template si existe
            const templateConfig = window.templateBridge.get('markmapConfig', {});
            this.config = { ...this.config, ...templateConfig };
            
            console.log('📄 Markdown content loaded for documentation');
        } catch (error) {
            console.error('❌ Error loading template data:', error);
        }
    }

    /**
     * Función para inicializar el mapa mental
     */
    async initMarkmap() {
        try {
            // Verificar que tenemos contenido markdown
            if (!this.markdownContent) {
                console.error('❌ No markdown content available');
                return;
            }

            // Esperar a que markmap esté disponible
            if (typeof markmap === 'undefined') {
                console.log('⏳ Esperando a que Markmap se cargue...');
                setTimeout(() => this.initMarkmap(), 100);
                return;
            }
            
            const { Markmap, loadCSS, loadJS } = markmap;
            
            // Crear instancia de Markmap con configuración
            this.markmapInstance = Markmap.create('#markmap-container', {
                duration: this.config.duration,
                maxWidth: this.config.maxWidth,
                color: (node) => {
                    // Colores según el nivel de profundidad
                    return this.config.colors[node.depth % this.config.colors.length];
                },
                paddingX: this.config.paddingX,
                autoFit: this.config.autoFit,
                initialExpandLevel: this.config.initialExpandLevel
            });
            
            // Transformar el markdown y renderizar
            const { root } = markmap.transform(this.markdownContent);
            this.markmapInstance.setData(root);
            this.markmapInstance.fit();
            
            // Guardar referencia global para compatibilidad
            window.markmapInstance = this.markmapInstance;
            
            console.log('✅ Markmap initialized successfully');
            
        } catch (error) {
            console.error('❌ Error al inicializar Markmap:', error);
            this.showError('Error al cargar el mapa mental');
        }
    }

    /**
     * Funciones de control de zoom
     */
    zoomIn() {
        if (this.markmapInstance) {
            const svg = this.markmapInstance.svg;
            const currentScale = svg.getScale();
            svg.setScale(currentScale * 1.2);
            console.log('🔍 Zoom in applied');
        }
    }
    
    zoomOut() {
        if (this.markmapInstance) {
            const svg = this.markmapInstance.svg;
            const currentScale = svg.getScale();
            svg.setScale(currentScale / 1.2);
            console.log('🔍 Zoom out applied');
        }
    }
    
    resetZoom() {
        if (this.markmapInstance) {
            this.markmapInstance.fit();
            console.log('🔄 Zoom reset');
        }
    }

    /**
     * Configurar eventos de fullscreen
     */
    setupFullscreenEvents() {
        document.addEventListener('fullscreenchange', () => {
            this.isFullscreen = !!document.fullscreenElement;
            this.updateFullscreenIcon();
        });
    }

    /**
     * Toggle modo pantalla completa
     */
    async toggleFullscreen() {
        try {
            const container = document.querySelector('.container-fluid');
            
            if (!this.isFullscreen) {
                await container.requestFullscreen();
                console.log('📺 Entering fullscreen mode');
            } else {
                await document.exitFullscreen();
                console.log('📺 Exiting fullscreen mode');
            }
        } catch (error) {
            console.error('❌ Error al cambiar pantalla completa:', error);
        }
    }

    /**
     * Actualizar icono de fullscreen
     */
    updateFullscreenIcon() {
        const fullscreenBtn = document.querySelector('button[onclick*="toggleFullscreen"]');
        if (fullscreenBtn) {
            const icon = fullscreenBtn.querySelector('i');
            if (this.isFullscreen) {
                icon.classList.replace('fa-expand', 'fa-compress');
                fullscreenBtn.title = 'Salir de pantalla completa';
            } else {
                icon.classList.replace('fa-compress', 'fa-expand');
                fullscreenBtn.title = 'Pantalla completa';
            }
        }
    }

    /**
     * Mostrar mensaje de error
     */
    showError(message) {
        // Usar el sistema centralizado de toast si está disponible
        if (window.showError) {
            window.showError(message);
        } else {
            console.error(message);
            alert(message); // Fallback básico
        }
    }

    /**
     * Recargar el mapa mental con nuevo contenido
     * @param {string} newMarkdownContent - Nuevo contenido markdown
     */
    updateContent(newMarkdownContent) {
        this.markdownContent = newMarkdownContent;
        if (this.markmapInstance) {
            const { root } = markmap.transform(this.markdownContent);
            this.markmapInstance.setData(root);
            this.markmapInstance.fit();
            console.log('🔄 Content updated');
        }
    }

    /**
     * Destruir instancia (cleanup)
     */
    destroy() {
        if (this.markmapInstance) {
            this.markmapInstance = null;
            window.markmapInstance = null;
        }
    }
}

// Funciones globales para compatibilidad con onclick en HTML
window.zoomIn = function() {
    if (window.documentacionManager) {
        window.documentacionManager.zoomIn();
    }
};

window.zoomOut = function() {
    if (window.documentacionManager) {
        window.documentacionManager.zoomOut();
    }
};

window.resetZoom = function() {
    if (window.documentacionManager) {
        window.documentacionManager.resetZoom();
    }
};

window.toggleFullscreen = function() {
    if (window.documentacionManager) {
        window.documentacionManager.toggleFullscreen();
    }
};

// Auto-inicializar cuando se carga el módulo
document.addEventListener('DOMContentLoaded', () => {
    window.documentacionManager = new DocumentacionManager();
    console.log('📚 Documentación module loaded and initialized');
});

// Export para módulos ES6 si se necesita
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DocumentacionManager;
}