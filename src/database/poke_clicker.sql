-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-05-2026 a las 23:45:27
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `poke_clicker`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_items`
--

CREATE TABLE `inventario_items` (
  `id_item_inv` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pokemones_obtenidos`
--

CREATE TABLE `pokemones_obtenidos` (
  `id_instancia` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `pokemon_api_id` int(11) NOT NULL,
  `nombre_personalizado` varchar(50) DEFAULT NULL,
  `nivel` int(11) DEFAULT 1,
  `esta_equipado` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `progreso_juego`
--

CREATE TABLE `progreso_juego` (
  `id_progreso` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `clicks_actuales` bigint(20) DEFAULT 0,
  `clicks_totales` bigint(20) DEFAULT 0,
  `cantidad_rebirths` int(11) DEFAULT 0,
  `costo_siguiente_rebirth` bigint(20) DEFAULT 100,
  `multiplicador_activo` float DEFAULT 1,
  `fin_boost` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `progreso_juego`
--

INSERT INTO `progreso_juego` (`id_progreso`, `id_usuario`, `clicks_actuales`, `clicks_totales`, `cantidad_rebirths`, `costo_siguiente_rebirth`, `multiplicador_activo`, `fin_boost`) VALUES
(1, 6, 51, 526, 3, 337, 1, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tienda`
--

CREATE TABLE `tienda` (
  `id_producto` int(11) NOT NULL,
  `nombre_producto` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `categoria` enum('item','pokemon','boost') NOT NULL,
  `costo_rebirths` int(11) NOT NULL,
  `valor_efecto` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `username`, `email`, `password`, `fecha_registro`) VALUES
(1, 'daniel', 'dani@gmail.com', '$2b$12$mliCCNl4A2f0W1QW23Knyer6nmKqRYj4oT.s8f4xujDoLfXJMt71e', '2026-05-18 23:12:26'),
(2, 'san', 'san@gmail.com', '$2b$12$NUjJsecPG2kKAM6JATKbe.W9j90nhUwt9ZHB2knpDJq6ZZd4lg5u6', '2026-05-18 23:29:36'),
(3, 'DAN', 'dan@gmail.com', '$2b$12$.gAxr2/vvGhA6fOnN70ruu5QbVJLTA2KiQCdW7mexV.5MEVKjEmYC', '2026-05-18 23:31:28'),
(4, 'Salo', 'salo@gmail.com', '$2b$12$gO7g/RKqEkEbP1YO.G8MQOU2QlX79AmXEgkGHBbjQuS1gDIvbclSe', '2026-05-18 23:32:56'),
(5, 'Sula', 'sula@gmail.com', '$2b$12$91FLRjH24eP/bCryNGnypuQ2Yv8SSgkK7vErRgZOfjhY3Efarupea', '2026-05-18 23:35:57'),
(6, 'JESUSDANIELRENTERIACALZADA', '23308060610259@cetis61.edu.mx', '$2b$12$ZeRiVodqz.4k6hswAy/wKO3SQPAwNuH4OfZqO2eP6I4bTlkS.8YbG', '2026-05-19 00:45:05'),
(7, 'dani', 'danielisrael@gmail.com', '$2b$12$p/n90pfuof753DfR7gs5HukY7s47qNSnixHtLuN2Yzjf0.EcuecsO', '2026-05-19 23:22:18'),
(8, 'danis', 'danielisraelrenteria.c@gmail.com', '$2b$12$/bg3kV4dzXLIMPwcvwH3vO1GE7YZ4qsR.abzZit8tpC10FLlMVAqW', '2026-05-20 22:17:17'),
(9, 'dasai', 'dasai@gmail.com', '$2b$12$4tUW4BsQhOhBBnA0uNg3mOJfXyYWA1aJ5Ho7ErV7naktesAMMtCCO', '2026-05-21 23:58:45');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `inventario_items`
--
ALTER TABLE `inventario_items`
  ADD PRIMARY KEY (`id_item_inv`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `pokemones_obtenidos`
--
ALTER TABLE `pokemones_obtenidos`
  ADD PRIMARY KEY (`id_instancia`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `progreso_juego`
--
ALTER TABLE `progreso_juego`
  ADD PRIMARY KEY (`id_progreso`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `tienda`
--
ALTER TABLE `tienda`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `inventario_items`
--
ALTER TABLE `inventario_items`
  MODIFY `id_item_inv` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pokemones_obtenidos`
--
ALTER TABLE `pokemones_obtenidos`
  MODIFY `id_instancia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `progreso_juego`
--
ALTER TABLE `progreso_juego`
  MODIFY `id_progreso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `tienda`
--
ALTER TABLE `tienda`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `inventario_items`
--
ALTER TABLE `inventario_items`
  ADD CONSTRAINT `inventario_items_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `inventario_items_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `tienda` (`id_producto`) ON DELETE CASCADE;

--
-- Filtros para la tabla `pokemones_obtenidos`
--
ALTER TABLE `pokemones_obtenidos`
  ADD CONSTRAINT `pokemones_obtenidos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `progreso_juego`
--
ALTER TABLE `progreso_juego`
  ADD CONSTRAINT `progreso_juego_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
