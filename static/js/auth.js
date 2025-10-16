class AuthManager {
    constructor() {
        // Intentar obtener token de localStorage primero, luego de cookies
        this.token = localStorage.getItem('token') || this.getCookie('token');
        this.user = null;
        if (localStorage.getItem('user')) {
            try {
                this.user = JSON.parse(localStorage.getItem('user'));
            } catch (e) {
                console.error('Error parsing user data:', e);
                localStorage.removeItem('user');
            }
        }
        
        this.setupAxiosInterceptors();
        this.init();
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
        console.log('Inicializando página de login...');
        
        // Si ya está autenticado, verificar que el token sea válido antes de redirigir
        if (this.isAuthenticated()) {
            console.log('Usuario ya autenticado, verificando token...');
            this.getCurrentUser()
                .then(() => {
                    console.log('Token válido, redirigiendo a dashboard...');
                    window.location.href = '/';
                })
                .catch((error) => {
                    console.log('Token inválido, limpiando y permaneciendo en login:', error);
                    this.logout();
                    // No redirigir, quedarse en login
                });
            return;
        }
        
        console.log('Usuario no autenticado, configurando formulario de login...');
        const loginForm = document.getElementById('loginForm');
        const togglePassword = document.querySelector('.toggle-password');
        
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }
        
        if (togglePassword) {
            togglePassword.addEventListener('click', () => this.togglePasswordVisibility());
        }
    }
    
    checkAuthStatus() {
        console.log('Verificando estado de autenticación...');
        
        if (!this.isAuthenticated()) {
            console.log('Usuario no autenticado, redirigiendo a login...');
            // Evitar loop infinito - solo redirigir si no estamos ya en login
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        } else {
            console.log('Usuario autenticado, verificando token...');
            // Verificar que el token siga siendo válido
            this.getCurrentUser().catch((error) => {
                console.log('Token inválido o expirado:', error);
                this.logout();
                if (window.location.pathname !== '/login') {
                    window.location.href = '/login';
                }
            });
        }
    }
    
    async handleLogin(event) {
        event.preventDefault();
        
        const form = event.target;
        const email = form.email.value;
        const password = form.password.value;
        const submitButton = form.querySelector('button[type="submit"]');
        const alertElement = document.getElementById('alert');
        
        this.hideAlert(alertElement);
        this.setLoading(submitButton, true);
        
        try {
            const response = await axios.post('/api/v1/personas/web-login', {
                email: email,
                password: password
            });
            
            const { access_token, user } = response.data;
            
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
        
        this.updateUI();
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
}

// Crear instancia global
window.authManager = new AuthManager();