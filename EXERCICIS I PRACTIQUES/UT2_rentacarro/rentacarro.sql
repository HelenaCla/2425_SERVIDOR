-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-08-2023 a las 18:42:35
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
-- Base de datos: `rentacarro`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carros`
--

CREATE TABLE `carros` (
  `id` int(11) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `clase` enum('basic','1cavall','2cavalls') NOT NULL,
  `preu` float NOT NULL,
  `descripcio` varchar(250) NOT NULL,
  `img` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `carros`
--

INSERT INTO `carros` (`id`, `nom`, `clase`, `preu`, `descripcio`, `img`) VALUES
(1, 'Carro simple', 'basic', 75, 'Un carro economic i familiar', 'carro1.png'),
(2, 'Western', 'basic', 90, 'Preparat per la conquesta de l\'oest!', 'carro2.png'),
(3, 'Utilitari 2px', '1cavall', 105, 'Amb aquest carretó seràs l\'enveja de les veinades', 'carro3.png'),
(4, 'Deportiu', '2cavalls', 180, 'Si t\'agrada la velocitat', 'carro4.png');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `idcarro` int(11) NOT NULL,
  `iniciReserva` datetime NOT NULL,
  `finalReserva` datetime NOT NULL,
  `usuario` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`idcarro`, `iniciReserva`, `finalReserva`, `usuario`) VALUES
(1, '2023-11-19 18:00:00', '2023-11-23 12:00:00', 'Joe Doe'),
(2, '2023-11-20 00:00:00', '2023-11-21 00:00:00', 'Jane Fletcher');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carros`
--
ALTER TABLE `carros`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`idcarro`,`iniciReserva`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carros`
--
ALTER TABLE `carros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`idcarro`) REFERENCES `carros` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
