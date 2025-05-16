-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: bbms
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `Admin_ID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(45) DEFAULT NULL,
  `Password` varchar(255) NOT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `Admin_Name` varchar(45) DEFAULT NULL,
  `BloodBank_ID` int DEFAULT NULL,
  `Created_At` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Last_Login` timestamp NULL DEFAULT NULL,
  `Is_Active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`Admin_ID`),
  UNIQUE KEY `Admin_ID_UNIQUE` (`Admin_ID`),
  KEY `BloodBank_ID_idx` (`BloodBank_ID`),
  CONSTRAINT `BloodBank_ID` FOREIGN KEY (`BloodBank_ID`) REFERENCES `blood_bank` (`BloodBank_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'adnan_swl','adnan1','adnan@email.com','Adnan Sohail',1,'2025-04-27 10:26:48',NULL,1),(2,'faisal_swl','faisal1','faisal@email.com','Faisal Bashir',2,'2025-04-27 10:26:48',NULL,1),(3,'sultan_lhr','sultan1','sultan@email.com','Sultan Ahmed',3,'2025-04-27 10:26:48',NULL,1),(4,'areeb_kar','areeb1','areeb@email.com','Areeb Asim',4,'2025-04-27 10:26:48',NULL,1),(5,'hamza_pes','hamza1','hamza@email.com','Hamza Ahad',5,'2025-04-27 10:26:48',NULL,1),(11,'aa1','ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f','aa1@gmail.com','Ali Asghar',3,'2025-04-27 10:41:42','2025-05-16 11:20:50',1);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blood_bank`
--

DROP TABLE IF EXISTS `blood_bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_bank` (
  `BloodBank_ID` int NOT NULL AUTO_INCREMENT,
  `BB_Name` varchar(45) DEFAULT NULL,
  `Location` varchar(45) DEFAULT NULL,
  `Capacity (BloodBags)` int DEFAULT NULL,
  `BB_Contact` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`BloodBank_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood_bank`
--

LOCK TABLES `blood_bank` WRITE;
/*!40000 ALTER TABLE `blood_bank` DISABLE KEYS */;
INSERT INTO `blood_bank` VALUES (1,'Alkidmat BB','Sahiwal',45,'+923219876543'),(2,'Alfaisal BB','Sahiwal',45,'+923211234567'),(3,'Lahore BB','Lahore',80,'+923229876543'),(4,'Memon BB','Karachi',160,'+923129876543'),(5,'Khan BB','Peshawar',45,'+923119876543');
/*!40000 ALTER TABLE `blood_bank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blood_component`
--

DROP TABLE IF EXISTS `blood_component`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_component` (
  `Component_ID` varchar(45) NOT NULL,
  `Blood_Type` varchar(45) DEFAULT NULL,
  `Component_Type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Component_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood_component`
--

LOCK TABLES `blood_component` WRITE;
/*!40000 ALTER TABLE `blood_component` DISABLE KEYS */;
INSERT INTO `blood_component` VALUES ('ABN_1','AB-','Plasma'),('ABN_2','AB-','Platelets'),('ABN_3','AB-','Red Blood Cells'),('ABN_4','AB-','Whole Blood'),('ABP_1','AB+','Plasma'),('ABP_2','AB+','Platelets'),('ABP_3','AB+','Red Blood Cells'),('ABP_4','AB+','Whole Blood'),('BP_!','B+','Plasma'),('BP_2','B+','Platelets'),('BP_3','B+','Red Blood Cells'),('BP_4','B+','Whole Blood'),('ON_1','O-','Plasma'),('ON_2','O-','Platelets'),('ON_3','O-','Red Blood Cells'),('ON_4','O-','Whole Blood'),('OP_1','O+','Plasma'),('OP_2','O+','Platelets'),('OP_3','O+','Red Blood Cells'),('OP_4','O+','Whole Blood');
/*!40000 ALTER TABLE `blood_component` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blood_donations`
--

DROP TABLE IF EXISTS `blood_donations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_donations` (
  `Donation_ID` int NOT NULL AUTO_INCREMENT,
  `Donor_ID` int DEFAULT NULL,
  `Donor_BloodType` varchar(45) DEFAULT NULL,
  `Quantity_Donated (BloodBags)` int DEFAULT NULL,
  `Donation_Date` varchar(45) DEFAULT NULL,
  `MedicalScreening_Result` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Donation_ID`),
  KEY `Donor_ID_idx` (`Donor_ID`),
  KEY `Donor_BloodType_idx` (`Donor_BloodType`),
  CONSTRAINT `Donor_ID` FOREIGN KEY (`Donor_ID`) REFERENCES `donor` (`Donor_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood_donations`
--

LOCK TABLES `blood_donations` WRITE;
/*!40000 ALTER TABLE `blood_donations` DISABLE KEYS */;
INSERT INTO `blood_donations` VALUES (1,9,'O+',20,'2024-04-25','Passed'),(2,2,'O-',3,'2024-01-20','Passed'),(3,8,'AB+',2,'2024-01-22','Passed'),(4,5,'AB-',5,'2024-02-25','Passed'),(5,7,'B+',6,'2024-07-15','Passed'),(6,4,'AB+',50,'2024-04-22','Failed');
/*!40000 ALTER TABLE `blood_donations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blood_test`
--

DROP TABLE IF EXISTS `blood_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_test` (
  `Test_ID` int NOT NULL AUTO_INCREMENT,
  `Donation_ID` int DEFAULT NULL,
  `Test_Type` varchar(45) DEFAULT NULL,
  `Test_Result` varchar(45) DEFAULT NULL,
  `Date_Conducted` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Test_ID`),
  KEY `Donation_ID_idx` (`Donation_ID`),
  CONSTRAINT `Donation_ID` FOREIGN KEY (`Donation_ID`) REFERENCES `blood_donations` (`Donation_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood_test`
--

LOCK TABLES `blood_test` WRITE;
/*!40000 ALTER TABLE `blood_test` DISABLE KEYS */;
INSERT INTO `blood_test` VALUES (1,6,'Blood Type Compatibility Test','Positive','2024-04-22'),(2,6,'Infectious Disease Screening','Positive','2024-04-22'),(3,6,'Crossmatching','Positive','2024-04-22'),(4,1,'Antibody Screening','Positive','2024-04-21'),(5,2,'Rhesus (Rh) Factor Test','Positive','2024-01-01');
/*!40000 ALTER TABLE `blood_test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blood_transfusion`
--

DROP TABLE IF EXISTS `blood_transfusion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_transfusion` (
  `Transfusion_ID` int NOT NULL AUTO_INCREMENT,
  `Receiver_ID` int DEFAULT NULL,
  `Blood_Type` varchar(45) DEFAULT NULL,
  `Transfusion_Date` varchar(45) DEFAULT NULL,
  `Inventory_ID` int DEFAULT NULL,
  `Quantity_Transfused` int DEFAULT NULL,
  PRIMARY KEY (`Transfusion_ID`),
  KEY `Receiver_ID_idx` (`Receiver_ID`),
  KEY `Inventory_ID_idx` (`Inventory_ID`),
  CONSTRAINT `Inventory_ID` FOREIGN KEY (`Inventory_ID`) REFERENCES `inventory` (`Inventory_ID`),
  CONSTRAINT `Receiver_ID` FOREIGN KEY (`Receiver_ID`) REFERENCES `receiver` (`Receriver_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood_transfusion`
--

LOCK TABLES `blood_transfusion` WRITE;
/*!40000 ALTER TABLE `blood_transfusion` DISABLE KEYS */;
INSERT INTO `blood_transfusion` VALUES (1,2,'O+','2024-04-20',1,2),(2,3,'O-','2024-04-22',2,1),(3,4,'AB-','2024-04-20',4,1),(4,5,'AB+','2024-04-22',3,1),(5,5,'AB+','2024-05-01',3,1),(6,5,'AB+','2024-05-02',3,15);
/*!40000 ALTER TABLE `blood_transfusion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donor`
--

DROP TABLE IF EXISTS `donor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donor` (
  `Donor_ID` int NOT NULL AUTO_INCREMENT,
  `Donor_Name` varchar(45) DEFAULT NULL,
  `Donor_BloodType` varchar(45) DEFAULT NULL,
  `Donor_Gender` varchar(45) DEFAULT NULL,
  `Donor_DOB` varchar(45) DEFAULT NULL,
  `Donor_Contact` varchar(45) DEFAULT NULL,
  `Donor_MedicalHistory` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Donor_ID`),
  UNIQUE KEY `Donor_ID_UNIQUE` (`Donor_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donor`
--

LOCK TABLES `donor` WRITE;
/*!40000 ALTER TABLE `donor` DISABLE KEYS */;
INSERT INTO `donor` VALUES (2,'Fahad Hassan','O-','Male','1990-03-25','+923339876543','No significant medical history'),(3,'Usman Khan','0+','Male','1982-11-10','+923001234567','No significant medical history'),(4,'Muhammad Ali','AB+','Male','1992-04-05','+923458765432','No significant medical history'),(5,'Hassan Ahmed','AB-','Male','1988-07-20','+923212345678','No significant medical history'),(6,'Fahad Mehmood','0+','Male','1989-08-12','+923331112233','Allergic to penicillin'),(7,'Nabeel Memon','B+','Male','1995-12-03','+923145556677','Allergic to penicillin'),(8,'Fahad Mustafa','AB+','Male','1987-05-10','+923449998877','No significant medical history'),(9,'Humayun Saeed','0+','Male','2024-04-01','+923223334455','No significant medical history'),(10,'Atif Aslam','O-','Male','2003-07-26','+92337778899','No significant medical history'),(11,'Micheal Jackson','0+','Male','1982-11-10','+923331112233','No significant medical history');
/*!40000 ALTER TABLE `donor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory` (
  `Inventory_ID` int NOT NULL AUTO_INCREMENT,
  `Quantity_Available (BloodBag)` int DEFAULT NULL,
  `Expiration_Date` varchar(45) DEFAULT NULL,
  `BloodBank_ID` int DEFAULT NULL,
  `Componnet_ID` varchar(45) DEFAULT NULL,
  `Donation_ID` int DEFAULT NULL,
  PRIMARY KEY (`Inventory_ID`),
  KEY `BloodBank_ID #1_idx` (`BloodBank_ID`),
  KEY `Component_ID #1_idx` (`Componnet_ID`),
  KEY `Donation_ID_idx` (`Donation_ID`),
  CONSTRAINT `BloodBank_ID #1` FOREIGN KEY (`BloodBank_ID`) REFERENCES `blood_bank` (`BloodBank_ID`),
  CONSTRAINT `Component_ID #1` FOREIGN KEY (`Componnet_ID`) REFERENCES `blood_component` (`Component_ID`),
  CONSTRAINT `Donation_ID #2` FOREIGN KEY (`Donation_ID`) REFERENCES `blood_donations` (`Donation_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,20,'2024-08-25',1,'OP_4',1),(2,3,'2024-04-20',1,'ON_4',2),(3,2,'2024-04-22',1,'ABP_4',3),(4,5,'2024-06-25',2,'ABN_4',4),(5,6,'2024-11-15',3,'BP_4',5),(6,50,'2024-08-22',4,'ABP_1',6);
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receiver`
--

DROP TABLE IF EXISTS `receiver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receiver` (
  `Receriver_ID` int NOT NULL AUTO_INCREMENT,
  `Receiver_Name` varchar(45) DEFAULT NULL,
  `Receiver_BloodType` varchar(45) DEFAULT NULL,
  `Receiver_Gender` varchar(45) DEFAULT NULL,
  `Receiver_DOB` varchar(45) DEFAULT NULL,
  `Receiver_Contact` varchar(45) DEFAULT NULL,
  `Receiver_MedicalCondition` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Receriver_ID`),
  UNIQUE KEY `Receriver_ID_UNIQUE` (`Receriver_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receiver`
--

LOCK TABLES `receiver` WRITE;
/*!40000 ALTER TABLE `receiver` DISABLE KEYS */;
INSERT INTO `receiver` VALUES (1,' Muhammad Ali','AB+','Male','1980-08-25','+923123456789','Anemia'),(2,'Fatima Malik','O+','Female','1995-03-12','+913123456789','Sickle cell disease'),(3,'Sana Ali','O-','Female','1980-01-02','+923037778899','Hypertension'),(4,'Hina Ahmed','AB-','Female','1995-03-09','+923145556677','Diabetes Mellitus'),(5,'Mahira Khan','AB+','Female','1980-08-25','+923001234567','Asthma');
/*!40000 ALTER TABLE `receiver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `Staff_ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Role` varchar(45) DEFAULT NULL,
  `Contact` varchar(45) DEFAULT NULL,
  `Schedule` varchar(45) DEFAULT NULL,
  `BloodBank_ID` int DEFAULT NULL,
  PRIMARY KEY (`Staff_ID`),
  KEY `BloodBank_ID #2_idx` (`BloodBank_ID`),
  CONSTRAINT `BloodBank_ID #2` FOREIGN KEY (`BloodBank_ID`) REFERENCES `blood_bank` (`BloodBank_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'Sara Khan ','Nurses','+923007007007','Mon-Fri, 9am-5pm',1),(2,'Ali Khan','Medical Technologists','+923306306306','Mon-Fri, 9am-5pm',1),(3,'Ayesha Malik','Hematologists','+923154154154','Tue-Sat, 10am-6pm',1),(4,'Aisha Ali','Nurses','+923310101010','Mon-Fri, 9am-5pm',2),(5,'Farhan Ahmed','Medical Technologists','+923355555555','Mon-Fri, 9am-5pm',2),(6,'Arslan Ahmed','Hematologists','+923355555555','Mon-Fri, 9am-5pm',2),(7,'Zara Malik ','Nurses','+923388888888','Mon-Fri, 9am-5pm',3),(8,'Amir Malik','Medical Technologists','+923300300300','Mon-Fri, 9am-5pm',3),(9,'Arslan Ahmed','Hematologists','+923393939393','Tue-Sat, 10am-6pm',3),(10,'Hira Ahmed','Nurses','+923366366366','Mon-Fri, 9am-5pm',4),(11,'Saad Khan','Medical Technologists','+923377377377','Mon-Fri, 9am-5pm',4),(12,'Saba Ali ','Hematologists','+923121212121','Tue-Sat, 10am-6pm',4),(13,'Mahnoor Khan','Nurses','+923323232323','Mon-Fri, 9am-5pm',5),(14,'Bilal Mahmood','Medical Technologists','+923214141414','Mon-Fri, 9am-5pm',5),(15,'Nida Khan','Hematologists','+923332244668','Mon-Fri, 9am-5pm',5);
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-16 16:43:10
