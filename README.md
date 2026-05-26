#  Poke-Clicker

**Autores:** Jesus Daniel Renteria Calzada, Heriberto Yurem Vasquez Cervantes
**Asignatura:** Implementa aplicaciones móviles multiplataforma


### Jesus Daniel Renteria Calzada

![Renteria](imagenes/Renteria.jpeg)

**Número de control:** 23308060610259  
**Correo electrónico:** 23308060610259@cetis61.edu.mx

### Heriberto Yurem Vasquez Cervantes

![Heriberto](imagenes/Heriberto.jpeg)

**Número de control:** 23308060610438  
**Correo electrónico:** 23308060610438@cetis61.edu.mx

**Especialidad:** Programación

**Poke-Clicker** es un proyecto de videojuego tipo **"Idle Clicker"** donde la progresión del jugador se basa en la acumulación de clics y la gestión estratégica de recursos inspirados en el universo Pokémon.

---

##  Descripción del Proyecto

El objetivo principal es acumular clics para avanzar en el juego. La experiencia comienza desde cero: al realizar el primer clic, el sistema interactúa con la **PokéAPI** para otorgar al usuario un Pokémon inicial de forma totalmente aleatoria.

### Mecánicas Principales

* **Sistema de Rebirth (Renacimiento):** Al alcanzar una cantidad considerable de clics, el jugador tiene la opción de "renacer". Esta acción resetea el contador de clics actuales, pero otorga un **Boost de velocidad** (incremento de clics por segundo) durante unos minutos, permitiendo una recuperación acelerada del nivel.
* **Tienda:** Un espacio dedicado para intercambiar puntos de renacimiento por artículos de utilidad:
    * **Caramelos:** Objetos para subir de nivel a los Pokémon y activar sus evoluciones.
    * **Mejoras de Boost:** Adquisición de potenciadores de clics adicionales.
    * **Pokémon Aleatorios:** Posibilidad de probar suerte para obtener nuevas criaturas.
* **Inventario:** Repositorio personal donde se almacenan permanentemente todas las compras, ganancias y Pokémon obtenidos.

---

## 📊 Estructura de la Base de Datos

El diseño lógico de la base de datos está optimizado para gestionar de manera eficiente la información de los usuarios, su progreso dinámico y la integración con datos externos de la PokéAPI.

### Diagrama Entidad-Relación (MER)

![Diagrama MER de Poke-Clicker](imagenes/image.png)

*El diagrama anterior detalla las relaciones entre las entidades de Usuario, Progreso, Tienda, Inventario y Pokémon obtenidos.*

---

##  Implementación Técnica (SQL)

A continuación, se presenta el script necesario para generar la estructura de tablas y las restricciones de integridad (llaves foráneas) que aseguran la consistencia de los datos.

