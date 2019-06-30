-- MySQL dump 10.13  Distrib 8.0.16, for osx10.13 (x86_64)
--
-- Host: localhost    Database: water_quality_ng
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `water_quality_ng`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `water_quality_ng` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `water_quality_ng`;

--
-- Table structure for table `contaminant`
--

DROP TABLE IF EXISTS `contaminant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `contaminant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_general_ci NOT NULL,
  `description` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `default_strength` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contaminant`
--

LOCK TABLES `contaminant` WRITE;
/*!40000 ALTER TABLE `contaminant` DISABLE KEYS */;
INSERT INTO `contaminant` VALUES (1,'chloroform','CHCl3',0.001),(2,'bromoform','CHBr3',0.001),(3,'bromodichloromethane','CHBrCl2',0.001),(4,'dibromichloromethane','CHBr2Cl also',0.001);
/*!40000 ALTER TABLE `contaminant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `factor`
--

DROP TABLE IF EXISTS `factor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `factor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `factor`
--

LOCK TABLES `factor` WRITE;
/*!40000 ALTER TABLE `factor` DISABLE KEYS */;
INSERT INTO `factor` VALUES (1,'New filtration factor 1');
/*!40000 ALTER TABLE `factor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `factor_contaminant_strength`
--

DROP TABLE IF EXISTS `factor_contaminant_strength`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `factor_contaminant_strength` (
  `factor_id` int(11) NOT NULL,
  `contaminant_id` int(11) NOT NULL,
  `strength` float NOT NULL,
  PRIMARY KEY (`factor_id`,`contaminant_id`),
  KEY `contaminant_id` (`contaminant_id`),
  CONSTRAINT `factor_contaminant_strength_ibfk_1` FOREIGN KEY (`factor_id`) REFERENCES `factor` (`id`),
  CONSTRAINT `factor_contaminant_strength_ibfk_2` FOREIGN KEY (`contaminant_id`) REFERENCES `contaminant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `factor_contaminant_strength`
--

LOCK TABLES `factor_contaminant_strength` WRITE;
/*!40000 ALTER TABLE `factor_contaminant_strength` DISABLE KEYS */;
INSERT INTO `factor_contaminant_strength` VALUES (1,1,0.8),(1,2,1.2),(1,3,1.5),(1,4,0.7);
/*!40000 ALTER TABLE `factor_contaminant_strength` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sample`
--

DROP TABLE IF EXISTS `sample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `sample` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site` varchar(80) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `site` (`site`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sample`
--

LOCK TABLES `sample` WRITE;
/*!40000 ALTER TABLE `sample` DISABLE KEYS */;
INSERT INTO `sample` VALUES (1,'LA Aquaduct Filteration Plant Effluent');
/*!40000 ALTER TABLE `sample` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sample_contaminant_concentration`
--

DROP TABLE IF EXISTS `sample_contaminant_concentration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `sample_contaminant_concentration` (
  `sample_id` int(11) NOT NULL,
  `contaminant_id` int(11) NOT NULL,
  `concentration` float NOT NULL,
  PRIMARY KEY (`sample_id`,`contaminant_id`),
  KEY `contaminant_id` (`contaminant_id`),
  CONSTRAINT `sample_contaminant_concentration_ibfk_1` FOREIGN KEY (`sample_id`) REFERENCES `sample` (`id`),
  CONSTRAINT `sample_contaminant_concentration_ibfk_2` FOREIGN KEY (`contaminant_id`) REFERENCES `contaminant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sample_contaminant_concentration`
--

LOCK TABLES `sample_contaminant_concentration` WRITE;
/*!40000 ALTER TABLE `sample_contaminant_concentration` DISABLE KEYS */;
INSERT INTO `sample_contaminant_concentration` VALUES (1,1,0.00104),(1,2,0),(1,3,0.00149),(1,4,0.00275);
/*!40000 ALTER TABLE `sample_contaminant_concentration` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-29 21:29:15
