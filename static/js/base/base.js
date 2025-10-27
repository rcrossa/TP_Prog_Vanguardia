document.addEventListener('DOMContentLoaded', function() {
    // Esperar a que AuthManager esté inicializado
    setTimeout(() => {
        updateMenuVisibility();
    }, 100);
});

// Control de menú basado en permisos
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        updateMenuVisibility();
    }, 100);
});

function updateMenuVisibility() {
    // No necesitamos manipular elementos individuales aquí
    // Actualizar el dropdown del usuario para mostrar el rol
    const user = window.authManager?.getUser();
    if (user) {
        updateUserDropdown(user);
    }
}

function updateUserDropdown(user) {
    const userDropdown = document.getElementById('navbarDropdown');
    if (userDropdown) {
        const roleText = user.is_admin ? ' (Admin)' : ' (Usuario)';
        userDropdown.innerHTML = `<i class="fas fa-user me-1"></i>${user.nombre}${roleText}`;
    }
}

function checkAdminAccess() {
    console.log('=== VERIFICANDO ACCESO ADMIN ===');
    if (!window.authManager) {
        console.warn('AuthManager no disponible, redirigiendo a login');
        window.location.href = '/login';
        return false;
    }
    console.log('Token disponible:', !!window.authManager.getToken());
    console.log('Token:', window.authManager.getToken()?.substring(0, 30) + '...');
    if (!window.authManager.isAuthenticated()) {
        console.warn('Usuario no autenticado, redirigiendo a login');
        window.location.href = '/login';
        return false;
    }
    const user = window.authManager.getUser();
    console.log('Usuario completo:', user);
    if (!user) {
        console.warn('Datos de usuario no disponibles, redirigiendo a login');
        window.location.href = '/login';
        return false;
    }
    console.log('Es admin:', user.is_admin);
    if (!user.is_admin) {
        console.warn('Usuario no tiene permisos de admin');
        alert('Acceso denegado. Solo los administradores pueden acceder a esta sección.');
        window.location.href = '/';
        return false;
    }
    console.log('✅ Acceso admin confirmado');
    return true;
}

function debugAuthState() {
    console.log('=== DEBUG AUTH STATE ===');
    console.log('AuthManager disponible:', !!window.authManager);
    console.log('Token localStorage:', localStorage.getItem('token')?.substring(0, 30) + '...');
    console.log('User localStorage:', localStorage.getItem('user'));
    console.log('Authenticated:', window.authManager?.isAuthenticated());
    console.log('User object:', window.authManager?.getUser());
    console.log('Current URL:', window.location.href);
    console.log('========================');
}

function logout() {
    console.log('Cerrando sesión...');
    if (window.authManager) {
        window.authManager.logout();
        console.log('Sesión cerrada, redirigiendo a login...');
        window.location.href = '/login';
    } else {
        console.error('AuthManager no disponible');
        // Limpiar manualmente y redirigir
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = '/login';
    }
}
