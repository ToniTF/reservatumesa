-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 17-03-2025 a las 19:57:10
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `reservatumesa`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `client`
--

DROP TABLE IF EXISTS `client`;
CREATE TABLE IF NOT EXISTS `client` (
  `client_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `client`
--

INSERT INTO `client` (`client_id`, `username`, `password`, `email`, `phone`) VALUES
(1, 'ComeYCorre', '$2b$12$ePD9tpUDBHwSyvIYWCQy3udrboj.LG7xXwZIVFud1NLA73HKQSd.S', '', '678 123 456'),
(2, 'MesaQueMasAplauda', '$2b$12$cfd25rxgyGyJFiVfOYR9ee9f/ANxtpe2HS0EKupFE5DKv4QY8H1qG', '', '612 987 654'),
(3, 'Tragoncio22', '$2b$12$Iv0VPmTI2lGewW/YUxlT8OPRO20Lm/wsFxiF.iGPteMbJYiO/QK5a', '', '645 321 789'),
(4, 'SillaCaliente', '$2b$12$VGCXFv8PmSJWadDnIR81hOREA/So3u/AdgkGVjEzVFDE2GB/0F0x6', '', '690 456 123'),
(5, 'ComeTierraPro', '$2b$12$w3z/6nGOMxF2mjgmZjj.cOnmOz/PTvge6Q.ZyO0F2rmYizfr8SnN.', '', '655 789 321'),
(6, 'DameTuMesa', '$2b$12$D88GNU69HPetABKkSeT0BeoGu3roIHLCpk4JoRzTgx77755oP6vee', '', '687 234 567'),
(7, 'FullPlato99', '$2b$12$sZSVjnOrxvRCKY8v.b10JOiwmAV5zMwNdLs76JrdTX4PMwsynql.m', '', '620 345 678'),
(8, 'BarrigaLlenaVIP', '$2b$12$1jwfzJij6GxqrEeKe9g23e73CAMX0zy/4lUxdldOjLIdYRNBKnC/e', '', '699 876 543'),
(9, 'ReservoYNoVoy', '$2b$12$2jJRG6H8Oc2MP4smnGW49eqpOZttQWgOG3zbOHAcoczETczkZj/Sq', '', '635 210 987'),
(10, 'ReyDelTenedor', '$2b$12$PgSOdL6vEfODcmTXUQ3aAOK9e01ErRxRl58Uys.i5Pgpx09DOEQ4W', '', '670 432 156'),
(18, 'Toni', '$2b$12$TzLs44p.z1sPuOfLriJQ7.6L1NYEcwWMd/Y0A0g2uCZY5re1zvGGm', 'admin@admin.es', '986458784');

-- --------------------------------------------------------
-- Estructura de tabla para la tabla `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
CREATE TABLE IF NOT EXISTS `restaurant` (
  `restaurant_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `restaurant_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `capacity` int NOT NULL,
  `website` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `address` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci,
  `image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `restaurant`
--

INSERT INTO `restaurant` (`restaurant_id`, `username`, `email`, `password`, `phone`, `restaurant_name`, `capacity`, `website`, `address`, `description`, `image`) VALUES
(1, 'ElReyDelBuffet ', 'elreydelbuffet@gmail.com', '$2b$12$GayWUl0kaswQoKBKla8xtO4vU1S4DfJyll1BAi/HZFkq/hE.lEVyC', '678 901 234', 'El Rey del Buffet', 40, 'www.reydelbuffet.com', 'Calle del Atracón, 12', 'Buffet libre con más de 100 platos, postres ilimitados y bebidas incluidas.', 'elreydelbuffet.jpg'),
(2, 'TacoLcoco ', 'tacolcoco@gmail.com', '$2b$12$etyFl4lBbHztCrApxTQfsOLilAZ1CXiJUpX.NAcJ4nHer4Lal6lae', '612 345 678', 'Taco Locco', 30, 'www.tacolocco.com', 'Avenida Picante, 45', 'Auténtica comida mexicana, tacos al pastor y nachos con queso fundido.', 'tacoloco.jpg'),
(3, 'FritangaVIP', 'fritangavip@gmail.com', '$2b$12$bbdvUtEK4nbZemOGQeANwu8kB6xdJ31YkHmh6RHEAgHU.d.wv7dyi', '645 789 123', 'Fritanga VIP', 25, 'www.fritangavip.com', 'Plaza del Aceite, 7', 'Especialidad en frituras de todo tipo, desde calamares hasta churros rellenos.', 'fritangavip.jpg'),
(4, 'Pizzarollit0', 'pizzarolli0@gmail.com', '$2b$12$QkjT3JbNn9BgKQpZHWoFkORaW.HGdQLEWx0zh8sR1BsYLjC7s1yhq', '690 234 567', 'Pizzarollito', 35, 'www.pizzarollito.com', 'Calle de la Masa, 99', 'Pizzería artesanal con horno de leña y opciones veganas.', 'pizzarolito.jpg'),
(5, 'HamburQueen', 'hamburqueen@gmail.com', '$2b$12$ueTa8wwQ6/oOsfmcGUjI4uE35xQeb/flqad69wqWK2wJomZaddb8e', '655 876 432', 'HamburQueen', 40, 'www.hamburqueen.com', 'Paseo del Sabor, 21', 'Hamburguesas gourmet con ingredientes premium y salsas caseras.', 'hamburqueen.jpg'),
(6, 'ComeQueTeVas', 'comequetevas@gmail.com', '$2b$12$Rbu2StmZbyxJGWLN..SLEu0c58/fCVdrnaV2xAKcZzlLryHsizzuO', ' 687 321 098', 'Come Que Te Vas', 20, 'www.comequetevas.com', 'Camino del Hambre, 5', 'Menús rápidos para los que tienen prisa, sin perder sabor.', 'comequetevas.jpg'),
(7, 'SushiMunchies', 'sushimunchies@gmail.com', '$2b$12$TM1vlnYIiYvPSOXeD9son.pOU.2dfWTnveltwDHv/7Ja4YlP/j8Be', '620 654 321', 'Sushi Munchies', 30, 'www.sushimunchies.com', 'Calle de la Soja, 10', 'Sushi fusión con opciones innovadoras y sabores únicos.', 'sushimunchies.jpg'),
(8, 'GordiPasta', 'gordipasta@gmail.com', '$2b$12$8zPWG7a30nQWGWgJeVuee.7qoRvkVSFOrMGAKKv11po0tsBs2gGpq', '699 210 876', 'GordiPasta', 25, 'www.gordipasta.com', 'Avenida Italiana, 88', 'Pastas caseras con salsas abundantes y pan de ajo ilimitado.', 'gordipasta.jpg'),
(9, 'WokAndRoll', 'wokandroll@gmail.com', '$2b$12$/MxUnez8Yyfhq3.zGrvqi.9K/jOKU.mIdxEdQVBVgcHT3P.tW33ly', '635 543 210', 'Wok & Roll', 30, 'www.wokandroll.com', 'Calle del Dragón, 23', 'Cocina asiática al wok con ingredientes frescos y show en vivo.', 'wokandroll.jpg'),
(10, 'PollosLocos', 'polloslocos@gmail.com', '$2b$12$gmJiiUwrP/H7VPwlN3l0qu/bnF4KMmcacHILGt2z07wLzpN9PK0Te', '670 876 543', 'Pollos Locos', 40, 'www.polloslocos.com', ' Plaza del Asador, 14', 'Especialistas en pollo frito crujiente y salsas caseras.', 'polloslocos.jpg'),
(11, 'CarnivoroXtreme', 'carnivoroextreme@gmail.com', '$2b$12$qa6mGPG0IdSOLiyh/V0UjuOZkoxb1FYGhn8rXUup1RF6qhmbjAG3K', '658 987 432', 'Carnívoro Xtreme', 35, 'www.carnivoroxtreme.com', 'Calle de la Barbacoa, 66', 'Parrillada de carnes con cortes premium y chimichurri casero.', 'carnivoroxtreme.jpg'),
(12, 'EmpanadaPower', 'empanadapower@gmail.com', '$2b$12$yLdH8ZpXnj/yiplsY8wyh.EAYFLmH1ghb5VCyU.lXbWndCbuSNNce', '625 432 678', 'Empanada Power', 20, 'www.empanadapower.com', 'Calle del Horno, 3', 'Empanadas argentinas y venezolanas con variedad de rellenos.', 'empanadapower.jpg'),
(13, 'VeggieLover', 'veggielover@gmail.com', '$2b$12$G3bCdCMUWtCJVwHZ46G1luieZnJRKa.flX9LPHbetoSlUGxBoO.ji', ' 681 210 654', 'Veggie Lover', 25, 'www.veggielover.com', 'Paseo Verde, 11', 'Cocina vegetariana con ingredientes frescos y orgánicos.', 'veggielover.jpg'),
(14, 'ChocoLoco', 'chocoloco@gmail.com', '$2b$12$oUf90qNOxvg0zN/Evy1wSutwcDqX9VZr/6Tbbg8KW3m3v6CFsiqGS', '689 567 890', 'ChocoLoco', 15, 'www.chocoloco.com', ' Calle del Cacao, 50', 'Postres y bebidas de chocolate en todas sus formas.', 'chocoloco.jpg'),
(15, 'PatataBrava', 'patatabrava@gmail.com', '$2b$12$QZGnKwQ/7XOcNcoqyn6mhuAidYlti/FQU1Snex52TFx2xDj6Bb3Py', '674 678 321', 'Patata Brava', 20, 'www.patatabrava.com', 'Avenida de las Tapas, 8', 'Especialidad en patatas bravas con salsas caseras.', 'patatabrava.jpg'),
(16, 'Marisquito', 'marisquito@gmail.com', '$2b$12$.ko315AkJ//Xqyijaa2pbObBmZxAYvGSgK409gsElRCC0zAk1FF0e', '663 345 987', 'Marisquito', 35, 'www.marisquito.com', 'Paseo Marítimo, 17', 'Mariscos frescos y paellas con ingredientes de primera calidad.', 'marisquito.jpg'),
(17, 'ArepaFest', 'arepafest@gmail.com', '$2b$12$7TXLFLEAIhMzCa21qrMAyuBBTBeOdVwJL.bj/67PWIQI7cPV10WhK', ' 611 789 234', 'Arepa Fest', 25, 'https://www.arepafest.com', 'Calle de la Harina, 22', ' Arepas rellenas al mejor estilo venezolano y colombiano.', 'arepafest.jpg'),
(18, 'RolloPrimavera', 'rolloprimavera@gmail.com', '$2b$12$ErHvLb2lJ2mV3v2aVO9hCOs1ZyMx5bWkJJX6nIVC7dwUOe.koOxZ2', '648 654 789', 'Rollo Primavera', 30, 'www.rolloprimavera.com', 'Barrio Chino, 29', 'ocina asiática con especialidad en rollitos de primavera y dumplings.', 'rolloprimavera.jpg'),
(19, 'TodoAlHorno', 'todoalhorno@gmail.com', '$2b$12$hsiO8pmRbzd/G7e6NR0PYOzk7HK7lkwc5eIsiaMylBVfPdLdN215S', '630 876 210', 'Todo al Horno', 40, ' www.todoalhorno.com', 'Calle del Fuego, 77', 'Platos cocinados al horno para una experiencia sin frituras.', 'todoalhorno.jpg'),
(20, 'CucharaDeOro', 'cucharadeoro@gmail.com', '$2b$12$OjezuacEZf0Vk0xrV/V9DeDryFZogkHfmtq17QjqJPUkYkRJzkqKC', '679 543 876', 'Cuchara de Oro', 25, 'www.cucharadeoro.com', 'Calle de la Abuela, 6', 'Comida casera con recetas tradicionales y sopas abundantes.', 'cucharadeoro.jpg'),
(31, 'Admin', 'adminrest@adminrest.com', '$2b$12$spFmCUXai29gSUGtJ917TObSqXtamTtiznSANxIOLmsvzsDNYAOHC', '986256987', 'ABC', 45, 'www.abc.com', 'Abecedario, 36', 'Comida con todas las letras.', 'aquitulogo-27.webp');

-- --------------------------------------------------------
--
-- Estructura de tabla para la tabla `cuisine_type`
--

DROP TABLE IF EXISTS `cuisine_type`;
CREATE TABLE IF NOT EXISTS `cuisine_type` (
  `cuisine_id` int NOT NULL AUTO_INCREMENT,
  `cuisine_name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cuisine_id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cuisine_type`
--

INSERT INTO `cuisine_type` (`cuisine_id`, `cuisine_name`, `description`) VALUES
(1, 'Mediterránea', NULL),
(2, 'Italiana', NULL),
(3, 'Japonesa', NULL),
(4, 'Mexicana', NULL),
(5, 'China', NULL),
(6, 'India', NULL),
(7, 'Vegana', NULL),
(8, 'Americana', NULL),
(9, 'Española', NULL),
(10, 'Fusión', NULL),
(11, 'Internacional', NULL),
(12, 'Tailandesa', NULL),
(13, 'Árabe', NULL),
(14, 'Peruana', NULL),
(15, 'Local/Regional', NULL),
(16, 'Rápida', NULL),
(17, 'Saludable', NULL),
(18, 'Vegetariana', NULL),
(19, 'Orgánica', NULL),
(20, 'Casera', NULL),
(21, 'Gourmet', NULL),
(22, 'Parrilla', NULL),
(23, 'Mariscos', NULL),
(24, 'Postres', NULL),
(25, 'Sudamérica', NULL),
(26, 'Sin gluten', NULL),
(27, 'Sin lactosa', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservation`
--

DROP TABLE IF EXISTS `reservation`;
CREATE TABLE IF NOT EXISTS `reservation` (
  `reservation_id` int NOT NULL AUTO_INCREMENT,
  `client_id` int NOT NULL,
  `restaurant_id` int NOT NULL,
  `diners` int NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `status` enum('pendiente','confirmada','cancelada') COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`reservation_id`),
  KEY `client_id` (`client_id`),
  KEY `restaurant_id` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reservation`
--

INSERT INTO `reservation` (`reservation_id`, `client_id`, `restaurant_id`, `diners`, `date`, `time`, `status`) VALUES
(22, 18, 31, 2, '2025-03-17', '20:30:00', ''),
(23, 18, 31, 4, '2025-03-18', '13:00:00', ''),
(24, 18, 31, 6, '2025-03-26', '13:30:00', '');

-- --------------------------------------------------------

----
-- Estructura de tabla para la tabla `restaurant_cuisine`
--

DROP TABLE IF EXISTS `restaurant_cuisine`;
CREATE TABLE IF NOT EXISTS `restaurant_cuisine` (
  `restaurant_id` int NOT NULL,
  `cuisine_id` int NOT NULL,
  PRIMARY KEY (`restaurant_id`,`cuisine_id`),
  KEY `cuisine_id` (`cuisine_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `restaurant_cuisine`
--

INSERT INTO `restaurant_cuisine` (`restaurant_id`, `cuisine_id`) VALUES
(1, 1),
(1, 9),
(2, 4),
(2, 11),
(3, 8),
(3, 16),
(4, 2),
(4, 16),
(4, 26),
(5, 8),
(5, 16),
(6, 15),
(6, 16),
(7, 3),
(7, 10),
(7, 11),
(8, 2),
(8, 26),
(9, 11),
(9, 12),
(10, 22),
(11, 15),
(11, 22),
(12, 9),
(12, 15),
(12, 19),
(13, 7),
(13, 17),
(13, 18),
(14, 24),
(14, 26),
(14, 27),
(15, 9),
(15, 15),
(16, 1),
(16, 23),
(17, 8),
(17, 11),
(18, 5),
(19, 15),
(19, 22),
(20, 9),
(20, 15),
(20, 17),
(32, 9),
(32, 15),
(32, 20),
(32, 22);


--


-- Estructura de tabla para la tabla `reservation`
--

DROP TABLE IF EXISTS `reservation`;
CREATE TABLE IF NOT EXISTS `reservation` (
  `reservation_id` int NOT NULL AUTO_INCREMENT,
  `client_id` int NOT NULL,
  `restaurant_id` int NOT NULL,
  `diners` int NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `status` enum('pendiente','confirmada','cancelada') COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`reservation_id`),
  KEY `client_id` (`client_id`),
  KEY `restaurant_id` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

-- --------------------------------------------------------
--
-- Restricciones para tablas volcadas
--
-- Filtros para la tabla `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`),
  ADD CONSTRAINT `reservation_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`);
COMMIT;
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
