-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-03-2024 a las 05:52:31
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
  `password` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`) VALUES
(1, 'xEmmanuelCobax', 'emmanuelcobacuevas@gmail.com', '1234'),
(2, 'xEmmanuelCoba2x', '12312@123', '123123'),
(3, 'e4201', 'l04220016@progreso.tecnm.mx', '1233'),
(4, 'xEmmanuelCobax123', 'emmanuelcobacu123123evas@gmail.com', '123'),
(5, 'xEmmanuelCobax123123', 'emmanuelcobacu112323123evas@gmail.com', '123123'),
(6, 'xEmmanuelCobax121233123', 'emmanuelcobacu112323123123evas@gmail.com', '123'),
(7, 'emmanuelcoba123cuevas@gmail.com', '123@12312', '123123'),
(8, 'emmanuelcobacuevas@gmail.com123', '12312323@12312', '12313213'),
(9, 'e4201123', '123@123123123', '12312312'),
(10, 'dawdwadawd', '123213!@312312', '12312'),
(11, '123123123', 'l04220011236@pr123ogreso.tecnm.mx', '123123'),
(12, '123', '123@213', '123'),
(13, 'u123213', 'uyu@123', '123'),
(14, '211231', '123213@1231231', '213123'),
(15, '123@12312', '123@31223', '1233'),
(16, '234324324', 'emmanue234324324co324bacuevas234234@gmail.com', '234234'),
(17, 'e4202343241', 'emmanuelco23234bacuevas@234324gmail.com', '234234324'),
(18, 'e4201123123', 'emmanue123123cobacuevas@gmail123123.com', '123213');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
