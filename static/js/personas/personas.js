// JS para personas.html
// Aquí se migran funciones como newPersona, loadPersonas, etc.

// Inicialización específica de la página de personas
document.addEventListener('DOMContentLoaded', function() {
    // Función para verificar autenticación y permisos
    const checkAuth = () => {
        console.log('🔍 Verificando autenticación para gestión de personas...');
        
        if (!window.authManager) {
            console.error('❌ AuthManager no disponible');
            window.location.href = '/login';
            return;
        }
        
        if (!window.authManager.isAuthenticated()) {
            console.log('❌ Usuario no autenticado, redirigiendo...');
            window.location.href = '/login';
            return;
        }
        
        const user = window.authManager.getUser();
        if (!user || !user.is_admin) {
            console.log('❌ ACCESO DENEGADO - Se requieren permisos de administrador');
            showError('No tienes permisos para acceder a esta página. Solo los administradores pueden gestionar personas.');
            setTimeout(() => {
                window.location.href = '/';
            }, 3000);
            return;
        }
        
        console.log('✅ ACCESO AUTORIZADO - Usuario es administrador');
        
        // Si todo está bien, cargar las personas
        loadPersonas();
    };
    
    // Iniciar verificación
    checkAuth();
});