/**
 * Template Bridge - Utilidad para manejar datos Jinja2 en módulos JavaScript
 * 
 * Esta clase proporciona una interfaz limpia para acceder a datos que vienen
 * desde el backend Python/Jinja2 hacia los módulos JavaScript frontales.
 * 
 * Patrón de uso:
 * 1. El template HTML embebe datos en un <script id="template-data" type="application/json">
 * 2. Los módulos JavaScript usan TemplateBridge.getData() para acceder a los datos
 * 3. Se mantiene separación limpia entre template y lógica JavaScript
 */

class TemplateBridge {
    constructor() {
        this.data = null;
        this.loadTemplateData();
    }

    /**
     * Carga datos del template desde el script tag embebido
     */
    loadTemplateData() {
        try {
            const templateDataElement = document.getElementById('template-data');
            if (templateDataElement) {
                this.data = JSON.parse(templateDataElement.textContent);
                console.log('✅ Template data loaded successfully:', Object.keys(this.data));
            } else {
                console.warn('⚠️ No template-data element found');
                this.data = {};
            }
        } catch (error) {
            console.error('❌ Error loading template data:', error);
            this.data = {};
        }
    }

    /**
     * Obtiene todos los datos del template
     * @returns {Object} Datos completos del template
     */
    getData() {
        return this.data;
    }

    /**
     * Obtiene un valor específico por clave
     * @param {string} key - Clave del dato a obtener
     * @param {*} defaultValue - Valor por defecto si la clave no existe
     * @returns {*} Valor solicitado o valor por defecto
     */
    get(key, defaultValue = null) {
        return this.data?.[key] ?? defaultValue;
    }

    /**
     * Obtiene un endpoint de API por nombre
     * @param {string} endpointName - Nombre del endpoint
     * @returns {string|null} URL del endpoint o null si no existe
     */
    getEndpoint(endpointName) {
        return this.data?.apiEndpoints?.[endpointName] ?? null;
    }

    /**
     * Obtiene datos iniciales específicos
     * @param {string} key - Clave de los datos iniciales
     * @param {*} defaultValue - Valor por defecto
     * @returns {*} Datos iniciales solicitados
     */
    getInitialData(key, defaultValue = null) {
        return this.data?.initialData?.[key] ?? defaultValue;
    }

    /**
     * Verifica si una clave existe en los datos
     * @param {string} key - Clave a verificar
     * @returns {boolean} True si la clave existe
     */
    has(key) {
        return key in (this.data || {});
    }

    /**
     * Obtiene configuración específica
     * @param {string} configKey - Clave de configuración
     * @param {*} defaultValue - Valor por defecto
     * @returns {*} Configuración solicitada
     */
    getConfig(configKey, defaultValue = null) {
        return this.data?.config?.[configKey] ?? defaultValue;
    }

    /**
     * Método de debugging para inspeccionar datos cargados
     */
    debugData() {
        console.group('🔍 Template Bridge Debug Data');
        console.log('Raw data:', this.data);
        if (this.data) {
            Object.keys(this.data).forEach(key => {
                console.log(`- ${key}:`, typeof this.data[key], this.data[key]);
            });
        }
        console.groupEnd();
    }
}

// Crear instancia global para uso en módulos
window.templateBridge = new TemplateBridge();

// Export para módulos ES6 si se necesita
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TemplateBridge;
}