```sql
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE progreso_juego (
    id_progreso INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    clicks_actuales BIGINT DEFAULT 0,
    clicks_totales BIGINT DEFAULT 0,
    cantidad_rebirths INT DEFAULT 0,
    costo_siguiente_rebirth BIGINT DEFAULT 100,
    multiplicador_activo FLOAT DEFAULT 1.0,
    fin_boost DATETIME NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE tienda (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria ENUM('item', 'pokemon', 'boost') NOT NULL,
    costo_rebirths INT NOT NULL,
    valor_efecto FLOAT NOT NULL
);

CREATE TABLE pokemones_obtenidos (
    id_instancia INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    pokemon_api_id INT NOT NULL,
    nombre_personalizado VARCHAR(50),
    nivel INT DEFAULT 1,
    esta_equipado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE inventario_items (
    id_item_inv INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT DEFAULT 1,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES tienda(id_producto) ON DELETE CASCADE
);


---

<<<<<<< HEAD
=======
# 🎮 Poke-Clicker

**Poke-Clicker** es una aplicación móvil multiplataforma que fusiona las mecánicas de los videojuegos de tipo *Idle Clicker* (juegos incrementales) con el universo estratégico de Pokémon. El software implementa una arquitectura modular con una interfaz gráfica reactiva desarrollada en **Flet (v0.82.x)** y persistencia de datos relacional en **MySQL**, garantizando un sistema completamente validado, funcional y libre de errores.

---

## 🚀 Descripción General del Proyecto

### 1. Propósito del Proyecto
El propósito fundamental de este proyecto es ofrecer una experiencia de usuario fluida e interactiva donde la progresión del jugador se divide en dos vertientes:
* **Progresión Activa:** Basada en la interacción directa del usuario mediante clics continuos en la interfaz principal para acumular recursos de forma inmediata.
* **Progresión Pasiva:** Basada en la gestión estratégica y adquisición de mejoras automatizadas que generan recursos de forma constante a lo largo del tiempo (recursos por segundo).

Desde una perspectiva técnica, el proyecto sirve como entorno de desarrollo para implementar patrones arquitectónicos de software, control de accesos seguro, persistencia de datos en tiempo real y operaciones CRUD síncronas.

### 2. Alcance del Proyecto
El alcance del sistema abarca el diseño del ciclo de juego completo (*Core Gameplay Loop*) y la infraestructura técnica de gestión de usuarios:
* **Sistema de Clics y Recursos:** Registro exacto de las interacciones del usuario y cálculo de las ganancias obtenidas.
* **Tienda de Mejoras (Upgrades):** Mecanismo funcional para comprar multiplicadores que modifican matemáticamente el valor de cada clic o activan la generación automática por segundo.
* **Persistencia de Datos Robustecida:** Uso de un motor relacional SQL para eliminar la volatilidad del estado del juego, asegurando que el progreso no se pierda al cerrar la aplicación.
* **Interfaz Modular (GUI):** Segmentación limpia de las pantallas del juego mediante pestañas independientes (`principal_tab.py`, `tienda_tab.py`, `ajustes_tab.py`).

---

## 🔐 Módulo de Autenticación, Usuarios y Gestión CRUD (Flet + MySQL)

Este módulo comprende el sistema de seguridad, control de acceso y administración de datos. Está diseñado bajo estándares estrictos de validación tanto en el lado del cliente como del servidor.

### 1. Características del Módulo
* **Autenticación Segura (Login):** Control de acceso que valida las credenciales del usuario contra la base de datos antes de permitir la redirección a la interfaz del juego.
* **Registro y Validación Obligatoria:** Mecanismo de alta para nuevos usuarios con validaciones estrictas (formatos de correo válidos, campos obligatorios y restricción de duplicados en números de control o correos).
* **Recuperación de Contraseñas:** Flujo funcional para restablecer credenciales de forma segura en caso de pérdida, previa verificación de identidad en el sistema.
* **Panel CRUD Integrado:** Interfaz gráfica completa construida en Flet para realizar operaciones de Creación, Lectura, Actualización y Eliminación (CRUD) directamente sobre las tablas de la base de datos.

### 2. Entidades y Flujo de Información
El flujo de datos se gestiona a través de tres componentes o entidades clave dentro del modelo relacional:

1. **Usuario / Jugador (`usuarios`):** Almacena la identidad, credenciales de acceso (correo, contraseña, número de control) y el saldo financiero del juego (Pokédólares o clics totales).
2. **Mejoras / Tienda (`mejoras`):** Catálogo maestro con los objetos disponibles para compra, definidos por su costo base, tipo de beneficio (activo/pasivo) y factor multiplicador.
3. **Progreso / Inventario (`usuario_mejoras`):** Entidad asociativa (puente) que rompe la relación de muchos a muchos, registrando qué multiplicadores posee cada usuario específico y su nivel actual.

#### 🔄 Flujo de Información en el Sistema:
* **Flujo de Registro:** El usuario ingresa sus datos en la GUI. El sistema valida las reglas de negocio (ej. formato de correo institucional o campos vacíos). Al confirmar, los datos se insertan limpiamente en la base de datos.
* **Flujo de Inicio de Sesión:** Se capturan las credenciales. El sistema realiza una consulta (`SELECT`) filtrando por usuario/correo. Si coinciden los parámetros, se inicia la sesión activa en el entorno de Flet y se desbloquea el juego; de lo contrario, se despliega una alerta de error sin romper el flujo del programa.
* **Flujo de Recuperación:** Se solicita el correo o número de control verificado. El sistema comprueba su existencia en la base de datos para autorizar el restablecimiento inmediato de la contraseña.
* **Flujo de Juego y CRUD:** Al hacer clic en la pestaña principal, el controlador procesa el cambio, modifica el estado en memoria y actualiza la entidad `usuarios` en la base de datos. En la pestaña de la tienda, al comprar una mejora, se valida que el saldo sea suficiente, se descuenta el costo y se actualiza de forma síncrona la tabla asociativa `usuario_mejoras`.

---

## 📊 Arquitectura de Datos y Normalización (SQL)

Para mitigar la redundancia de datos y prevenir anomalías, la base de datos ha sido estructurada aplicando criterios de **Normalización hasta la Tercera Forma Normal (3FN)**. Las restricciones de integridad (Llaves Foráneas - `FOREIGN KEY`) aseguran la consistencia referencial con políticas de actualización y borrado en cascada.

A continuación se presenta la estructura analítica de la base de datos relacional requerida para el funcionamiento del sistema:

### Base de Datos: poke_clicker_db

#### 1. Tabla: usuarios
Soporta los flujos de autenticación, control de accesos y el estado general de recursos del jugador.
* **id_usuario:** Entero (`INT`), no nulo, auto-incremental. Llave Primaria.
* **num_control:** Cadena (`VARCHAR(20)`), no nulo, único.
* **nombre_usuario:** Cadena (`VARCHAR(50)`), no nulo.
* **correo:** Cadena (`VARCHAR(100)`), no nulo, único.
* **password:** Cadena (`VARCHAR(255)`), no nulo.
* **pokedolares:** Entero (`INT`), valor por defecto 0.
* **clics_totales:** Entero (`INT`), valor por defecto 0.
* **fecha_registro:** Marca de tiempo (`TIMESTAMP`), valor por defecto el tiempo actual del sistema.

#### 2. Tabla: mejoras
Catálogo centralizado de modificadores y elementos disponibles para la progresión económica interna.
* **id_mejora:** Entero (`INT`), no nulo, auto-incremental. Llave Primaria.
* **nombre:** Cadena (`VARCHAR(50)`), no nulo.
* **costo_base:** Entero (`INT`), no nulo.
* **multiplicador:** Decimal (`DECIMAL(5,2)`), no nulo.
* **tipo:** Enumeración (`ENUM('activo', 'pasivo')`), no nulo.

#### 3. Tabla: usuario_mejoras
Entidad relacional puente encargada de romper la relación de muchos a muchos y resguardar el inventario de las mejoras adquiridas.
* **id_usuario:** Entero (`INT`), no nulo.
* **id_mejora:** Entero (`INT`), no nulo.
* **nivel_actual:** Entero (`INT`), valor por defecto 1.

##### Restricciones de Integridad y Consistencia:
* **Llave Primaria Compuesta:** Formada en conjunto por los campos `id_usuario` e `id_mejora`.
* **Llave Foránea (fk_usuario_autenticado):** El campo `id_usuario` hace referencia a la tabla `usuarios` (`id_usuario`). Configurada con eliminación en cascada y actualización en cascada.
* **Llave Foránea (fk_mejora_adquirida):** El campo `id_mejora` hace referencia a la tabla `mejoras` (`id_mejora`). Configurada con eliminación en cascada y actualización en cascada.

---
> **Nota del Sistema:** La base de datos opera bajo el motor transaccional **InnoDB** utilizando el set de caracteres **utf8mb4** para asegurar un soporte multilenguaje completo.