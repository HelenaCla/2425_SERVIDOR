-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-11-2021 a las 16:30:59
-- Versión del servidor: 10.4.6-MariaDB-log
-- Versión de PHP: 7.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `usuarisut4`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuaris`
--

CREATE TABLE `usuaris` (
  `id` int(3) NOT NULL,
  `usuari` varchar(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `rol` enum('admin','user','','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `usuaris`
--

INSERT INTO `usuaris` (`id`, `usuari`, `password`, `email`, `rol`) VALUES
(1, 'root', 'pbkdf2:sha256:150000$zBIzWPI6$7e92ed04ee10e63c8acafa849c2fa203cef5ba57a7ab128dbbf05fc84d9643b8', 'administrador@paucasesnovescifp.cat', 'admin'),
(2, 'user1', 'pbkdf2:sha256:150000$xFCVeLDa$723a1c81148d1bdcf5dd8b69699d2de55c4aa51aab5fcae9e977ae9929313e07', 'user1@hotmail.com', 'user');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuaris`
--
ALTER TABLE `usuaris`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
