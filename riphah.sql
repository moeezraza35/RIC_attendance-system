-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 20, 2024 at 08:00 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `riphah`
--
CREATE DATABASE IF NOT EXISTS `riphah` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `riphah`;

-- --------------------------------------------------------

--
-- Table structure for table `lectures`
--

CREATE TABLE `lectures` (
  `id` int(11) NOT NULL,
  `subject` text NOT NULL,
  `section` int(11) NOT NULL,
  `staff` int(11) NOT NULL,
  `day` tinytext NOT NULL,
  `period` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `lecture_attendance`
--

CREATE TABLE `lecture_attendance` (
  `sr` int(11) NOT NULL,
  `lecture` int(11) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `id` int(11) NOT NULL,
  `name` tinytext DEFAULT NULL,
  `attendance` tinyint(1) DEFAULT NULL,
  `examination` tinyint(1) DEFAULT NULL,
  `management` tinyint(1) DEFAULT NULL,
  `privileges` tinyint(1) DEFAULT NULL,
  `staff` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sections`
--

CREATE TABLE `sections` (
  `id` int(11) NOT NULL,
  `name` tinytext DEFAULT NULL,
  `fall` tinytext DEFAULT NULL,
  `program` tinytext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `id` int(11) NOT NULL,
  `name` tinytext DEFAULT NULL,
  `password` tinytext DEFAULT NULL,
  `post` int(11) DEFAULT NULL,
  `status` tinytext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `staff_absence`
--

CREATE TABLE `staff_absence` (
  `sr` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `request` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `staff_attendance`
--

CREATE TABLE `staff_attendance` (
  `sr` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `time_in` time DEFAULT NULL,
  `time_out` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `sr` int(11) NOT NULL,
  `id` varchar(4) NOT NULL,
  `name` tinytext DEFAULT NULL,
  `father` tinytext DEFAULT NULL,
  `section` tinytext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `student_attendance`
--

CREATE TABLE `student_attendance` (
  `sr` int(11) NOT NULL,
  `lecture` int(11) NOT NULL,
  `student` int(11) NOT NULL,
  `attended` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `visiting_record`
--

CREATE TABLE `visiting_record` (
  `sr` int(11) NOT NULL,
  `program` int(11) DEFAULT NULL,
  `subject` tinytext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `lectures`
--
ALTER TABLE `lectures`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `lecture_attendance`
--
ALTER TABLE `lecture_attendance`
  ADD PRIMARY KEY (`sr`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sections`
--
ALTER TABLE `sections`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `staff_absence`
--
ALTER TABLE `staff_absence`
  ADD PRIMARY KEY (`sr`);

--
-- Indexes for table `staff_attendance`
--
ALTER TABLE `staff_attendance`
  ADD PRIMARY KEY (`sr`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`sr`);

--
-- Indexes for table `student_attendance`
--
ALTER TABLE `student_attendance`
  ADD PRIMARY KEY (`sr`);

--
-- Indexes for table `visiting_record`
--
ALTER TABLE `visiting_record`
  ADD PRIMARY KEY (`sr`);
COMMIT;