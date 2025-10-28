class AuthManager {
    constructor() {
        // Intentar obtener token de localStorage primero, luego de cookies
        this.token = localStorage.getItem('token') || this.getCookie('token');
        
        this.user = null;
        const userStr = localStorage.getItem('user');
        
        if (userStr) {
            try {
                this.user = JSON.parse(userStr);
            } catch (e) {
                console.error('Error parsing user data:', e);
                localStorage.removeItem('user');
            }
        }
        
        // Si hay token pero no hay usuario, obtenerlo del servidor
        if (this.token && !this.user) {
            this.recoverUserFromServer();
        }
        
        this.setupAxiosInterceptors();
        this.init();
    }
    
    async recoverUserFromServer() {
        try {
            const response = await axios.get('/api/v1/personas/me');
            this.setUser(response.data);
        } catch (error) {
            console.error('No se pudo recuperar usuario del servidor:', error);
            
            // Solo hacer logout si es error 401 (no autenticado)
            if (error.response?.status === 401) {
                this.logout();
            }
        }
    }
    
    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
    
    setupAxiosInterceptors() {
        // Solo configurar si no se ha hecho antes
        if (axios.defaults._authConfigured) return;
        
        // Request interceptor
        axios.interceptors.request.use((config) => {
            const token = this.getToken();
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });
            
        // Interceptor para responses - manejar errores de auth
        axios.interceptors.response.use(
            (response) => response,
            (error) => {
                const status = error.response?.status;
                const url = error.config?.url;
                const detail = error.response?.data?.detail;
                
                // Solo hacer logout en errores de autenticación REALES:
                // 1. Error 401 (siempre es problema de token)
                // 2. Error 403 SOLO en endpoints de autenticación (como /me)
                //    pero NO en endpoints protegidos por permisos (como /personas)
                
                if (status === 401) {
                    // 401 = No autenticado, token inválido o expirado
                    this.logout();
                    if (window.location.pathname !== '/login') {
                        alert('⚠️ Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
                        window.location.href = '/login';
                    }
                } else if (status === 403) {
                    // 403 puede ser:
                    // - "Usuario inactivo" = problema de autenticación → logout
                    // - "No tienes permisos de administrador" = problema de permisos → NO logout
                    const isAuthProblem = detail?.includes('inactivo') || 
                                         detail?.includes('inválido') ||
                                         url?.includes('/me');
                    
                    if (isAuthProblem) {
                        this.logout();
                        if (window.location.pathname !== '/login') {
                            alert('⚠️ Tu cuenta está inactiva o tu sesión expiró.');
                            window.location.href = '/login';
                        }
                    }
                }
                return Promise.reject(error);
            }
        );
        
        // Marcar como configurado
        axios.defaults._authConfigured = true;
    }
    
    init() {
        const path = window.location.pathname;
        
        if (path === '/login') {
            this.initLoginPage();
        } else {
            // Para todas las páginas excepto login, verificar auth
            this.checkAuthStatus();
        }
    }
    
    initLoginPage() {
        // Si ya está autenticado, verificar que el token sea válido antes de redirigir
        if (this.isAuthenticated()) {
            this.getCurrentUser()
                .then(() => {
                    window.location.href = '/';
                })
                .catch((error) => {
                    this.logout();
                    // No redirigir, quedarse en login
                });
            return;
        }
        const loginForm = document.getElementById('loginForm');
        const togglePassword = document.querySelector('.toggle-password');
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const alertElement = document.getElementById('alert');

        // Mostrar requerimientos en la vista
        const emailReq = document.getElementById('email-requirements');
        if (emailReq) {
            emailReq.textContent = 'Debe ingresar un email válido (ejemplo: usuario@dominio.com)';
            emailReq.style.display = 'block';
        }
        const passReq = document.getElementById('password-requirements');
        if (passReq) {
            passReq.textContent = 'La contraseña debe tener al menos 6 caracteres.';
            passReq.style.display = 'block';
        }

        // Validación en tiempo real para email
        if (emailInput) {
            emailInput.addEventListener('input', () => {
                const email = emailInput.value.trim();
                const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
                if (!email) {
                    this.showAlert(alertElement, 'warning', 'Por favor, ingresa tu email.');
                } else if (!emailRegex.test(email)) {
                    this.showAlert(alertElement, 'warning', 'El email ingresado no es válido.');
                } else {
                    this.hideAlert(alertElement);
                }
            });
        }
        // Validación en tiempo real para password
        if (passwordInput) {
            passwordInput.addEventListener('input', () => {
                const password = passwordInput.value;
                if (password.length < 6) {
                    this.showAlert(alertElement, 'warning', 'La contraseña debe tener al menos 6 caracteres.');
                } else {
                    this.hideAlert(alertElement);
                }
            });
        }

        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        if (togglePassword) {
            togglePassword.addEventListener('click', () => this.togglePasswordVisibility());
        }
    }
    
    checkAuthStatus() {
        if (!this.isAuthenticated()) {
            // Evitar loop infinito - solo redirigir si no estamos ya en login
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        } else {
            // Verificar que el token siga siendo válido
            this.getCurrentUser().catch((error) => {
                // Solo hacer logout si es error 401 (no autenticado)
                if (error.response?.status === 401) {
                    this.logout();
                    if (window.location.pathname !== '/login') {
                        window.location.href = '/login';
                    }
                }
            });
        }
    }
    
    async handleLogin(event) {
        event.preventDefault();

        const form = event.target;
        const email = form.email.value.trim();
        const password = form.password.value;
        const submitButton = form.querySelector('button[type="submit"]');
        const alertElement = document.getElementById('alert');

        this.hideAlert(alertElement);
        this.setLoading(submitButton, true);

        // Validación: email obligatorio y formato
        if (!email) {
            this.showAlert(alertElement, 'warning', 'Por favor, ingresa tu email.');
            this.setLoading(submitButton, false);
            return;
        }
        // Validar formato básico de email
        const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
        if (!emailRegex.test(email)) {
            this.showAlert(alertElement, 'warning', 'El email ingresado no es válido.');
            this.setLoading(submitButton, false);
            return;
        }

        try {
            const response = await axios.post('/api/v1/personas/web-login', {
                email: email,
                password: password
            });

            const { access_token, user } = response.data;

            if (!user || !user.id) {
                throw new Error('Error de autenticación: datos de usuario incompletos');
            }

            this.setToken(access_token);
            this.setUser(user);

            // Redirigir al dashboard
            window.location.href = '/';

        } catch (error) {
            console.error('Error de login:', error);

            let message = 'Error de conexión';
            if (error.response?.data?.detail) {
                message = error.response.data.detail;
            } else if (error.response?.status === 401) {
                message = 'Email o contraseña incorrectos';
            }

            this.showAlert(alertElement, 'danger', message);
        } finally {
            this.setLoading(submitButton, false);
        }
    }
    
    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        this.token = null;
        this.user = null;
        
        // También eliminar la cookie
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        
        // Limpiar headers de axios
        delete axios.defaults.headers.common['Authorization'];
    }
    
    updateUI() {
        const userInfo = document.querySelector('.user-info');
        const authButtons = document.querySelector('.auth-buttons');
        const loginSection = document.querySelector('.login-section');
        
        if (this.isAuthenticated()) {
            if (userInfo) {
                userInfo.style.display = 'block';
                userInfo.querySelector('.user-name').textContent = this.user.nombre;
                userInfo.querySelector('.user-role').textContent = this.user.is_admin ? 'Administrador' : 'Usuario';
            }
            if (authButtons) authButtons.style.display = 'none';
            if (loginSection) loginSection.style.display = 'none';
        } else {
            if (userInfo) userInfo.style.display = 'none';
            if (authButtons) authButtons.style.display = 'block';
            if (loginSection) loginSection.style.display = 'block';
        }
    }
    
    togglePasswordVisibility() {
        const passwordInput = document.getElementById('password');
        const toggleIcon = document.querySelector('.toggle-password i');
        if (!passwordInput || !toggleIcon) return;

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
        if (loading) {
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Iniciando sesión...';
        } else {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-sign-in-alt me-1"></i>Iniciar Sesión';
        }
    }
    
    showAlert(alertElement, type, message) {
        if (alertElement) {
            alertElement.className = `alert alert-${type}`;
            alertElement.textContent = message;
            alertElement.style.display = 'block';
        }
    }
    
    hideAlert(alertElement) {
        if (alertElement) {
            alertElement.style.display = 'none';
        }
    }
    
    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
        
        // También guardar en cookie para las peticiones web normales
        if (token) {
            // Cookie que expira en 24 horas
            const expirationDate = new Date();
            expirationDate.setTime(expirationDate.getTime() + (24 * 60 * 60 * 1000));
            // No usar secure en desarrollo (localhost)
            const isSecure = window.location.protocol === 'https:';
            const cookieOptions = isSecure ? 'secure; samesite=strict' : 'samesite=lax';
            document.cookie = `token=${token}; expires=${expirationDate.toUTCString()}; path=/; ${cookieOptions}`;
        }
    }
    
    getToken() {
        return this.token;
    }
    
    setUser(user) {
        this.user = user;
        localStorage.setItem('user', JSON.stringify(user));
        
        // Aplicar o remover clase is-admin inmediatamente
        this.applyAdminClass();
    }
    
    getUser() {
        return this.user;
    }
    
    isAuthenticated() {
        return !!(this.token && this.user);
    }
    
    async getCurrentUser() {
        const response = await axios.get('/api/v1/personas/me');
        this.setUser(response.data);
        return response.data;
    }
    
    // Método para aplicar la clase de admin al body inmediatamente
    applyAdminClass() {
        // Verificación ESTRICTA: solo si is_admin es exactamente true
        if (this.user && this.user.is_admin === true) {
            document.body.classList.add('is-admin');
        } else {
            document.body.classList.remove('is-admin');
        }
    }
}

// Crear instancia global
window.authManager = new AuthManager();
window.auth = window.authManager; // Alias para compatibilidad

// Aplicar clase de admin inmediatamente si hay usuario en localStorage
// Esto evita el "flash" de contenido al recargar la página
if (window.authManager.user) {
    // Verificación ESTRICTA: solo agregar clase si is_admin es EXACTAMENTE true
    if (window.authManager.user.is_admin === true) {
        document.body.classList.add('is-admin');
    } else {
        document.body.classList.remove('is-admin');
    }
} else {
    document.body.classList.remove('is-admin');
}