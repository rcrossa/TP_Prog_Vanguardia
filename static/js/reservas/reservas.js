// JS para reservas.html
// 🔒 SEGURIDAD PRE-RENDER: Aplicar clase admin INMEDIATAMENTE antes de que la página renderice
(function() {
    try {
        const userStr = localStorage.getItem('user');
        
        if (userStr && userStr !== 'undefined' && userStr !== 'null') {
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

let reservas = [];
let salas = [];
let articulos = [];
let personas = [];
let reservaModal;
let articulosModal;
let currentReservaId = null;
let articulosAsignadosActuales = []; // Para saber qué artículos ya están asignados
let articuloToDelete = null; // Para almacenar el artículo a eliminar

// Función para esperar a que auth esté disponible
function waitForAuth(callback, maxAttempts = 100) {
    let attempts = 0;
    const checkAuth = () => {
        attempts++;
        if (window.auth && window.authManager) {
            callback();
        } else if (attempts < maxAttempts) {
            setTimeout(checkAuth, 50);
        } else {
            // Timeout - redirigir al login
            window.location.href = '/login';
        }
    };
    checkAuth();
}

document.addEventListener('DOMContentLoaded', function() {
    // Esperar a que el sistema de autenticación esté listo
    waitForAuth(() => {
        // 🔒 SEGURIDAD: Verificar rol de usuario inmediatamente
        const currentUser = window.authManager ? window.authManager.getUser() : null;
        if (currentUser) {
            if (currentUser.is_admin === true) {
                document.body.classList.add('is-admin');
            } else {
                document.body.classList.remove('is-admin');
                // Forzar ocultamiento de elementos admin
                document.querySelectorAll('.admin-only').forEach(el => {
                    el.style.display = 'none';
                });
            }
        } else {
            // Sin usuario autenticado, ocultar todo contenido admin
            document.body.classList.remove('is-admin');
            document.querySelectorAll('.admin-only').forEach(el => {
                el.style.display = 'none';
            });
        }
        
        reservaModal = new bootstrap.Modal(document.getElementById('reservaModal'));
        articulosModal = new bootstrap.Modal(document.getElementById('articulosModal'));
        
        // Cargar datos iniciales
        loadReservas();
        loadSalas();
        loadArticulos();
        loadPersonas();
        
        // Event listeners
        document.getElementById('newReservaBtn').addEventListener('click', () => openModal());
        document.getElementById('searchInput').addEventListener('input', filterReservas);
        document.getElementById('filterTipo').addEventListener('change', filterReservas);
        document.getElementById('filterEstado').addEventListener('change', filterReservas);
        document.getElementById('tipoReserva').addEventListener('change', toggleTipoReserva);
    });
});

// Cargar reservas
async function loadReservas() {
    try {
        const response = await axios.get('/api/v1/reservas/');
        reservas = response.data;
        // Salvaguarda: si el usuario NO es admin, filtrar solo sus reservas en cliente
        try {
            const user = window.authManager ? window.authManager.getUser() : null;
            if (user && user.is_admin === false) {
                reservas = reservas.filter(r => r.id_persona === user.id);
            }
        } catch (_) { /* noop */ }
        renderReservas(reservas);
    } catch (error) {
        console.error('Error cargando reservas:', error);
        showError('Error al cargar las reservas');
    }
}

// Cargar salas
async function loadSalas() {
    try {
        const response = await axios.get('/api/v1/salas/');
        salas = response.data;
        updateSalaSelect();
    } catch (error) {
        console.error('Error cargando salas:', error);
    }
}

// Cargar artículos
async function loadArticulos() {
    try {
        const response = await axios.get('/api/v1/articulos/');
        articulos = response.data;
        updateArticuloSelect();
    } catch (error) {
        console.error('Error cargando artículos:', error);
    }
}

// Cargar personas
async function loadPersonas() {
    try {
        const response = await axios.get('/api/v1/personas/');
        personas = response.data;
        updatePersonaSelect();
    } catch (error) {
        console.error('Error cargando personas:', error);
        
        // Si el error es 403 (no es admin), usar solo el usuario actual
        if (error.response?.status === 403) {
            // Verificar que window.auth existe
            if (!window.auth || !window.authManager) {
                personas = [];
                updatePersonaSelect();
                return;
            }
            
            let currentUser = window.auth.getUser();
            
            // Si no hay usuario en localStorage, consultar al servidor
            if (!currentUser || !currentUser.id) {
                try {
                    const meResponse = await axios.get('/api/v1/personas/me');
                    currentUser = meResponse.data;
                    
                    // Guardar en localStorage para próximas consultas
                    window.auth.setUser(currentUser);
                } catch (meError) {
                    console.error('Error al obtener usuario del servidor:', meError);
                    alert('No se pudo obtener tu información de usuario. Por favor, inicia sesión nuevamente.');
                    window.location.href = '/login';
                    return;
                }
            }
            
            if (currentUser && currentUser.id) {
                personas = [{
                    id: currentUser.id,
                    nombre: currentUser.nombre,
                    email: currentUser.email
                }];
                updatePersonaSelect();
            } else {
                personas = [];
            }
        } else if (error.response?.status === 401) {
            alert('⚠️ Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
            window.location.href = '/login';
        }
    }
}

// Actualizar select de salas
function updateSalaSelect() {
    const select = document.getElementById('idSala');
    select.innerHTML = '<option value="">Seleccione una sala...</option>';
    salas.forEach(sala => {
        select.innerHTML += `<option value="${sala.id}">${sala.nombre} (Cap: ${sala.capacidad})</option>`;
    });
}

// Actualizar select de artículos
function updateArticuloSelect() {
    const select = document.getElementById('idArticulo');
    select.innerHTML = '<option value="">Seleccione un artículo...</option>';
    articulos.filter(a => a.disponible).forEach(articulo => {
        select.innerHTML += `<option value="${articulo.id}">${articulo.nombre}</option>`;
    });
}

// Actualizar select de personas
function updatePersonaSelect() {
    const select = document.getElementById('idPersona');
    if (!select) {
        return;
    }
    
    select.innerHTML = '<option value="">Seleccione una persona...</option>';
    
    if (personas.length === 0) {
        select.innerHTML += '<option value="" disabled>No hay personas disponibles</option>';
        return;
    }
    
    personas.forEach(persona => {
        select.innerHTML += `<option value="${persona.id}">${persona.nombre}</option>`;
    });
}

// Toggle tipo de reserva
function toggleTipoReserva() {
    const tipo = document.getElementById('tipoReserva').value;
    const salaGroup = document.getElementById('salaGroup');
    const articuloGroup = document.getElementById('articuloGroup');
    const idSala = document.getElementById('idSala');
    const idArticulo = document.getElementById('idArticulo');
    
    if (tipo === 'sala') {
        salaGroup.style.display = 'block';
        articuloGroup.style.display = 'none';
        idSala.required = true;
        idArticulo.required = false;
        idArticulo.value = '';
    } else if (tipo === 'articulo') {
        salaGroup.style.display = 'none';
        articuloGroup.style.display = 'block';
        idSala.required = false;
        idArticulo.required = true;
        idSala.value = '';
    } else {
        salaGroup.style.display = 'none';
        articuloGroup.style.display = 'none';
        idSala.required = false;
        idArticulo.required = false;
    }
}

// Renderizar reservas
function renderReservas(data) {
    const tbody = document.getElementById('reservasTableBody');
    
    if (data.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center py-4">
                    <i class="fas fa-calendar-times fa-2x text-muted mb-2"></i>
                    <p class="mb-0 text-muted">No se encontraron reservas</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = data.map(reserva => {
        const esSala = reserva.id_sala !== null && reserva.id_sala !== undefined;
        const tipo = esSala ? 'Sala' : 'Artículo';
        const recurso = getNombreRecurso(reserva);
        const persona = getNombrePersona(reserva.id_persona);
        const estado = getEstadoReserva(reserva);
        const estadoBadge = getEstadoBadge(estado);
        // Botones con estilos unificados y accesibilidad
        let btn1, btn2, btn3;
        if (esSala) {
            btn1 = `<button class="btn btn-sm btn-outline-info btn-3d flex-fill w-100 py-2" onclick="gestionarArticulos(${reserva.id})" aria-label="Gestionar Artículos" title="Gestionar Artículos">
                        <i class="fas fa-boxes" aria-hidden="true"></i>
                        <span class="visually-hidden">Gestionar Artículos</span>
                    </button>`;
        } else {
            btn1 = `<button class="btn btn-sm btn-outline-info btn-3d flex-fill w-100 py-2" disabled style="opacity:0;pointer-events:none;">
                        <i class="fas fa-boxes" aria-hidden="true"></i>
                        <span class="visually-hidden">Gestionar Artículos</span>
                    </button>`;
        }
        if (estado === 'futuro') {
            btn2 = `<button class="btn btn-sm btn-outline-primary btn-3d flex-fill w-100 py-2" onclick="editReserva(${reserva.id})" aria-label="Editar" title="Editar">
                        <i class="fas fa-edit" aria-hidden="true"></i>
                        <span class="visually-hidden">Editar</span>
                    </button>`;
        } else {
            btn2 = `<button class="btn btn-sm btn-outline-secondary btn-3d flex-fill w-100 py-2" onclick="viewReserva(${reserva.id})" aria-label="Ver detalles" title="Ver detalles">
                        <i class="fas fa-eye" aria-hidden="true"></i>
                        <span class="visually-hidden">Ver detalles</span>
                    </button>`;
        }
        btn3 = `<button class="btn btn-sm btn-outline-danger btn-3d flex-fill w-100 py-2" onclick="deleteReserva(${reserva.id})" aria-label="Eliminar" title="Eliminar">
                    <i class="fas fa-trash" aria-hidden="true"></i>
                    <span class="visually-hidden">Eliminar</span>
                </button>`;
        return `
            <tr>
                <td><span class="badge bg-secondary">#${reserva.id}</span></td>
                <td><i class="fas fa-${esSala ? 'door-open' : 'box'} me-1"></i>${tipo}</td>
                <td>${recurso}</td>
                <td>${persona}</td>
                <td>${formatDateTime(reserva.fecha_hora_inicio)}</td>
                <td>${formatDateTime(reserva.fecha_hora_fin)}</td>
                <td>${estadoBadge}</td>
                <td>
                    <div class="d-flex gap-2 btn-equal-group">
                        ${btn1}
                        ${btn2}
                        ${btn3}
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// Obtener nombre del recurso
function getNombreRecurso(reserva) {
    if (reserva.id_sala !== null && reserva.id_sala !== undefined) {
        const sala = salas.find(s => s.id === reserva.id_sala);
        return sala ? sala.nombre : `Sala #${reserva.id_sala}`;
    } else if (reserva.id_articulo !== null && reserva.id_articulo !== undefined) {
        const articulo = articulos.find(a => a.id === reserva.id_articulo);
        return articulo ? articulo.nombre : `Artículo #${reserva.id_articulo}`;
    }
    return 'N/A';
}

// Obtener nombre de persona
function getNombrePersona(idPersona) {
    const persona = personas.find(p => p.id === idPersona);
    return persona ? persona.nombre : `Persona #${idPersona}`;
}

// Obtener estado de reserva
function getEstadoReserva(reserva) {
    const ahora = new Date();
    const inicio = new Date(reserva.fecha_hora_inicio);
    const fin = new Date(reserva.fecha_hora_fin);
    
    if (ahora < inicio) return 'futuro';
    if (ahora > fin) return 'pasado';
    return 'activo';
}

// Obtener badge de estado
function getEstadoBadge(estado) {
    const badges = {
        'futuro': '<span class="badge bg-info">Futura</span>',
        'activo': '<span class="badge bg-success">Activa</span>',
        'pasado': '<span class="badge bg-secondary">Pasada</span>'
    };
    return badges[estado] || '';
}

// Formatear fecha/hora
function formatDateTime(dateString) {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}

// Filtrar reservas
function filterReservas() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const tipoFilter = document.getElementById('filterTipo').value;
    const estadoFilter = document.getElementById('filterEstado').value;
    
    let filtered = reservas.filter(reserva => {
        const recurso = getNombreRecurso(reserva).toLowerCase();
        const persona = getNombrePersona(reserva.id_persona).toLowerCase();
        const matchSearch = recurso.includes(searchTerm) || persona.includes(searchTerm);
        
        const tipo = (reserva.id_sala !== null && reserva.id_sala !== undefined) ? 'sala' : 'articulo';
        const matchTipo = !tipoFilter || tipo === tipoFilter;
        
        const estado = getEstadoReserva(reserva);
        const matchEstado = !estadoFilter || estado === estadoFilter;
        
        return matchSearch && matchTipo && matchEstado;
    });
    
    renderReservas(filtered);
}

// Abrir modal
function openModal(reserva = null) {
    document.getElementById('reservaForm').reset();
    document.getElementById('reservaId').value = '';
    document.getElementById('modalTitle').textContent = 'Nueva Reserva';
    toggleTipoReserva();
    reservaModal.show();
}

// Ver detalles de reserva
function viewReserva(id) {
    const reserva = reservas.find(r => r.id === id);
    if (!reserva) return;
    
        // Crear contenido para el modal
        const modalHtml = `
            <div class="modal fade" id="detalleReservaModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Detalles de Reserva #${id}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <ul class="list-group mb-3">
                                <li class="list-group-item"><strong>Tipo:</strong> ${reserva.id_sala ? 'Sala' : 'Artículo'}</li>
                                <li class="list-group-item"><strong>Recurso:</strong> ${getNombreRecurso(reserva)}</li>
                                <li class="list-group-item"><strong>Persona:</strong> ${getNombrePersona(reserva.id_persona)}</li>
                                <li class="list-group-item"><strong>Inicio:</strong> ${formatDateTime(reserva.fecha_hora_inicio)}</li>
                                <li class="list-group-item"><strong>Fin:</strong> ${formatDateTime(reserva.fecha_hora_fin)}</li>
                                <li class="list-group-item"><strong>Estado:</strong> ${getEstadoReserva(reserva)}</li>
                            </ul>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                        </div>
                    </div>
                </div>
            </div>`;
        // Eliminar modal anterior si existe
        const oldModal = document.getElementById('detalleReservaModal');
        if (oldModal) oldModal.remove();
        // Insertar modal en el body
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        // Mostrar modal
        const modalInstance = new bootstrap.Modal(document.getElementById('detalleReservaModal'));
        modalInstance.show();
}

// Editar reserva
function editReserva(id) {
    const reserva = reservas.find(r => r.id === id);
    if (!reserva) return;
    
    // Verificar que es una reserva futura
    const estado = getEstadoReserva(reserva);
    if (estado !== 'futuro') {
        showError('Solo se pueden editar reservas futuras');
        return;
    }
    
    // Cargar datos en el formulario
    document.getElementById('reservaId').value = reserva.id;
    document.getElementById('idPersona').value = reserva.id_persona;
    
    // Convertir fechas a formato ISO para el input datetime-local
    const fechaInicio = new Date(reserva.fecha_hora_inicio);
    const fechaFin = new Date(reserva.fecha_hora_fin);
    
    document.getElementById('fechaInicio').value = fechaInicio.toISOString().slice(0, 16);
    document.getElementById('fechaFin').value = fechaFin.toISOString().slice(0, 16);
    
    // Configurar tipo de reserva
    if (reserva.id_sala) {
        document.getElementById('tipoReserva').value = 'sala';
        toggleTipoReserva();
        document.getElementById('idSala').value = reserva.id_sala;
    } else {
        document.getElementById('tipoReserva').value = 'articulo';
        toggleTipoReserva();
        document.getElementById('idArticulo').value = reserva.id_articulo;
    }
    
    document.getElementById('modalTitle').textContent = `Editar Reserva #${id}`;
    reservaModal.show();
}

// Guardar reserva
async function saveReserva() {
    const form = document.getElementById('reservaForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const reservaId = document.getElementById('reservaId').value;
    const tipo = document.getElementById('tipoReserva').value;
    
    // Obtener las fechas del formulario
    let fechaInicio = document.getElementById('fechaInicio').value;
    let fechaFin = document.getElementById('fechaFin').value;
    
    // Convertir a formato ISO con segundos si no los tiene
    // El input datetime-local devuelve: "2025-10-17T14:30"
    // Necesitamos: "2025-10-17T14:30:00"
    if (fechaInicio && fechaInicio.length === 16) {
        fechaInicio += ':00';
    }
    if (fechaFin && fechaFin.length === 16) {
        fechaFin += ':00';
    }
    
    const data = {
        id_persona: parseInt(document.getElementById('idPersona').value),
        fecha_hora_inicio: fechaInicio,
        fecha_hora_fin: fechaFin,
        id_sala: tipo === 'sala' ? parseInt(document.getElementById('idSala').value) : null,
        id_articulo: tipo === 'articulo' ? parseInt(document.getElementById('idArticulo').value) : null
    };
    
    try {
        if (reservaId) {
            // Actualizar reserva existente
            await axios.put(`/api/v1/reservas/${reservaId}`, data);
        } else {
            // Crear nueva reserva
            await axios.post('/api/v1/reservas/', data);
        }
        
        // Si llegamos aquí, la operación fue exitosa
        // Cerrar el modal INMEDIATAMENTE para evitar problemas
        reservaModal.hide();
        
        // Mostrar mensaje de éxito y recargar (con manejo de errores)
        try {
            const message = reservaId ? 'Reserva actualizada exitosamente' : 'Reserva creada exitosamente';
            showSuccess(message);
            await loadReservas();
        } catch (postOperationError) {
            console.warn('Error post-operación (no afecta el guardado):', postOperationError);
            // No lanzar el error para que no interfiera con el cierre del modal
        }
    } catch (error) {
        console.error('Error guardando reserva:', error);
        
        // Mostrar mensaje de error más detallado
        let errorMsg = 'Error al guardar la reserva';
        if (error.response?.data?.detail) {
            if (Array.isArray(error.response.data.detail)) {
                // Errores de validación de Pydantic
                errorMsg = error.response.data.detail.map(err => {
                    const location = err.loc ? err.loc.join('.') : 'unknown';
                    const message = err.msg || err.message || 'Error desconocido';
                    const inputValue = err.input !== undefined ? ` (valor: ${err.input})` : '';
                    return `• ${location}: ${message}${inputValue}`;
                }).join('\n');
            } else {
                errorMsg = error.response.data.detail;
            }
        }
        showError(errorMsg);
    }
}

// Eliminar reserva
async function deleteReserva(id) {
    if (!confirm('¿Está seguro de eliminar esta reserva?')) return;
    
    try {
        await axios.delete(`/api/v1/reservas/${id}`);
        loadReservas();
        showSuccess('Reserva eliminada exitosamente');
    } catch (error) {
        console.error('Error eliminando reserva:', error);
        showError('Error al eliminar la reserva');
    }
}

// Mostrar mensajes con Toast - delegamos al sistema centralizado
function showSuccess(message) {
    // Delegar de forma segura sin recursión
    if (typeof window.showToast === 'function') {
        window.showToast(message, 'success');
    } else {
        showToastLocal(message, 'success');
    }
}

function showError(message) {
    // Normalizar mensaje si es objeto
    if (typeof message === 'object') {
        if (message?.detail) message = message.detail;
        else if (message?.message) message = message.message;
        else message = JSON.stringify(message);
    }
    if (typeof window.showToast === 'function') {
        window.showToast(message, 'danger');
    } else {
        showToastLocal(message, 'danger');
    }
}

// ===== GESTIÓN DE ARTÍCULOS EN RESERVAS =====

// Actualizar información del artículo seleccionado
function actualizarInfoArticulo() {
    const selectArticulo = document.getElementById('articuloSelect');
    const inputCantidad = document.getElementById('articuloCantidad');
    
    // Simplemente resetear la cantidad a 1
    if (!selectArticulo.value) {
        inputCantidad.value = '1';
        return;
    }
    
    inputCantidad.value = '1';
}

// Cargar disponibilidad de artículos en el select
async function cargarDisponibilidadArticulos(reservaId) {
    const reserva = reservas.find(r => r.id === reservaId);
    if (!reserva) {
        showError('No se encontró la reserva');
        return;
    }
    
    const select = document.getElementById('articuloSelect');
    const valorActual = select.value; // Guardar selección actual
    select.innerHTML = '<option value="">Cargando disponibilidad...</option>';
    
    try {
        // Obtener disponibilidad de artículos para el período de la reserva
        // NO pasamos reserva_id para que incluya TODAS las reservas (incluida esta)
        // así sabemos si realmente hay stock disponible
        const response = await axios.get('/api/v1/articulos/disponibilidad', {
            params: {
                fecha_inicio: reserva.fecha_hora_inicio,
                fecha_fin: reserva.fecha_hora_fin,
                // Excluir la reserva actual para calcular correctamente la disponibilidad incremental
                reserva_id: reservaId,
                t: Date.now()
            }
        });
        
    const articulosDisponibilidad = response.data;
        
        
        
        // Actualizar select con disponibilidad real
        select.innerHTML = '<option value="">Seleccione un artículo...</option>';
        
        // Mostrar artículos con su disponibilidad real para AGREGAR en esta reserva
        
        articulosDisponibilidad.forEach(articulo => {
            const dispAgregar = (typeof articulo.cantidad_disponible_para_agregar === 'number')
                ? articulo.cantidad_disponible_para_agregar
                : articulo.cantidad_disponible; // compat
            const option = document.createElement('option');
            option.value = articulo.id;
            option.textContent = `${articulo.nombre} (Agregar: ${dispAgregar} | Total: ${articulo.cantidad_total})`;
            if (dispAgregar <= 0) {
                option.disabled = true;
                option.textContent += ' (sin disponible)';
            }
            select.appendChild(option);
        });
        
        // Mensaje si no hay artículos disponibles
        if (select.options.length === 1) { // Solo tiene la opción "Seleccione..."
            const option = document.createElement('option');
            option.disabled = true;
            option.textContent = 'No hay artículos disponibles para agregar';
            select.appendChild(option);
        }
        
        // Restaurar selección si todavía existe
        if (valorActual && select.querySelector(`option[value="${valorActual}"]`)) {
            select.value = valorActual;
        }
        
    } catch (error) {
        console.error('Error obteniendo disponibilidad:', error);
        // Fallback: mostrar artículos sin cálculo de disponibilidad
        select.innerHTML = '<option value="">Seleccione un artículo...</option>';
        articulos.filter(a => a.disponible).forEach(articulo => {
            select.innerHTML += `<option value="${articulo.id}">${articulo.nombre}</option>`;
        });
    }
}

// Abrir modal de gestión de artículos
async function gestionarArticulos(reservaId) {
    currentReservaId = reservaId;
    document.getElementById('reservaIdArticulos').value = reservaId;
    
    // Cargar disponibilidad inicial
    await cargarDisponibilidadArticulos(reservaId);
    
    // Cargar artículos asignados
    await loadArticulosAsignados(reservaId);
    
    articulosModal.show();
}

// Cargar artículos asignados a una reserva
async function loadArticulosAsignados(reservaId) {
    const container = document.getElementById('articulosAsignados');
    
    try {
    const response = await axios.get(`/api/v1/reservas/${reservaId}/articulos`, { params: { t: Date.now() }});
        articulosAsignadosActuales = response.data; // Guardar para referencia
        
        if (articulosAsignadosActuales.length === 0) {
            container.innerHTML = `
                <div class="text-center text-muted py-3">
                    <i class="fas fa-inbox me-2"></i>
                    No hay artículos asignados a esta reserva
                </div>
            `;
            return;
        }
        
        container.innerHTML = `
            <div class="list-group">
                ${articulosAsignadosActuales.map(art => `
                    <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <i class="fas fa-box text-primary me-2"></i>
                            <strong>${art.nombre}</strong>
                            ${art.descripcion ? `<br><small class="text-muted">${art.descripcion}</small>` : ''}
                        </div>
                        <div class="d-flex align-items-center gap-2">
                            ${art.categoria ? `<span class="badge bg-secondary">${art.categoria}</span>` : ''}
                            <div class="btn-group btn-group-sm" role="group">
                                <button class="btn btn-outline-secondary" onclick="modificarCantidadArticulo(${art.id}, -1)" title="Reducir cantidad" ${art.cantidad <= 1 ? 'disabled' : ''}>
                                    <i class="fas fa-minus"></i>
                                </button>
                                <button class="btn btn-outline-info btn-value-display" disabled>
                                    ${art.cantidad}
                                </button>
                                <button class="btn btn-outline-secondary" onclick="modificarCantidadArticulo(${art.id}, 1)" title="Aumentar cantidad">
                                    <i class="fas fa-plus"></i>
                                </button>
                            </div>
                            <button class="btn btn-sm btn-outline-danger" onclick="eliminarArticuloDeReserva(${art.id})" title="Eliminar completamente">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        // Inicializar el estado del formulario de agregar/actualizar
        actualizarInfoArticulo();
        
    } catch (error) {
        console.error('Error cargando artículos asignados:', error);
        container.innerHTML = `
            <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Error al cargar los artículos asignados
            </div>
        `;
    }
}

// Agregar artículo a la reserva
async function agregarArticuloAReserva() {
    const articuloId = document.getElementById('articuloSelect').value;
    const cantidad = parseInt(document.getElementById('articuloCantidad').value);
    
    if (!articuloId) {
        showError('Debe seleccionar un artículo');
        return;
    }
    
    if (!cantidad || cantidad < 1) {
        showError('La cantidad debe ser mayor a 0');
        return;
    }
    
    try {
        await axios.post(`/api/v1/reservas/${currentReservaId}/articulos/${articuloId}?cantidad=${cantidad}`);
        showSuccess('Artículo agregado/actualizado exitosamente');
        
    // Recargar lista de artículos asignados y disponibilidad
    await loadArticulosAsignados(currentReservaId);
    await cargarDisponibilidadArticulos(currentReservaId);
    // Refrescar también la grilla de reservas
    await loadReservas();
        
        // Actualizar el estado del formulario (el select mantiene su valor)
        actualizarInfoArticulo();
    } catch (error) {
        console.error('Error agregando artículo:', error);
        const status = error.response?.status;
        const detail = error.response?.data?.detail || error.message || 'Error al agregar el artículo';
        showError(`${status ? '['+status+'] ' : ''}${detail}`);
    }
}

// Modificar cantidad de un artículo en la reserva
async function modificarCantidadArticulo(articuloId, cambio) {
    try {
        // Encontrar el artículo actual
        const articuloActual = articulosAsignadosActuales.find(a => a.id === articuloId);
        if (!articuloActual) {
            showError('Artículo no encontrado');
            return;
        }
        
        const nuevaCantidad = articuloActual.cantidad + cambio;
        
        if (nuevaCantidad < 1) {
            showError('La cantidad mínima es 1. Use el botón de eliminar para quitar el artículo.');
            return;
        }
        
        // Usar el endpoint POST con modo='reemplazar' para establecer la cantidad exacta
        await axios.post(`/api/v1/reservas/${currentReservaId}/articulos/${articuloId}?cantidad=${nuevaCantidad}&modo=reemplazar`);
        showSuccess(`Cantidad actualizada a ${nuevaCantidad}`);
        
    // Recargar lista y disponibilidad
    await loadArticulosAsignados(currentReservaId);
    await cargarDisponibilidadArticulos(currentReservaId);
    // Refrescar también la grilla de reservas
    await loadReservas();
        
        // Actualizar el estado del formulario
        actualizarInfoArticulo();
    } catch (error) {
        console.error('Error modificando cantidad:', error);
        showError(error.response?.data?.detail || 'Error al modificar la cantidad');
    }
}

// Eliminar artículo de la reserva
async function eliminarArticuloDeReserva(articuloId) {
    // Buscar el nombre del artículo para mostrarlo en el modal
    const articuloAsignado = articulosAsignadosActuales.find(item => item.id === articuloId);
    const nombreArticulo = articuloAsignado ? articuloAsignado.nombre : 'este artículo';
    
    // Almacenar el ID del artículo a eliminar
    articuloToDelete = articuloId;
    
    // Actualizar el nombre en el modal
    document.getElementById('articuloNameToDelete').textContent = nombreArticulo;
    
    // Mostrar el modal de confirmación
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmDeleteArticuloModal'));
    confirmModal.show();
}

// Función para confirmar la eliminación del artículo
async function confirmarEliminarArticulo() {
    if (!articuloToDelete) return;
    
    try {
        // Mostrar loading en el botón
        const deleteBtn = document.querySelector('#confirmDeleteArticuloModal .btn-danger');
        const originalText = deleteBtn.innerHTML;
        deleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Eliminando...';
        deleteBtn.disabled = true;
        
        await axios.delete(`/api/v1/reservas/${currentReservaId}/articulos/${articuloToDelete}`);
        
        // Cerrar el modal
        const confirmModal = bootstrap.Modal.getInstance(document.getElementById('confirmDeleteArticuloModal'));
        confirmModal.hide();
        
        // Mostrar toast de éxito con animación
        showSuccess('🗑️ Artículo eliminado exitosamente de la reserva');
        
    // Recargar lista y disponibilidad
    await loadArticulosAsignados(currentReservaId);
    await cargarDisponibilidadArticulos(currentReservaId);
    // Refrescar también la grilla de reservas
    await loadReservas();
        
        // Actualizar el estado del formulario
        actualizarInfoArticulo();
        
        // Limpiar variable
        articuloToDelete = null;
        
        // Restaurar botón
        deleteBtn.innerHTML = originalText;
        deleteBtn.disabled = false;
        
    } catch (error) {
        console.error('Error eliminando artículo:', error);
        
        // Mostrar toast de error con detalles
        const errorMessage = error.response?.data?.detail || 'Error al eliminar el artículo';
        showError(`❌ ${errorMessage}`);
        
        // Restaurar botón
        const deleteBtn = document.querySelector('#confirmDeleteArticuloModal .btn-danger');
        deleteBtn.innerHTML = '<i class="fas fa-trash me-1"></i>Eliminar Artículo';
        deleteBtn.disabled = false;
    }
}

// Función para mostrar Toast notifications - delegamos al sistema centralizado
function showToastLocal(message, type = 'success') {
    // Usar el sistema centralizado de toast-notifications.js
    if (typeof window.showToast === 'function') { window.showToast(message, type); return; }
    // Fallback básico si no está cargado
    
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed; top: 20px; right: 20px; z-index: 9999;
        background: ${type === 'success' ? '#28a745' : type === 'danger' ? '#dc3545' : '#17a2b8'};
        color: white; padding: 12px 16px; border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => { if (toast.parentNode) toast.parentNode.removeChild(toast); }, 3000);
}