# 🎮 Poke-Clicker

[cite_start]**Poke-Clicker** es un proyecto de videojuego tipo **"Idle Clicker"** donde la progresión del jugador se basa en la acumulación de clics y la gestión estratégica de recursos inspirados en el universo Pokémon[cite: 13, 14].

---

## 📝 Descripción del Proyecto

El objetivo principal es acumular clics para avanzar en el juego. [cite_start]La experiencia comienza desde cero: al realizar el primer clic, el sistema interactúa con la **PokéAPI** para otorgar al usuario un Pokémon inicial de forma totalmente aleatoria[cite: 14, 15].

### Mecánicas Principales

* **Sistema de Rebirth (Renacimiento):** Al alcanzar una cantidad considerable de clics, el jugador tiene la opción de "renacer". [cite_start]Esta acción resetea el contador de clics actuales, pero otorga un **Boost de velocidad** (incremento de clics por segundo) durante unos minutos, permitiendo una recuperación acelerada del nivel[cite: 16, 17].
* [cite_start]**Tienda:** Un espacio dedicado para intercambiar puntos de renacimiento por artículos de utilidad[cite: 18]:
    * [cite_start]**Caramelos:** Objetos para subir de nivel a los Pokémon y activar sus evoluciones[cite: 19].
    * [cite_start]**Mejoras de Boost:** Adquisición de potenciadores de clics adicionales[cite: 20].
    * [cite_start]**Pokémon Aleatorios:** Posibilidad de probar suerte para obtener nuevas criaturas[cite: 21].
* [cite_start]**Inventario:** Repositorio personal donde se almacenan permanentemente todas las compras, ganancias y Pokémon obtenidos[cite: 22].

---

## 📊 Estructura de la Base de Datos

[cite_start]El diseño lógico de la base de datos está optimizado para gestionar de manera eficiente la información de los usuarios, su progreso dinámico y la integración con datos externos de la PokéAPI[cite: 23].

### Diagrama Entidad-Relación (MER)

![Diagrama MER de Poke-Clicker](imagenes/image.png)

[cite_start]*El diagrama anterior detalla las relaciones entre las entidades de Usuario, Progreso, Tienda, Inventario y Pokémon obtenidos[cite: 23].*

---

## 💻 Implementación Técnica (SQL)

[cite_start]A continuación, se presenta el script necesario para generar la estructura de tablas y las restricciones de integridad (llaves foráneas) que aseguran la consistencia de los datos[cite: 105].

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