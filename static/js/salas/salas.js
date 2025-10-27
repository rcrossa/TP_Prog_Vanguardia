/**
 * JavaScript para gestión de salas
 * Dependencias: axios, bootstrap, toast-notifications.js
 */

// Variables globales
let salas = [];
let isAdmin = false;
let salaModal;
let salaToDelete = null;

// 🔒 SEGURIDAD PRE-RENDER: Aplicar clase admin INMEDIATAMENTE
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

/**
 * Cargar salas desde la API
 */
async function loadSalas() {
    try {
        const response = await axios.get('/api/v1/salas/');
        // Limpiar y actualizar la variable global correctamente
        salas = Array.isArray(response.data) ? response.data.slice() : [];
        renderSalas(salas);
    } catch (error) {
        salas = [];
        renderSalas(salas);
        console.error('Error al cargar salas:', error);
        showError('Error al cargar las salas');
    }
}

/**
 * Renderizar tabla de salas
 */
function renderSalas(salasToRender) {
    const tbody = document.getElementById('salasTableBody');
    
    if (salasToRender.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="${isAdmin ? 5 : 4}" class="text-center py-4">
                    <i class="fas fa-door-open fa-2x text-muted mb-2"></i>
                    <p class="text-muted mb-0">No hay salas disponibles</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = salasToRender.map(sala => `
        <tr>
            <td><span class="badge bg-secondary">${sala.id}</span></td>
            <td>
                <div class="d-flex align-items-center">
                    <div class="avatar-sm bg-info rounded-circle d-flex align-items-center justify-content-center me-2">
                        <i class="fas fa-door-open text-white small"></i>
                    </div>
                    <strong>${sala.nombre}</strong>
                </div>
            </td>
            <td>
                <span class="badge bg-primary">${sala.capacidad} personas</span>
            </td>
            ${!isAdmin ? `
                <td>
                    <span class="badge bg-success">
                        <i class="fas fa-check me-1"></i>Disponible
                    </span>
                </td>
            ` : ''}
            ${isAdmin ? `
                <td>
                    <div class="btn-group btn-group-sm">
                            <div class="d-flex gap-2 btn-equal-group">
                                <button class="btn btn-sm btn-outline-primary btn-3d flex-fill" onclick="editSala(${sala.id})" aria-label="Editar" title="Editar">
                                    <i class="fas fa-edit" aria-hidden="true"></i>
                                    <span class="visually-hidden">Editar</span>
                                </button>
                                <button class="btn btn-sm btn-outline-danger btn-3d flex-fill" onclick="deleteSala(${sala.id})" aria-label="Eliminar" title="Eliminar">
                                    <i class="fas fa-trash" aria-hidden="true"></i>
                                    <span class="visually-hidden">Eliminar</span>
                                </button>
                            </div>
                    </div>
                </td>
            ` : ''}
        </tr>
    `).join('');
}

/**
 * Actualizar página según rol de usuario
 */
function updatePageForUserRole(user) {
    isAdmin = user && user.is_admin === true;
    
    if (isAdmin) {
        document.querySelectorAll('.admin-only').forEach(el => el.style.display = 'block');
        document.querySelectorAll('.user-only').forEach(el => el.style.display = 'none');
    } else {
        document.querySelectorAll('.admin-only').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.user-only').forEach(el => el.style.display = 'table-cell');
    }
}

/**
 * Abrir modal para nueva sala
 */
function openNewSalaModal() {
    document.getElementById('salaModalLabel').textContent = 'Nueva Sala';
    document.getElementById('salaForm').reset();
    document.getElementById('salaId').value = '';
    
    salaModal.show();
}

/**
 * Editar sala existente
 */
async function editSala(id) {
    try {
        const response = await axios.get(`/api/v1/salas/${id}`);
        const sala = response.data;
        
        document.getElementById('salaModalLabel').textContent = 'Editar Sala';
        document.getElementById('salaId').value = sala.id;
        document.getElementById('nombre').value = sala.nombre;
        document.getElementById('capacidad').value = sala.capacidad;
        
        salaModal.show();
    } catch (error) {
        console.error('Error al cargar sala:', error);
        showError('Error al cargar los datos de la sala');
    }
}

/**
 * Guardar sala (crear o actualizar)
 */
async function saveSala() {
    const id = document.getElementById('salaId').value;
    const nombre = document.getElementById('nombre').value.trim();
    const capacidad = parseInt(document.getElementById('capacidad').value);
    
    if (!nombre || !capacidad || capacidad <= 0) {
        showError('Por favor, complete todos los campos correctamente');
        return;
    }
    
    try {
        const salaData = { nombre, capacidad };
        
        if (id) {
            // Actualizar sala existente
            await axios.put(`/api/v1/salas/${id}`, salaData);
            showSuccess('Sala actualizada exitosamente');
        } else {
            // Crear nueva sala
            await axios.post('/api/v1/salas/', salaData);
            showSuccess('Sala creada exitosamente');
        }
        
        // Limpiar el formulario antes de cerrar el modal
        document.getElementById('salaForm').reset();
        await loadSalas();
        salaModal.hide();
    } catch (error) {
        console.error('Error al guardar sala:', error);
        if (error.response?.data?.detail) {
            showError(error.response.data.detail);
        } else {
            showError('Error al guardar la sala');
        }
    }
}

/**
 * Mostrar modal de confirmación para eliminar sala
 */
async function deleteSala(id) {
    salaToDelete = id;
    const sala = salas.find(s => s.id === id);
    document.getElementById('salaNameToDelete').textContent = sala ? sala.nombre : 'esta sala';
    
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    confirmModal.show();
}

/**
 * Confirmar eliminación de sala
 */
async function confirmDelete() {
    if (!salaToDelete) return;
    const deleteBtn = document.querySelector('#confirmDeleteModal .btn-danger');
    const originalText = deleteBtn.innerHTML;
    deleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Eliminando...';
    deleteBtn.disabled = true;
    try {
        await axios.delete(`/api/v1/salas/${salaToDelete}`);
        showSuccess('Sala eliminada exitosamente');
        await loadSalas();
        const confirmModal = bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal'));
        confirmModal.hide();
        salaToDelete = null;
    } catch (error) {
        console.error('Error al eliminar sala:', error);
            let errorMsg = 'No se pudo eliminar la sala. El sistema de gestión de salas no está disponible. Intente más tarde.';
            if (error.response?.data?.detail) {
                // Si el backend envía un mensaje específico, lo mostramos
                if (error.response.data.detail.includes('No se encontró una sala')) {
                    errorMsg = 'La sala ya fue eliminada o sincronizada previamente.';
                } else {
                    errorMsg = error.response.data.detail;
                }
            }
            showError(errorMsg);
            const confirmModal = bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal'));
            confirmModal.hide();
    } finally {
        deleteBtn.innerHTML = originalText;
        deleteBtn.disabled = false;
    }
}

/**
 * Aplicar filtros a las salas
 */
function applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const capacityFilter = document.getElementById('filterCapacity').value;
    
    let filteredSalas = salas.filter(sala => {
        const matchesSearch = sala.nombre.toLowerCase().includes(searchTerm);
        const matchesCapacity = !capacityFilter || 
            (capacityFilter === 'small' && sala.capacidad <= 10) ||
            (capacityFilter === 'medium' && sala.capacidad > 10 && sala.capacidad <= 50) ||
            (capacityFilter === 'large' && sala.capacidad > 50);
        
        return matchesSearch && matchesCapacity;
    });
    
    renderSalas(filteredSalas);
}

/**
 * Inicialización cuando el DOM está listo
 */
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar modal
    const salaModalElement = document.getElementById('salaModal');
    if (salaModalElement) {
        salaModal = new bootstrap.Modal(salaModalElement);
    }
    
    // Obtener información del usuario y configurar la página
    const user = window.authManager ? window.authManager.getUser() : null;
    updatePageForUserRole(user);
    
    // Cargar salas
    loadSalas();
    
    // Configurar eventos de filtrado
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', applyFilters);
    }
    
    const filterCapacity = document.getElementById('filterCapacity');
    if (filterCapacity) {
        filterCapacity.addEventListener('change', applyFilters);
    }
    
    // Configurar eventos del formulario
    const salaForm = document.getElementById('salaForm');
    if (salaForm) {
        salaForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveSala();
        });
    }
});

/**
 * Wrappers para mantener compatibilidad con funciones legacy de toast
 */
window.showToast = window.showToast || function(message, type = 'success') {
    if (typeof showSuccess === 'function') {
        if (type === 'success') showSuccess(message);
        else if (type === 'danger' || type === 'error') showError(message);
        else if (type === 'info') showInfo(message);
        else if (type === 'warning') showWarning(message);
    }
};