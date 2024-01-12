-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 06, 2023 at 04:10 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `review`
--

-- --------------------------------------------------------

--
-- Table structure for table `hasil_model`
--

CREATE TABLE `hasil_model` (
  `id_hasil_model` int(11) NOT NULL,
  `id_review` int(11) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `tanggal` date NOT NULL,
  `review` varchar(255) NOT NULL,
  `label` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hasil_model`
--

INSERT INTO `hasil_model` (`id_hasil_model`, `id_review`, `nama`, `tanggal`, `review`, `label`) VALUES
(13, 13, 'User1', '2023-12-04', 'Aplikasi ini sangat membantu dan mudah digunakan.', 1),
(14, 14, 'User2', '2023-12-04', 'Website ini memberikan pengalaman yang luar biasa.', 1),
(15, 15, 'User3', '2023-12-04', 'Saya sangat puas dengan fitur-fitur yang disediakan.', 1),
(16, 16, 'User4', '2023-12-04', 'Layanan pelanggan yang ramah dan responsif.', 1),
(17, 17, 'User5', '2023-12-04', 'Aplikasi ini membuat hidup saya lebih mudah dan efisien.', 1),
(18, 18, 'User6', '2023-12-04', 'Banyak bug pada aplikasi, membuat pengalaman buruk.', 0),
(19, 19, 'User7', '2023-12-04', 'Navigasi website sangat membingungkan dan lambat.', 0),
(20, 20, 'User8', '2023-12-04', 'Fitur-fitur yang ditawarkan kurang memuaskan.', 0),
(21, 21, 'User9', '2023-12-04', 'Aplikasi sering crash dan tidak stabil.', 0),
(22, 22, 'User10', '2023-12-04', 'Pelayanan pelanggan sangat buruk dan tidak responsif.', 0),
(23, 23, 'User11', '2023-12-04', 'Saya merasa biasa saja dengan aplikasi ini.', -1),
(24, 24, 'User12', '2023-12-04', 'Website ini memiliki kelebihan dan kekurangan masing-masing.', -1),
(25, 25, 'User13', '2023-12-04', 'Tidak terlalu terkesan dengan fitur-fitur yang disediakan.', -1),
(26, 26, 'User14', '2023-12-04', 'Penggunaan aplikasi ini standar saja.', -1),
(27, 27, 'User15', '2023-12-04', 'Tidak ada yang istimewa dari website ini.', -1),
(28, 28, 'User16', '2023-12-05', 'Aplikasi ini Sangat Berguna dan sangat responsif', -1);

-- --------------------------------------------------------

--
-- Table structure for table `input_review`
--

CREATE TABLE `input_review` (
  `id_review` int(11) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `tanggal` date NOT NULL,
  `review` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `hasil_model`
--
ALTER TABLE `hasil_model`
  ADD PRIMARY KEY (`id_hasil_model`);

--
-- Indexes for table `input_review`
--
ALTER TABLE `input_review`
  ADD PRIMARY KEY (`id_review`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `hasil_model`
--
ALTER TABLE `hasil_model`
  MODIFY `id_hasil_model` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `input_review`
--
ALTER TABLE `input_review`
  MODIFY `id_review` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
