-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-04-2024 a las 01:12:15
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
-- Base de datos: `registros`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(10) NOT NULL,
  `Phone` bigint(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `Phone`) VALUES
(4, 'xEmmanuelCobax123', 'emmanuelcobacu123123evas@gmail.com', '123', NULL),
(5, 'xEmmanuelCobax123123', 'emmanuelcobacu112323123evas@gmail.com', '123123', NULL),
(6, 'xEmmanuelCobax121233123', 'emmanuelcobacu112323123123evas@gmail.com', '123', NULL),
(7, 'emmanuelcoba123cuevas@gmail.com', '123@12312', '123123', NULL),
(8, 'emmanuelcobacuevas@gmail.com123', '12312323@12312', '12313213', NULL),
(9, 'e4201123', '123@123123123', '12312312', NULL),
(10, 'dawdwadawd', '123213!@312312', '12312', NULL),
(11, '123123123', 'l04220011236@pr123ogreso.tecnm.mx', '123123', NULL),
(12, '123', '123@213', '123', NULL),
(13, 'u123213', 'uyu@123', '123', NULL),
(14, '211231', '123213@1231231', '213123', NULL),
(15, '123@12312', '123@31223', '1233', NULL),
(16, '234324324', 'emmanue234324324co324bacuevas234234@gmail.com', '234234', NULL),
(17, 'e4202343241', 'emmanuelco23234bacuevas@234324gmail.com', '234234324', NULL),
(18, 'e4201123123', 'emmanue123123cobacuevas@gmail123123.com', '123213', NULL),
(19, '123xEmm232anuelCobax223', 'emm123anuelcobacuevas123@gmail.co1233123', '123', NULL),
(20, 'emmanuelcobacuevas@gmail.com', 'emmanu123321elcob123123acuevas@gmail.com', '123123213', NULL),
(21, '1232314434312312313123', 'e12333123mmanue12123lcobacuevas@gmail.com', '12312323', NULL),
(22, '123123', 'e312mma123n231uelcobacuevas@123gmail.312om', '1231231231', NULL),
(26, 'xEmmanuelCobax', 'l04220016@progreso.tecnm.mx', '123', 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
