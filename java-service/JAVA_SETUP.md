# ⚙️ Configuración de Java 21 para el Servicio Java

## 🎯 Problema

Maven puede usar la versión incorrecta de Java (por ejemplo, Java 25 en lugar de Java 21), causando errores de compilación:

```
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.13.0:compile
[ERROR] Fatal error compiling: java.lang.ExceptionInInitializerError: com.sun.tools.javac.code.TypeTag :: UNKNOWN
```

## ✅ Solución: Usar el Wrapper `mvn21`

Hemos creado un script wrapper llamado `mvn21` que **garantiza que siempre se use Java 21**, sin importar qué versión de Java tengas configurada por defecto en tu sistema.

### 📝 Uso del Wrapper

Simplemente reemplaza `mvn` con `./mvn21` en todos tus comandos:

```bash
# En lugar de:
mvn clean install
mvn spring-boot:run

# Usa:
./mvn21 clean install
./mvn21 spring-boot:run
```

### 🔍 Verificar Versión

```bash
# Verificar qué Java usa el wrapper (debería ser 21.x.x)
./mvn21 --version

# Comparar con la versión por defecto (puede ser diferente)
mvn --version
```

**Salida esperada de `./mvn21 --version`:**
```
Apache Maven 3.9.11
Java version: 21.0.8, vendor: Amazon.com Inc.
```

## 🛠️ Instalación de Java 21

Si no tienes Java 21 instalado:

### macOS

**Opción 1: Homebrew**
```bash
brew install --cask corretto21
```

**Opción 2: Descarga manual**
1. Visita: https://aws.amazon.com/corretto/
2. Descarga Amazon Corretto 21 para macOS
3. Instala el archivo `.pkg`

### Linux (Ubuntu/Debian)

```bash
wget -O- https://apt.corretto.aws/corretto.key | sudo apt-key add -
sudo add-apt-repository 'deb https://apt.corretto.aws stable main'
sudo apt-get update
sudo apt-get install -y java-21-amazon-corretto-jdk
```

### Windows

1. Descarga desde: https://aws.amazon.com/corretto/
2. Instala el archivo `.msi`
3. Configura `JAVA_HOME`:
   - Panel de Control → Sistema → Configuración avanzada del sistema
   - Variables de entorno
   - Nueva variable: `JAVA_HOME` = `C:\Program Files\Amazon Corretto\jdk21.x.x`

## 🔧 Configuración Manual de JAVA_HOME (Alternativa)

Si prefieres no usar el wrapper `mvn21`, puedes configurar `JAVA_HOME` manualmente:

### macOS/Linux

**Temporal (solo para la sesión actual):**
```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)  # macOS
export JAVA_HOME=/usr/lib/jvm/java-21-amazon-corretto  # Linux
```

**Permanente (en tu shell):**

Agrega al archivo `~/.zshrc` o `~/.bashrc`:
```bash
# Java 21 para proyectos Maven
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
```

Luego recarga:
```bash
source ~/.zshrc  # o ~/.bashrc
```

### Windows

**CMD:**
```cmd
set JAVA_HOME=C:\Program Files\Amazon Corretto\jdk21.0.8
```

**PowerShell:**
```powershell
$env:JAVA_HOME = "C:\Program Files\Amazon Corretto\jdk21.0.8"
```

## 🏃 Comandos Comunes

```bash
# Compilar el proyecto
./mvn21 clean install

# Ejecutar sin compilar (requiere compilación previa)
./mvn21 spring-boot:run

# Ejecutar tests
./mvn21 test

# Empaquetar sin tests
./mvn21 package -DskipTests

# Limpiar build
./mvn21 clean
```

## 📚 Múltiples Versiones de Java

Si trabajas con proyectos que requieren diferentes versiones de Java:

### macOS

**Listar versiones instaladas:**
```bash
/usr/libexec/java_home -V
```

**Cambiar versión temporalmente:**
```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)  # Java 21
export JAVA_HOME=$(/usr/libexec/java_home -v 17)  # Java 17
export JAVA_HOME=$(/usr/libexec/java_home -v 11)  # Java 11
```

**Crear alias útiles (en ~/.zshrc o ~/.bashrc):**
```bash
alias java21='export JAVA_HOME=$(/usr/libexec/java_home -v 21)'
alias java17='export JAVA_HOME=$(/usr/libexec/java_home -v 17)'
alias java11='export JAVA_HOME=$(/usr/libexec/java_home -v 11)'
```

Uso:
```bash
java21  # Cambia a Java 21
mvn spring-boot:run
```

### Linux

**Usando update-alternatives:**
```bash
# Listar versiones disponibles
sudo update-alternatives --config java

# Selecciona el número correspondiente a Java 21
```

## ❓ Preguntas Frecuentes

**P: ¿Por qué no usar directamente `mvn`?**  
R: Maven usa la versión de Java definida en `JAVA_HOME`. Si tienes Java 25 (o cualquier otra versión) como predeterminada, Maven la usará y causará errores de compilación. El wrapper `mvn21` garantiza Java 21.

**P: ¿Puedo eliminar el archivo `.mavenrc`?**  
R: Sí, no es necesario con el wrapper `mvn21`. Ese archivo era un intento anterior de configuración automática.

**P: ¿Funciona el wrapper en Windows?**  
R: No directamente. En Windows usa `setup_win.bat` que configura automáticamente el entorno.

**P: ¿Qué pasa si ejecuto `mvn` sin el wrapper?**  
R: Usará la versión de Java predeterminada del sistema, que puede no ser Java 21 y causar errores de compilación.

## 📖 Referencias

- **Amazon Corretto 21:** https://aws.amazon.com/corretto/
- **Spring Boot 3.3 Requirements:** https://docs.spring.io/spring-boot/system-requirements.html
- **Maven Toolchains:** https://maven.apache.org/guides/mini/guide-using-toolchains.html

---

**Última actualización:** Noviembre 2025  
**Autor:** Sistema de Reservas - TP Programación de Vanguardia
