-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.28-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.17.0.7270
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para poke_clicker
CREATE DATABASE IF NOT EXISTS `poke_clicker` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `poke_clicker`;

-- Volcando estructura para tabla poke_clicker.inventario
CREATE TABLE IF NOT EXISTS `inventario` (
  `id_item_inv` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `tipo` enum('pokemon','boost') NOT NULL,
  `item_id` varchar(50) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `cantidad` int(11) DEFAULT 1,
  `fecha_obtencion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_item_inv`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla poke_clicker.inventario: ~1 rows (aproximadamente)
INSERT INTO `inventario` (`id_item_inv`, `id_usuario`, `tipo`, `item_id`, `nombre`, `cantidad`, `fecha_obtencion`) VALUES
	(1, 1, 'boost', 'boost_x2', 'Boost x2 (5 min)', 1, '2026-05-27 22:58:22');

-- Volcando estructura para tabla poke_clicker.pokemones_obtenidos
CREATE TABLE IF NOT EXISTS `pokemones_obtenidos` (
  `id_instancia` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `pokemon_api_id` int(11) NOT NULL,
  `nombre_personalizado` varchar(50) DEFAULT NULL,
  `nivel` int(11) DEFAULT 1,
  `esta_equipado` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id_instancia`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `pokemones_obtenidos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla poke_clicker.pokemones_obtenidos: ~0 rows (aproximadamente)

-- Volcando estructura para tabla poke_clicker.progreso_juego
CREATE TABLE IF NOT EXISTS `progreso_juego` (
  `id_progreso` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `clicks_actuales` bigint(20) DEFAULT 0,
  `clicks_totales` bigint(20) DEFAULT 0,
  `cantidad_rebirths` int(11) DEFAULT 0,
  `costo_siguiente_rebirth` bigint(20) DEFAULT 100,
  `multiplicador_activo` float DEFAULT 1,
  `fin_boost` datetime DEFAULT NULL,
  `boost_tienda_fin` datetime DEFAULT NULL,
  `fin_boost_tienda` datetime DEFAULT NULL,
  `boost_tienda_pendiente` int(11) DEFAULT 0,
  PRIMARY KEY (`id_progreso`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `progreso_juego_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla poke_clicker.progreso_juego: ~7 rows (aproximadamente)
INSERT INTO `progreso_juego` (`id_progreso`, `id_usuario`, `clicks_actuales`, `clicks_totales`, `cantidad_rebirths`, `costo_siguiente_rebirth`, `multiplicador_activo`, `fin_boost`, `boost_tienda_fin`, `fin_boost_tienda`, `boost_tienda_pendiente`) VALUES
	(1, 1, 18, 493, 0, 337, 1.25, '2026-05-27 17:28:48', NULL, NULL, 0),
	(2, 2, 0, 475, 3, 337, 1.25, '2026-05-27 17:41:35', NULL, NULL, 0),
	(3, 4, 262, 747, 0, 337, 2.75, '2026-06-02 15:46:50', NULL, NULL, 0),
	(4, 5, 0, 1339, 60, 757, 3.25, '2026-05-28 16:41:38', NULL, NULL, 0),
	(6, 6, 34, 138, 1, 150, 1.25, '2026-05-28 16:52:03', NULL, NULL, 0),
	(7, 7, 66, 3407, 1, 1702, 2.75, '2026-06-02 16:05:38', NULL, '2026-06-02 16:04:41', 0),
	(8, 8, 0, 875, 1, 505, 2, '2026-06-02 16:21:24', NULL, NULL, 1);

-- Volcando estructura para tabla poke_clicker.tienda
CREATE TABLE IF NOT EXISTS `tienda` (
  `id_producto` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `categoria` enum('item','pokemon','boost') NOT NULL,
  `costo_rebirths` int(11) NOT NULL,
  `valor_efecto` float NOT NULL,
  PRIMARY KEY (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla poke_clicker.tienda: ~2 rows (aproximadamente)
INSERT INTO `tienda` (`id_producto`, `nombre_producto`, `descripcion`, `categoria`, `costo_rebirths`, `valor_efecto`) VALUES
	(1, 'Pokémon Aleatorio', '¡Obtén un pokémon al azar de la PokéAPI!', 'pokemon', 10, 1),
	(2, 'Boost x2 (5 min)', 'Duplica tus clicks por 5 minutos', 'boost', 3, 2);

-- Volcando estructura para tabla poke_clicker.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla poke_clicker.usuarios: ~8 rows (aproximadamente)
INSERT INTO `usuarios` (`id_usuario`, `username`, `email`, `password`, `fecha_registro`) VALUES
	(1, 'sali', 'sali@gmail.com', '$2b$12$OHITACOZlYY.xnNwCUYfNORK/lM1wD7orMPJ7se0.7vhg3imosg.y', '2026-05-27 22:14:21'),
	(2, 'feliz', 'feliz@gmail.com', '$2b$12$M2/p7e1Q10GIhuQ6XQljc.a1ZY30wOd3bPQv1yvV7leZvsr3TIF5i', '2026-05-27 23:26:13'),
	(3, 'danis', '23308060610259@cetis61.edu.mx', '$2b$12$af/gh3XnGcsWoIEt/IofpOEh7zEw3fwknNg7MlYD91YxFHZwjImze', '2026-05-27 23:52:33'),
	(4, 'danieles', 'danielisraelrenteria.c@gmail.com', '$2b$12$.0ogAvvumnieRTpJ2Kpjc.NB62ey69O1Fv6xWiyJKNC1e8ui.4Gqi', '2026-05-27 23:53:44'),
	(5, 'salinas', 'salinas@gmail.com', '$2b$12$qqaCTYc6fFLX6/sCdE1qN.TnbeppmCVlkENikmRSr.1YmAInesCme', '2026-05-28 22:30:35'),
	(6, 'solio', 'solio@gmail.com', '$2b$12$FlLk9I6.JTQQyy2sRUR1oOeshGFs6/UZIwa3UyO5Y3XowmDQI6OfK', '2026-05-28 22:46:31'),
	(7, 'dalas', 'dalas@gmail.com', '$2b$12$vCTvY8.oCaltrLBCf9KGoeK8vNlEoYNwFcOZ.nxeqtiijigyehtpe', '2026-06-02 21:50:13'),
	(8, 'domi', 'domi@gmail.com', '$2b$12$l54rYSvlg730CGVwDiPlFu1O34kDtEBNot12qkzvfsXdjK9RXFdz6', '2026-06-02 22:12:54');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
