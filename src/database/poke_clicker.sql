-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-06-2026 a las 01:01:17
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
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id_item_inv` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo` enum('pokemon','boost') NOT NULL,
  `item_id` varchar(50) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `cantidad` int(11) DEFAULT 1,
  `fecha_obtencion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_item_inv`, `id_usuario`, `tipo`, `item_id`, `nombre`, `cantidad`, `fecha_obtencion`) VALUES
(1, 1, 'boost', 'boost_x2', 'Boost x2 (5 min)', 1, '2026-05-27 22:58:22');

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
  `fin_boost` datetime DEFAULT NULL,
  `boost_tienda_fin` datetime DEFAULT NULL,
  `fin_boost_tienda` datetime DEFAULT NULL,
  `boost_tienda_pendiente` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `progreso_juego`
--

INSERT INTO `progreso_juego` (`id_progreso`, `id_usuario`, `clicks_actuales`, `clicks_totales`, `cantidad_rebirths`, `costo_siguiente_rebirth`, `multiplicador_activo`, `fin_boost`, `boost_tienda_fin`, `fin_boost_tienda`, `boost_tienda_pendiente`) VALUES
(1, 1, 18, 493, 0, 337, 1.25, '2026-05-27 17:28:48', NULL, NULL, 0),
(2, 2, 0, 475, 3, 337, 1.25, '2026-05-27 17:41:35', NULL, NULL, 0),
(3, 4, 262, 747, 0, 337, 2.75, '2026-06-02 15:46:50', NULL, NULL, 0),
(4, 5, 0, 1339, 60, 757, 3.25, '2026-05-28 16:41:38', NULL, NULL, 0),
(6, 6, 34, 138, 1, 150, 1.25, '2026-05-28 16:52:03', NULL, NULL, 0),
(7, 7, 66, 3407, 1, 1702, 2.75, '2026-06-02 16:05:38', NULL, '2026-06-02 16:04:41', 0),
(8, 8, 0, 875, 1, 505, 2, '2026-06-02 16:21:24', NULL, NULL, 1);

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

--
-- Volcado de datos para la tabla `tienda`
--

INSERT INTO `tienda` (`id_producto`, `nombre_producto`, `descripcion`, `categoria`, `costo_rebirths`, `valor_efecto`) VALUES
(1, 'Pokémon Aleatorio', '¡Obtén un pokémon al azar de la PokéAPI!', 'pokemon', 10, 1),
(2, 'Boost x2 (5 min)', 'Duplica tus clicks por 5 minutos', 'boost', 3, 2);

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
(1, 'sali', 'sali@gmail.com', '$2b$12$OHITACOZlYY.xnNwCUYfNORK/lM1wD7orMPJ7se0.7vhg3imosg.y', '2026-05-27 22:14:21'),
(2, 'feliz', 'feliz@gmail.com', '$2b$12$M2/p7e1Q10GIhuQ6XQljc.a1ZY30wOd3bPQv1yvV7leZvsr3TIF5i', '2026-05-27 23:26:13'),
(3, 'danis', '23308060610259@cetis61.edu.mx', '$2b$12$af/gh3XnGcsWoIEt/IofpOEh7zEw3fwknNg7MlYD91YxFHZwjImze', '2026-05-27 23:52:33'),
(4, 'danieles', 'danielisraelrenteria.c@gmail.com', '$2b$12$.0ogAvvumnieRTpJ2Kpjc.NB62ey69O1Fv6xWiyJKNC1e8ui.4Gqi', '2026-05-27 23:53:44'),
(5, 'salinas', 'salinas@gmail.com', '$2b$12$qqaCTYc6fFLX6/sCdE1qN.TnbeppmCVlkENikmRSr.1YmAInesCme', '2026-05-28 22:30:35'),
(6, 'solio', 'solio@gmail.com', '$2b$12$FlLk9I6.JTQQyy2sRUR1oOeshGFs6/UZIwa3UyO5Y3XowmDQI6OfK', '2026-05-28 22:46:31'),
(7, 'dalas', 'dalas@gmail.com', '$2b$12$vCTvY8.oCaltrLBCf9KGoeK8vNlEoYNwFcOZ.nxeqtiijigyehtpe', '2026-06-02 21:50:13'),
(8, 'domi', 'domi@gmail.com', '$2b$12$l54rYSvlg730CGVwDiPlFu1O34kDtEBNot12qkzvfsXdjK9RXFdz6', '2026-06-02 22:12:54');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id_item_inv`),
  ADD KEY `id_usuario` (`id_usuario`);

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
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id_item_inv` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `pokemones_obtenidos`
--
ALTER TABLE `pokemones_obtenidos`
  MODIFY `id_instancia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `progreso_juego`
--
ALTER TABLE `progreso_juego`
  MODIFY `id_progreso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `tienda`
--
ALTER TABLE `tienda`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

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
