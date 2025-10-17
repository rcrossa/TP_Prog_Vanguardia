/**
 * Sistema de Toast Notifications reutilizable
 * Dependencias: Bootstrap 5
 */

/**
 * Muestra un toast de éxito
 * @param {string} message - Mensaje a mostrar
 */
function showSuccess(message) {
    showToast(message, 'success');
}

/**
 * Muestra un toast de error
 * @param {string} message - Mensaje a mostrar
 */
function showError(message) {
    showToast(message, 'danger');
}

/**
 * Muestra un toast de información
 * @param {string} message - Mensaje a mostrar
 */
function showInfo(message) {
    showToast(message, 'info');
}

/**
 * Muestra un toast de advertencia
 * @param {string} message - Mensaje a mostrar
 */
function showWarning(message) {
    showToast(message, 'warning');
}

/**
 * Función principal para mostrar toasts
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo de toast (success, danger, info, warning)
 */
function showToast(message, type = 'success') {
    // Crear contenedor si no existe
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    // Configuración de colores y iconos
    const toastConfig = {
        success: { bgClass: 'bg-success', icon: '✅', textClass: 'text-white' },
        danger: { bgClass: 'bg-danger', icon: '❌', textClass: 'text-white' },
        info: { bgClass: 'bg-info', icon: 'ℹ️', textClass: 'text-white' },
        warning: { bgClass: 'bg-warning', icon: '⚠️', textClass: 'text-dark' }
    };

    const config = toastConfig[type] || toastConfig.success;

    // Crear elemento toast
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast ${config.bgClass} ${config.textClass}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header ${config.bgClass} ${config.textClass} border-0">
                <span class="me-2">${config.icon}</span>
                <strong class="me-auto">Notificación</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;

    // Insertar toast en el contenedor
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Activar el toast
    const toastElement = document.getElementById(toastId);
    const bsToast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 4000
    });

    // Limpiar elemento cuando se oculte
    toastElement.addEventListener('hidden.bs.toast', function () {
        toastElement.remove();
    });

    // Mostrar el toast
    bsToast.show();
}

/**
 * Oculta todos los toasts activos
 */
function hideAllToasts() {
    const toastContainer = document.getElementById('toast-container');
    if (toastContainer) {
        const toasts = toastContainer.querySelectorAll('.toast');
        toasts.forEach(toast => {
            const bsToast = bootstrap.Toast.getInstance(toast);
            if (bsToast) {
                bsToast.hide();
            }
        });
    }
}