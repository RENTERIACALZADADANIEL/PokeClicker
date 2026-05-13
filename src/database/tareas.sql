-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-03-2026 a las 04:11:41
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
-- Base de datos: `tareas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `id_tarea` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT current_timestamp(),
  `fecha_limite` date DEFAULT NULL,
  `hora_limite` time DEFAULT NULL,
  `estado` enum('pendiente','en_progreso','completada','cancelada') DEFAULT 'pendiente',
  `clasificacion` enum('personal','trabajo','estudio','hogar','salud','otro') DEFAULT 'personal',
  `prioridad` enum('baja','media','alta') DEFAULT 'media',
  `completada` tinyint(1) DEFAULT 0,
  `fecha_completada` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`id_tarea`, `id_usuario`, `titulo`, `descripcion`, `fecha_creacion`, `fecha_limite`, `hora_limite`, `estado`, `clasificacion`, `prioridad`, `completada`, `fecha_completada`) VALUES
(1, 1, 'Terminar la preparatoria', 'Completar todos los estudios de nivel medio superior', '2026-03-20 03:10:01', '2026-07-01', NULL, 'en_progreso', 'estudio', 'alta', 0, NULL),
(2, 1, 'Ingresar a la universidad', 'Entrar a la carrera de manufactura', '2026-03-20 03:10:01', '2027-01-15', NULL, 'pendiente', 'estudio', 'alta', 0, NULL),
(3, 1, 'Aprender programación avanzada', 'Dominar programación orientada a objetos', '2026-03-20 03:10:01', '2027-12-01', NULL, 'en_progreso', 'estudio', 'media', 0, NULL),
(4, 1, 'Conseguir mi primer empleo', 'Obtener experiencia laboral en mi área', '2026-03-20 03:10:01', '2027-06-01', NULL, 'pendiente', 'trabajo', 'alta', 0, NULL),
(5, 1, 'Comprar un automóvil', 'Ahorrar y comprar mi primer auto', '2026-03-20 03:10:01', '2028-12-01', NULL, 'pendiente', 'personal', 'media', 0, NULL),
(6, 1, 'Mantener vida saludable', 'Hacer ejercicio y buena alimentación', '2026-03-20 03:10:01', NULL, NULL, 'en_progreso', 'salud', 'alta', 0, NULL),
(7, 1, 'Ahorrar para una casa', 'Juntar dinero para una casa propia', '2026-03-20 03:10:01', '2030-01-01', NULL, 'pendiente', 'hogar', 'alta', 0, NULL),
(8, 1, 'Segunda carrera o especialidad', 'Estudiar otra carrera o especialización', '2026-03-20 03:10:01', '2032-01-01', NULL, 'pendiente', 'estudio', 'media', 0, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT current_timestamp(),
  `ultimo_acceso` timestamp NULL DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `foto_perfil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `nombre`, `apellido`, `email`, `password`, `telefono`, `fecha_registro`, `ultimo_acceso`, `activo`, `foto_perfil`) VALUES
(1, 'Admin', 'Principal', 'admin@tareas.com', '123456', '6560000000', '2026-03-20 03:10:01', NULL, 1, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id_tarea`),
  ADD KEY `idx_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id_tarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `fk_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
