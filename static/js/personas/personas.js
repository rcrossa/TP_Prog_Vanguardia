/**
 * Unificado: JS para gestión de personas
 * Este archivo contiene toda la lógica de personas (cargar, renderizar, crear, editar, eliminar, filtrar, validar, seguridad)
 * Dependencias: axios, bootstrap, toast-notifications.js
 */

// Variables globales
let currentPersonaId = null;
let personas = [];

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

// Inicialización específica de la página de personas
document.addEventListener('DOMContentLoaded', function() {
    // Seguridad: Verificar autenticación y permisos
    const checkAuth = () => {
        if (!window.authManager) {
            window.location.href = '/login';
            return;
        }
        if (!window.authManager.isAuthenticated()) {
            window.location.href = '/login';
            return;
        }
        const user = window.authManager.getUser();
        if (!user || !user.is_admin) {
            showError('No tienes permisos para acceder a esta página. Solo los administradores pueden gestionar personas.');
            setTimeout(() => {
                window.location.href = '/';
            }, 3000);
            return;
        }
        loadPersonas();
    };
    checkAuth();
    // Filtrado de personas
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const filteredPersonas = personas.filter(persona =>
                persona.nombre.toLowerCase().includes(searchTerm) ||
                (persona.apellido || '').toLowerCase().includes(searchTerm) ||
                persona.email.toLowerCase().includes(searchTerm)
            );
            renderFilteredPersonas(filteredPersonas);
        });
    }
});

/**
 * Cargar personas desde la API
 */
async function loadPersonas() {
    try {
        const response = await axios.get('/api/v1/personas');
        personas = response.data;
        renderPersonasTable();
    } catch (error) {
        showError('Error al cargar las personas: ' + (error.response?.data?.detail || error.message));
    }
}

/**
 * Renderizar tabla de personas
 */
