-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-11-2024 a las 17:28:11
-- Versión del servidor: 10.4.14-MariaDB
-- Versión de PHP: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `vols`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `airports`
--

CREATE TABLE `airports` (
  `id_airport` char(3) NOT NULL,
  `location` varchar(30) DEFAULT NULL,
  `country` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `airports`
--

INSERT INTO `airports` (`id_airport`, `location`, `country`) VALUES
('AMS', 'Amsterdam', 'HOLANDA'),
('BCN', 'Barcelona', 'ESPAÑA'),
('BIO', 'Bilbao', 'ESPAÑA'),
('LIS', 'Lisboa', 'PORTUGAL'),
('MAD', 'Madrid', 'ESPAÑA'),
('ORY', 'París', 'FRANCIA'),
('PMI', 'Palma de Mallorca', 'ESPAÑA'),
('TFN', 'Tenerife Norte', 'ESPAÑA'),
('TFS', 'Tenerife Sur', 'ESPAÑA'),
('VRN', 'Verona', 'ITALIA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `crews`
--

CREATE TABLE `crews` (
  `id_crew` int(11) NOT NULL,
  `alias` varchar(20) DEFAULT NULL,
  `firstname` varchar(30) DEFAULT NULL,
  `surname` varchar(30) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `mobile_phone` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `crews`
--

INSERT INTO `crews` (`id_crew`, `alias`, `firstname`, `surname`, `email`, `mobile_phone`) VALUES
(1, 'PEPE', 'José Maria', 'Torres Quetglas', 'pepe@airline.com', '111222222'),
(2, 'JUAN', 'Juan', 'Maroto Quetglas', 'juan@airline.com', '112123456'),
(3, 'PACO', 'Francisco', 'Mas Jaume', 'paco@airline.com', '113654321'),
(4, 'TONI', 'Antonio', 'Gibert Ximenes', 'toni@airline.com', '114456789'),
(5, 'PEPA', 'Francisca', 'Cerdá Alorda', 'pepa@airline.com', '115888888'),
(6, 'XISCO', 'Francisco', 'Méndez Gómez', 'xisco@airline.com', '116989898'),
(7, 'ALLY', 'Alícia', 'Foord', 'ally@airline.com', '117777777'),
(8, 'JOHN', 'John Brown', 'Reus Mateu', 'john@airline.com', '118987654'),
(9, 'JUANA', 'Juana Maria', 'Vives Barceló', 'juana@airline.com', '119456789');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `flights`
--

CREATE TABLE `flights` (
  `id_flight` int(11) NOT NULL,
  `flight_number` char(5) DEFAULT NULL,
  `departure_airport` char(3) DEFAULT NULL,
  `arrival_airport` char(3) DEFAULT NULL,
  `departure_time` datetime DEFAULT NULL,
  `arrival_time` datetime DEFAULT NULL,
  `number_pax` int(11) DEFAULT NULL,
  `id_pilot` int(11) DEFAULT NULL,
  `id_copilot` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `flights`
--

INSERT INTO `flights` (`id_flight`, `flight_number`, `departure_airport`, `arrival_airport`, `departure_time`, `arrival_time`, `number_pax`, `id_pilot`, `id_copilot`) VALUES
(20, 'UX265', 'VRN', 'BCN', '2025-01-11 18:00:00', '2025-01-11 20:00:00', 91, 7, 2),
(21, 'JK338', 'PMI', 'TFS', '2025-01-12 15:00:00', '2025-01-12 16:30:00', 65, 7, 8),
(22, 'JK135', 'TFN', 'BIO', '2025-01-12 23:30:00', '2025-01-13 01:25:00', 80, 9, 8),
(23, 'JK389', 'VRN', 'PMI', '2025-01-13 12:50:00', '2025-01-13 14:55:00', 70, 6, 9),
(24, 'AT299', 'BIO', 'MAD', '2025-01-14 16:20:00', '2025-01-14 17:30:00', 73, 5, 2),
(25, 'JK598', 'MAD', 'BIO', '2025-01-15 10:00:00', '2025-01-15 11:10:00', 103, 5, 3),
(26, 'PH993', 'PMI', 'ORY', '2025-01-16 22:10:00', '2025-01-16 23:55:00', 91, 6, 7),
(36, 'JK644', 'AMS', 'ORY', '2025-01-08 22:00:00', '2025-01-08 23:45:00', 110, 2, 9),
(37, 'JK978', 'TFS', 'AMS', '2025-01-08 23:45:00', '2025-01-09 01:50:00', 76, 1, 3),
(38, 'JK187', 'PMI', 'ORY', '2025-01-09 15:00:00', '2025-01-09 16:15:00', 98, 1, 4),
(39, 'JK267', 'BCN', 'MAD', '2024-11-09 09:40:00', '2024-11-09 10:40:00', 99, 7, 1),
(41, 'JK623', 'BCN', 'PMI', '2025-01-05 17:00:00', '2025-01-05 17:30:00', 90, 1, 9),
(42, 'JK621', 'MAD', 'BCN', '2025-01-05 19:00:00', '2025-01-05 19:45:00', 92, 1, 3),
(43, 'JK611', 'TFN', 'BIO', '2024-10-09 12:00:00', '2024-10-09 13:15:00', 120, 1, 7),
(45, 'JK622', 'LIS', 'BIO', '2024-10-10 06:10:00', '2024-10-10 08:15:00', 87, 6, 9),
(47, 'UX633', 'PMI', 'LIS', '2025-01-07 13:20:00', '2025-01-07 14:35:00', 90, 8, 9),
(56, 'JK444', 'ORY', 'AMS', '2025-01-08 21:00:00', '2025-01-08 21:45:00', 110, 2, 9),
(57, 'JK678', 'AMS', 'TFS', '2025-01-08 23:05:00', '2025-01-09 01:30:00', 76, 1, 3),
(58, 'JK987', 'ORY', 'PMI', '2025-01-09 13:00:00', '2025-01-09 14:15:00', 98, 1, 4),
(59, 'JK567', 'BCN', 'MAD', '2024-11-09 08:40:00', '2024-11-09 09:40:00', 99, 7, 1),
(60, 'UX765', 'VRN', 'BCN', '2025-01-11 17:00:00', '2025-01-11 19:00:00', 91, 7, 2),
(61, 'JK838', 'PMI', 'TFS', '2025-01-12 12:00:00', '2025-01-12 13:30:00', 65, 7, 8),
(62, 'JK435', 'TFN', 'BIO', '2025-01-12 23:50:00', '2025-01-13 01:45:00', 80, 9, 8),
(63, 'JK789', 'VRN', 'PMI', '2025-01-13 12:00:00', '2025-01-13 14:05:00', 70, 6, 9),
(64, 'AT899', 'BIO', 'MAD', '2025-01-14 12:20:00', '2025-01-14 13:30:00', 73, 5, 2),
(65, 'JK098', 'MAD', 'BIO', '2025-01-15 11:00:00', '2025-01-15 11:30:00', 103, 5, 3),
(66, 'PH299', 'PMI', 'ORY', '2025-01-16 22:00:00', '2025-01-16 23:45:00', 91, 6, 7),
(81, 'JK123', 'PMI', 'BCN', '2025-01-05 12:00:00', '2025-01-05 12:30:00', 90, 1, 9),
(82, 'JK321', 'BCN', 'MAD', '2025-01-05 18:00:00', '2025-01-05 18:45:00', 92, 1, 3),
(83, 'JK111', 'BIO', 'TFN', '2024-10-09 10:00:00', '2024-10-09 11:15:00', 120, 1, 7),
(85, 'JK222', 'BIO', 'LIS', '2024-10-10 09:10:00', '2024-10-10 10:15:00', 87, 6, 9),
(87, 'UX333', 'LIS', 'PMI', '2025-01-07 19:20:00', '2025-01-07 20:35:00', 90, 8, 9);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `airports`
--
ALTER TABLE `airports`
  ADD PRIMARY KEY (`id_airport`);

--
-- Indices de la tabla `crews`
--
ALTER TABLE `crews`
  ADD PRIMARY KEY (`id_crew`);

--
-- Indices de la tabla `flights`
--
ALTER TABLE `flights`
  ADD PRIMARY KEY (`id_flight`),
  ADD KEY `departure_airport` (`departure_airport`),
  ADD KEY `arrival_airport` (`arrival_airport`),
  ADD KEY `id_pilot` (`id_pilot`),
  ADD KEY `id_copilot` (`id_copilot`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `flights`
--
ALTER TABLE `flights`
  ADD CONSTRAINT `flights_ibfk_1` FOREIGN KEY (`departure_airport`) REFERENCES `airports` (`id_airport`),
  ADD CONSTRAINT `flights_ibfk_2` FOREIGN KEY (`arrival_airport`) REFERENCES `airports` (`id_airport`),
  ADD CONSTRAINT `flights_ibfk_3` FOREIGN KEY (`id_pilot`) REFERENCES `crews` (`id_crew`),
  ADD CONSTRAINT `flights_ibfk_4` FOREIGN KEY (`id_copilot`) REFERENCES `crews` (`id_crew`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
