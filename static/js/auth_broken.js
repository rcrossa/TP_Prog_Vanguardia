/**
 * Manejo de autenticación en el frontend
 */

class AuthManager {
    constructor() {
        this.baseURL = '/api/v1/auth';
        this.tokenKey = 'access_token';
        this.userKey = 'user_data';

        // Configurar axios con interceptores
        this.setupAxiosInterceptors();

        // Inicializar según la página
        this.init();
    }

    setupAxiosInterceptors() {
        // Request interceptor
        axios.interceptors.request.use((config) => {
            const token = this.getToken();
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
                console.log('Token agregado a request:', config.url);
            } else {
                console.log('No hay token para request:', config.url);
            }
            return config;
        });

            // Interceptor para responses - manejar errores de auth
            axios.interceptors.response.use(
                (response) => response,
                (error) => {
                    if (error.response?.status === 401) {
                        this.logout();
                        window.location.href = '/login';
                    }
                    return Promise.reject(error);
                }
            );

            // Marcar como configurado
            axios.defaults._authConfigured = true;
        }
    };

    init() {
        const path = window.location.pathname;

        if (path === '/login') {
            this.initLoginPage();
        } else {
            this.checkAuthStatus();
        }
    }

    initLoginPage() {
        // Si ya está logueado, redirigir al dashboard
        if (this.isAuthenticated()) {
            window.location.href = '/';
            return;
        }

        // Configurar formulario de login
        const loginForm = document.getElementById('loginForm');
        const togglePassword = document.getElementById('togglePassword');

        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        if (togglePassword) {
            togglePassword.addEventListener('click', () => this.togglePasswordVisibility());
        }
    }

    checkAuthStatus() {
        if (!this.isAuthenticated()) {
            window.location.href = '/login';
            return;
        }

        // Actualizar UI con datos del usuario
        this.updateUI();
    }

    async handleLogin(event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const loginBtn = document.getElementById('loginBtn');
        const loginAlert = document.getElementById('loginAlert');

        // Deshabilitar botón y mostrar loading
        this.setLoading(loginBtn, true);
        this.hideAlert(loginAlert);

        try {
            const response = await axios.post(`${this.baseURL}/login`, {
                email: formData.get('email'),
                password: formData.get('password')
            });

            const data = response.data;

            // Guardar token y datos del usuario
            this.setToken(data.token.access_token);
            this.setUser(data.user);

            // Mostrar mensaje de éxito
            this.showAlert(loginAlert, 'success', '¡Login exitoso! Redirigiendo...');

            // Redirigir después de un breve delay
            setTimeout(() => {
                window.location.href = '/';
            }, 1000);

        } catch (error) {
            console.error('Error de login:', error);
            let message = 'Error al iniciar sesión. Intenta nuevamente.';

            if (error.response?.data?.detail) {
                message = error.response.data.detail;
            }

            this.showAlert(loginAlert, 'danger', message);
        } finally {
            this.setLoading(loginBtn, false);
        }
    }

    logout() {
        // Limpiar localStorage
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem(this.userKey);

        // Redirigir a login
        window.location.href = '/login';
    }

    updateUI() {
        const user = this.getUser();
        if (!user) return;

        // Actualizar dropdown del usuario en el navbar
        const userDropdown = document.getElementById('navbarDropdown');
        if (userDropdown) {
            userDropdown.innerHTML = `
                <i class="fas fa-user me-1"></i>${user.nombre}
                ${user.is_admin ? '<span class="badge bg-warning ms-1">Admin</span>' : ''}
            `;
        }

        // Configurar botón de logout
        const logoutBtn = document.querySelector('a[href="#"]:has(.fa-sign-out-alt)');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        }
    }

    togglePasswordVisibility() {
        const passwordInput = document.getElementById('password');
        const toggleIcon = document.querySelector('#togglePassword i');

        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleIcon.classList.remove('fa-eye');
            toggleIcon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            toggleIcon.classList.remove('fa-eye-slash');
            toggleIcon.classList.add('fa-eye');
        }
    }

    setLoading(button, loading) {
        const spinner = '<i class="fas fa-spinner fa-spin me-2"></i>';
        const icon = '<i class="fas fa-sign-in-alt me-2"></i>';

        if (loading) {
            button.disabled = true;
            button.innerHTML = `${spinner}Iniciando sesión...`;
        } else {
            button.disabled = false;
            button.innerHTML = `${icon}<span>Iniciar Sesión</span>`;
        }
    }

    showAlert(alertElement, type, message) {
        alertElement.className = `alert alert-${type}`;
        alertElement.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>${message}`;
        alertElement.classList.remove('d-none');
    }

    hideAlert(alertElement) {
        alertElement.classList.add('d-none');
    }

    // Métodos de utilidad para localStorage
    setToken(token) {
        localStorage.setItem(this.tokenKey, token);
    }

    getToken() {
        return localStorage.getItem(this.tokenKey);
    }

    setUser(user) {
        localStorage.setItem(this.userKey, JSON.stringify(user));
    }

    getUser() {
        const userData = localStorage.getItem(this.userKey);
        return userData ? JSON.parse(userData) : null;
    }

    isAuthenticated() {
        return !!this.getToken() && !!this.getUser();
    }

    // API calls
    async getCurrentUser() {
        try {
            const response = await axios.get(`${this.baseURL}/me`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.authManager = new AuthManager();
});

// Función global para logout (por si se necesita desde otros scripts)
function logout() {
    if (window.authManager) {
        window.authManager.logout();
    }
}