function renderPersonasTable() {
    const tbody = document.querySelector('#personasTable tbody');
    if (!tbody) return;
    if (personas.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay personas registradas</td></tr>';
        return;
    }
    tbody.innerHTML = personas.map(persona => `
        <tr>
            <td>${persona.id}</td>
            <td>${persona.nombre}</td>
            <td>${persona.apellido || ''}</td>
            <td>${persona.email}</td>
            <td><span class="badge bg-${persona.is_admin ? 'danger' : 'primary'}">${persona.is_admin ? 'Administrador' : 'Usuario'}</span></td>
            <td class="admin-only table-actions">
                <div class="d-flex gap-2 btn-equal-group">
                    <button class="btn btn-sm btn-outline-primary btn-3d flex-fill" onclick="editPersona(${persona.id})" aria-label="Editar" title="Editar">
                        <i class="fas fa-edit" aria-hidden="true"></i>
                        <span class="visually-hidden">Editar</span>
                    </button>
                    <button class="btn btn-sm btn-outline-danger btn-3d flex-fill" onclick="deletePersona(${persona.id})" aria-label="Eliminar" title="Eliminar">
                        <i class="fas fa-trash" aria-hidden="true"></i>
                        <span class="visually-hidden">Eliminar</span>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function renderFilteredPersonas(filteredPersonas) {
    const tbody = document.querySelector('#personasTable tbody');
    if (!tbody) return;
    if (filteredPersonas.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No se encontraron personas</td></tr>';
        return;
    }
    tbody.innerHTML = filteredPersonas.map(persona => `
        <tr>
            <td>${persona.id}</td>
            <td>${persona.nombre}</td>
            <td>${persona.apellido || ''}</td>
            <td>${persona.email}</td>
            <td><span class="badge bg-${persona.is_admin ? 'danger' : 'primary'}">${persona.is_admin ? 'Administrador' : 'Usuario'}</span></td>
            <td class="admin-only table-actions">
                <div class="d-flex gap-2 btn-equal-group">
                    <button class="btn btn-sm btn-outline-primary btn-3d flex-fill" onclick="editPersona(${persona.id})" aria-label="Editar" title="Editar">
                        <i class="fas fa-edit" aria-hidden="true"></i>
                        <span class="visually-hidden">Editar</span>
                    </button>
                    <button class="btn btn-sm btn-outline-danger btn-3d flex-fill" onclick="deletePersona(${persona.id})" aria-label="Eliminar" title="Eliminar">
                        <i class="fas fa-trash" aria-hidden="true"></i>
                        <span class="visually-hidden">Eliminar</span>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

/**
 * Abrir modal para nueva persona
 */
function newPersona() {
    currentPersonaId = null;
    document.getElementById('modalTitle').textContent = 'Nueva Persona';
    document.getElementById('personaForm').reset();
    clearValidation();
    document.getElementById('passwordHelp').style.display = 'none';
    const modal = new bootstrap.Modal(document.getElementById('personaModal'));
    modal.show();
}

/**
 * Editar persona existente
 */
async function editPersona(id) {
    try {
        const response = await axios.get(`/api/v1/personas/${id}`);
        const persona = response.data;
        currentPersonaId = id;
        document.getElementById('modalTitle').textContent = 'Editar Persona';
        document.getElementById('nombre').value = persona.nombre;
        document.getElementById('apellido').value = persona.apellido || '';
        document.getElementById('email').value = persona.email;
        document.getElementById('is_admin').checked = persona.is_admin;
        document.getElementById('password').value = '';
        document.getElementById('passwordHelp').style.display = 'block';
        clearValidation();
        const modal = new bootstrap.Modal(document.getElementById('personaModal'));
        modal.show();
    } catch (error) {
        showError('Error al cargar los datos de la persona');
    }
}

/**
 * Guardar persona (crear o actualizar)
 */
async function savePersona() {
    const nombre = document.getElementById('nombre').value.trim();
    const apellido = document.getElementById('apellido').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const is_admin = document.getElementById('is_admin').checked;
    if (!validateForm(nombre, apellido, email, password)) {
        return;
    }
    try {
        const personaData = { nombre, apellido, email, is_admin };
        if (password) {
            personaData.password = password;
        }
        let response;
        if (currentPersonaId) {
            response = await axios.put(`/api/v1/personas/${currentPersonaId}`, personaData);
            showSuccess('Persona actualizada exitosamente');
        } else {
            if (!password) {
                setFieldError('password', 'La contraseña es requerida para nuevas personas');
                return;
            }
            response = await axios.post('/api/v1/personas', personaData);
            showSuccess('Persona creada exitosamente');
        }
        const modal = bootstrap.Modal.getInstance(document.getElementById('personaModal'));
        modal.hide();
        await loadPersonas();
    } catch (error) {
        if (error.response?.data?.detail) {
            if (typeof error.response.data.detail === 'string') {
                showError(error.response.data.detail);
            } else {
                const details = error.response.data.detail;
                if (Array.isArray(details)) {
                    details.forEach(detail => {
                        if (detail.loc && detail.loc.includes('email')) {
                            setFieldError('email', detail.msg);
                        }
                    });
                }
            }
        } else {
            showError('Error al guardar la persona');
        }
    }
}

/**
 * Confirmar eliminación de persona
 */
function deletePersona(id) {
    currentPersonaId = id;
    const persona = personas.find(p => p.id === id);
    document.getElementById('deletePersonaName').textContent = persona ? persona.nombre : 'esta persona';
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}

/**
 * Ejecutar eliminación de persona
 */
async function confirmDelete() {
    try {
        await axios.delete(`/api/v1/personas/${currentPersonaId}`);
        showSuccess('Persona eliminada exitosamente');
        const modal = bootstrap.Modal.getInstance(document.getElementById('deleteModal'));
        modal.hide();
        await loadPersonas();
    } catch (error) {
        showError('Error al eliminar la persona: ' + (error.response?.data?.detail || error.message));
    }
}

/**
 * Validar formulario de persona
 */
function validateForm(nombre, apellido, email, password) {
    clearValidation();
    let isValid = true;
    if (!nombre) {
        setFieldError('nombre', 'El nombre es requerido');
        isValid = false;
    } else if (nombre.length < 2) {
        setFieldError('nombre', 'El nombre debe tener al menos 2 caracteres');
        isValid = false;
    }
    if (!apellido) {
        setFieldError('apellido', 'El apellido es requerido');
        isValid = false;
    } else if (apellido.length < 2) {
        setFieldError('apellido', 'El apellido debe tener al menos 2 caracteres');
        isValid = false;
    }
    if (!email) {
        setFieldError('email', 'El email es requerido');
        isValid = false;
    } else if (!isValidEmail(email)) {
        setFieldError('email', 'El formato del email no es válido');
        isValid = false;
    }
    if (!currentPersonaId && !password) {
        setFieldError('password', 'La contraseña es requerida');
        isValid = false;
    } else if (password && password.length < 6) {
        setFieldError('password', 'La contraseña debe tener al menos 6 caracteres');
        isValid = false;
    }
    return isValid;
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function setFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    field.classList.add('is-invalid');
    const feedback = field.parentNode.querySelector('.invalid-feedback') || field.parentNode.querySelector('.text-danger');
    if (feedback) feedback.textContent = message;
}

function clearValidation() {
    document.querySelectorAll('.is-invalid').forEach(field => {
        field.classList.remove('is-invalid');
    });
    document.querySelectorAll('.invalid-feedback, .text-danger').forEach(feedback => {
        feedback.textContent = '';
    });
}

// Debug de estado de autenticación
function debugAuthState() {
    console.log('=== DEBUG AUTH STATE ===');
    console.log('AuthManager disponible:', !!window.authManager);
    if (window.authManager) {
        const token = window.authManager.getToken();
        const user = window.authManager.getUser();
        const isAuth = window.authManager.isAuthenticated();
        console.log('Token presente:', !!token);
        console.log('Token length:', token ? token.length : 0);
        console.log('Token (primeros 50 chars):', token ? token.substring(0, 50) + '...' : 'null');
        console.log('User object presente:', !!user);
        console.log('User data:', user);
        console.log('isAuthenticated():', isAuth);
        console.log('localStorage token:', !!localStorage.getItem('token'));
        console.log('localStorage user:', !!localStorage.getItem('user'));
    }
}