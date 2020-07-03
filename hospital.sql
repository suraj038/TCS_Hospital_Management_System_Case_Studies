-- phpMyAdmin SQL Dump
-- version 4.4.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jul 03, 2020 at 04:17 PM
-- Server version: 5.6.26
-- PHP Version: 5.6.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hospital`
--

-- --------------------------------------------------------

--
-- Table structure for table `diagnostics_master`
--

CREATE TABLE IF NOT EXISTS `diagnostics_master` (
  `TestID` int(9) NOT NULL,
  `TestName` varchar(25) NOT NULL,
  `Chargefortest` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `diagnostics_master`
--

INSERT INTO `diagnostics_master` (`TestID`, `TestName`, `Chargefortest`) VALUES
(300000001, 'CBP', 2000),
(300000002, 'Lipid', 1500),
(300000003, 'X-RAY', 2500);

-- --------------------------------------------------------

--
-- Table structure for table `medicine_master`
--

CREATE TABLE IF NOT EXISTS `medicine_master` (
  `MedicineID` int(9) NOT NULL,
  `MedicineName` varchar(25) NOT NULL,
  `QuantityAvailable` int(10) NOT NULL,
  `Rateofmedicine` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `medicine_master`
--

INSERT INTO `medicine_master` (`MedicineID`, `MedicineName`, `QuantityAvailable`, `Rateofmedicine`) VALUES
(200000001, 'Acebutolodo', 15, 55),
(200000002, 'Corgard', 25, 2000),
(200000003, 'Tenormin', 1, 100),
(200000004, 'Paracetamol', 30, 200),
(200000005, 'Dolo', 14, 150),
(200000006, 'coughsyrup', 45, 100);

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE IF NOT EXISTS `patients` (
  `PatientID` int(9) NOT NULL,
  `PatientName` char(20) NOT NULL,
  `Age` int(3) NOT NULL,
  `DateofAdmission` date NOT NULL,
  `Typeofbed` char(20) NOT NULL,
  `Address` varchar(80) NOT NULL,
  `City` varchar(25) NOT NULL,
  `State` varchar(25) NOT NULL,
  `Status` varchar(20) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=100000014 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`PatientID`, `PatientName`, `Age`, `DateofAdmission`, `Typeofbed`, `Address`, `City`, `State`, `Status`) VALUES
(100000001, 'suraj singh', 22, '2020-06-28', 'Single', 'Biet-Boys-Hostel', ' Candolim ', 'Goa', 'Active'),
(100000005, 'govind', 30, '2020-06-29', 'Shared', 'Near-Hospital_Road', 'Davangere', 'Karnataka', 'Discharged'),
(100000007, 'surya', 55, '2020-06-29', 'Shared', 'Anjaneya-Layout', ' Bayad ', 'Gujarat', 'Active'),
(100000008, 'carry bhai', 25, '2020-06-29', 'Single', 'SP ROAD Heblui', ' Aurangabad ', 'Bihar', 'Active'),
(100000010, 'rahul', 25, '2020-06-30', 'Shared', '1868/3,Swami-Vivekanada-Badavanes', ' Bettiah ', 'Bihar', 'Active'),
(100000013, 'saurab', 18, '2020-07-02', 'Single', 'ABC-happy-onam', ' Chainpur ', 'Jharkhand', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `tracking_diagnostics`
--

CREATE TABLE IF NOT EXISTS `tracking_diagnostics` (
  `PatientID` int(9) NOT NULL,
  `TestID` int(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tracking_diagnostics`
--

INSERT INTO `tracking_diagnostics` (`PatientID`, `TestID`) VALUES
(100000001, 300000001),
(100000005, 300000002),
(100000007, 300000001),
(100000008, 300000002),
(100000007, 300000002),
(100000005, 300000001),
(100000010, 300000002),
(100000010, 300000001),
(100000007, 300000003),
(100000001, 300000002),
(100000001, 300000002),
(100000001, 300000001),
(100000001, 300000001),
(100000001, 300000001),
(100000001, 300000001),
(100000001, 300000003),
(100000001, 300000001),
(100000001, 300000002),
(100000001, 300000003),
(100000013, 300000003);

-- --------------------------------------------------------

--
-- Table structure for table `tracking_medicines`
--

CREATE TABLE IF NOT EXISTS `tracking_medicines` (
  `PatientID` int(9) NOT NULL,
  `IDofMedicineIssued` int(9) NOT NULL,
  `QuantityIssued` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tracking_medicines`
--

INSERT INTO `tracking_medicines` (`PatientID`, `IDofMedicineIssued`, `QuantityIssued`) VALUES
(100000001, 200000001, 5),
(100000005, 200000002, 10),
(100000007, 200000003, 15),
(100000008, 200000004, 10),
(100000007, 200000003, 2),
(100000007, 200000003, 2),
(100000001, 200000001, 3),
(100000001, 200000001, 1),
(100000005, 200000002, 5),
(100000005, 200000003, 2),
(100000005, 200000003, 1),
(100000001, 200000003, 1),
(100000010, 200000005, 30),
(100000010, 200000003, 5),
(100000007, 200000001, 1),
(100000001, 200000005, 1),
(100000013, 200000005, 5);

-- --------------------------------------------------------

--
-- Table structure for table `userstore`
--

CREATE TABLE IF NOT EXISTS `userstore` (
  `username` varchar(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `userstore`
--

INSERT INTO `userstore` (`username`, `password`, `timestamp`) VALUES
('admin', 'admin', '2020-07-03 13:35:32');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `diagnostics_master`
--
ALTER TABLE `diagnostics_master`
  ADD PRIMARY KEY (`TestID`);

--
-- Indexes for table `medicine_master`
--
ALTER TABLE `medicine_master`
  ADD PRIMARY KEY (`MedicineID`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`PatientID`);

--
-- Indexes for table `tracking_diagnostics`
--
ALTER TABLE `tracking_diagnostics`
  ADD KEY `Patient ID` (`PatientID`),
  ADD KEY `Test ID` (`TestID`);

--
-- Indexes for table `tracking_medicines`
--
ALTER TABLE `tracking_medicines`
  ADD KEY `PatientID` (`PatientID`),
  ADD KEY `IDofMedicine Issued` (`IDofMedicineIssued`);

--
-- Indexes for table `userstore`
--
ALTER TABLE `userstore`
  ADD PRIMARY KEY (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `PatientID` int(9) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=100000014;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `tracking_diagnostics`
--
ALTER TABLE `tracking_diagnostics`
  ADD CONSTRAINT `tracking_diagnostics_ibfk_1` FOREIGN KEY (`PatientID`) REFERENCES `patients` (`PatientID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tracking_diagnostics_ibfk_2` FOREIGN KEY (`TestID`) REFERENCES `diagnostics_master` (`TestID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tracking_medicines`
--
ALTER TABLE `tracking_medicines`
  ADD CONSTRAINT `tracking_medicines_ibfk_1` FOREIGN KEY (`IDofMedicineIssued`) REFERENCES `medicine_master` (`MedicineID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tracking_medicines_ibfk_2` FOREIGN KEY (`PatientID`) REFERENCES `patients` (`PatientID`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
