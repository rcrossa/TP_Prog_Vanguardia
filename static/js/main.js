// JavaScript principal para el Sistema de Reservas

// Configuración global de Axios
axios.defaults.baseURL = '';
axios.defaults.timeout = 10000;
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Note: Los interceptors de autenticación están manejados en auth.js

// Sistema de notificaciones Toast
function showToast(message, type = 'info', duration = 5000) {
    // Crear contenedor de toasts si no existe
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }

    // Crear toast
    const toastId = 'toast-' + Date.now();
    const iconMap = {
        success: 'fas fa-check-circle',
        error: 'fas fa-times-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };

    const colorMap = {
        success: 'text-success',
        error: 'text-danger',
        warning: 'text-warning',
        info: 'text-primary'
    };

    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = 'toast align-items-center border-0 fade show';
    toast.setAttribute('role', 'alert');

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body d-flex align-items-center">
                <i class="${iconMap[type]} ${colorMap[type]} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toast);

    // Auto-hide
    setTimeout(() => {
        const bsToast = new bootstrap.Toast(toast);
        bsToast.hide();

        // Remover del DOM después de la animación
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 500);
    }, duration);
}

// Función para formatear fechas
function formatDate(dateString) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

// Función para formatear fechas cortas
function formatDateShort(dateString) {
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

// Debounce para búsquedas
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Validadores comunes
const validators = {
    email: (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email),
    minLength: (text, min) => text && text.length >= min,
    required: (value) => value !== null && value !== undefined && value.trim() !== '',
    numeric: (value) => !isNaN(value) && !isNaN(parseFloat(value))
};

// Cliente para microservicio Java
class JavaServiceClient {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
        this.client = axios.create({
            baseURL: baseURL,
            timeout: 5000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

    async checkHealth() {
        try {
            const response = await this.client.get('/actuator/health');
            return response.data.status === 'UP';
        } catch (error) {
            return false;
        }
    }

    async getArticulos(params = {}) {
        const response = await this.client.get('/api/v1/articulos', { params });
        return response.data;
    }

    async getArticulo(id) {
        const response = await this.client.get(`/api/v1/articulos/${id}`);
        return response.data;
    }

    async createArticulo(data) {
        const response = await this.client.post('/api/v1/articulos', data);
        return response.data;
    }

    async updateArticulo(id, data) {
        const response = await this.client.put(`/api/v1/articulos/${id}`, data);
        return response.data;
    }

    async deleteArticulo(id) {
        await this.client.delete(`/api/v1/articulos/${id}`);
    }

    async countArticulos(disponible = null) {
        const params = disponible !== null ? { disponible } : {};
        const response = await this.client.get('/api/v1/articulos/count/total', { params });
        return response.data;
    }

    async toggleDisponibilidad(id) {
        const response = await this.client.patch(`/api/v1/articulos/${id}/toggle-disponibilidad`);
        return response.data;
    }

    async getReportes() {
        const response = await this.client.get('/api/v1/reportes');
        return response.data;
    }

    async getPredicciones() {
        const response = await this.client.get('/api/v1/predicciones');
        return response.data;
    }
}

// Instancia global del cliente Java
const javaService = new JavaServiceClient();

// Funciones de utilidad para el DOM
function showElement(selector) {
    const element = document.querySelector(selector);
    if (element) element.style.display = 'block';
}

function hideElement(selector) {
    const element = document.querySelector(selector);
    if (element) element.style.display = 'none';
}

function toggleElement(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'block' : 'none';
    }
}

// Manejo de loading states
function setLoadingState(selector, isLoading = true) {
    const element = document.querySelector(selector);
    if (!element) return;

    if (isLoading) {
        element.innerHTML = `
            <span class="spinner-border spinner-border-sm me-1" role="status"></span>
            Cargando...
        `;
        element.disabled = true;
    } else {
        element.disabled = false;
    }
}

// Confirmar acciones peligrosas
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Event listeners globales
document.addEventListener('DOMContentLoaded', function() {
    // Resaltar navegación activa
    highlightActiveNavigation();

    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers de Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Resaltar navegación activa
function highlightActiveNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Manejo de errores de red
window.addEventListener('online', function() {
    showToast('Conexión restablecida', 'success');
});

window.addEventListener('offline', function() {
    showToast('Sin conexión a internet', 'warning');
});

// Exportar funciones útiles al scope global
window.showToast = showToast;
window.formatDate = formatDate;
window.formatDateShort = formatDateShort;
window.validators = validators;
window.javaService = javaService;
window.confirmAction = confirmAction;