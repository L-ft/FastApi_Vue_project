-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: autotest
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `api_group`
--

DROP TABLE IF EXISTS `api_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_group`
--

LOCK TABLES `api_group` WRITE;
/*!40000 ALTER TABLE `api_group` DISABLE KEYS */;
INSERT INTO `api_group` VALUES (1,'H5璁よ瘉鎺ュ彛'),(5,'your_group_name'),(6,'榛樿鍒嗙粍');
/*!40000 ALTER TABLE `api_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_info`
--

DROP TABLE IF EXISTS `api_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `url` varchar(255) NOT NULL,
  `method` varchar(10) NOT NULL,
  `group_id` int DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `env_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id` (`group_id`),
  KEY `fk_env` (`env_id`),
  CONSTRAINT `api_info_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `api_group` (`id`),
  CONSTRAINT `fk_env` FOREIGN KEY (`env_id`) REFERENCES `environment_variables` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_info`
--

LOCK TABLES `api_info` WRITE;
/*!40000 ALTER TABLE `api_info` DISABLE KEYS */;
INSERT INTO `api_info` VALUES (2,'H5璁よ瘉','/auth/oauth/token','POST',1,'娴嬭瘯2323432',2),(3,'娴嬭瘯','娴嬭瘯','娴嬭瘯222',1,'娴嬭瘯232344',2);
/*!40000 ALTER TABLE `api_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `case_info`
--

DROP TABLE IF EXISTS `case_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `case_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `group_id` int DEFAULT NULL,
  `api_id` int DEFAULT NULL,
  `request_data` varchar(255) DEFAULT NULL,
  `request_header` varchar(255) DEFAULT NULL,
  `request_method` varchar(10) DEFAULT NULL,
  `request_url` varchar(255) DEFAULT NULL,
  `response_data` varchar(255) DEFAULT NULL,
  `response_header` varchar(255) DEFAULT NULL,
  `response_status` varchar(10) DEFAULT NULL,
  `creator` varchar(100) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `modifier` varchar(100) DEFAULT NULL,
  `modify_time` datetime DEFAULT NULL,
  `params` varchar(1000) DEFAULT NULL,
  `headers` varchar(1000) DEFAULT NULL,
  `body` varchar(2000) DEFAULT NULL,
  `expected_status` int DEFAULT NULL,
  `expected_response` varchar(2000) DEFAULT NULL,
  `method` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id` (`group_id`),
  KEY `api_id` (`api_id`),
  CONSTRAINT `case_info_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `api_group` (`id`),
  CONSTRAINT `case_info_ibfk_2` FOREIGN KEY (`api_id`) REFERENCES `api_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `case_info`
--

LOCK TABLES `case_info` WRITE;
/*!40000 ALTER TABLE `case_info` DISABLE KEYS */;
INSERT INTO `case_info` VALUES (7,'H5璁よ瘉','娴嬭瘯2323432',1,2,NULL,NULL,NULL,'https://zmp-test1.nbm2m.com/api/auth/oauth/token',NULL,NULL,NULL,NULL,'2025-07-18 10:15:56',NULL,'2025-07-18 10:15:56','{\"cIdentity\": \"WWSB11132\", \"grant_type\": \"device\", \"client_id\": \"zmp-h5\", \"client_secret\": \"VIlA38m0G2YwGagS\", \"path\": \"https%3A%2F%2Fzmp-test1.nbm2m.com\"}',NULL,NULL,200,'{}','POST');
/*!40000 ALTER TABLE `case_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `environment_variables`
--

DROP TABLE IF EXISTS `environment_variables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `environment_variables` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `environment_variables`
--

LOCK TABLES `environment_variables` WRITE;
/*!40000 ALTER TABLE `environment_variables` DISABLE KEYS */;
INSERT INTO `environment_variables` VALUES (2,'娴嬭瘯','https://zmp-test1.nbm2m.com/api');
/*!40000 ALTER TABLE `environment_variables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `environments`
--

DROP TABLE IF EXISTS `environments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `environments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `value` varchar(500) NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_environments_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `environments`
--

LOCK TABLES `environments` WRITE;
/*!40000 ALTER TABLE `environments` DISABLE KEYS */;
/*!40000 ALTER TABLE `environments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','tester','developer','guest') DEFAULT 'tester',
  `avatar` varchar(255) DEFAULT NULL,
  `status` enum('active','inactive','locked') DEFAULT 'active',
  `lastLogin` datetime DEFAULT NULL,
  `createdAt` datetime DEFAULT NULL,
  `updatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'娴嬭瘯鐢ㄦ埛','test@example.com','simple_hash_password123','tester',NULL,'active','2025-05-16 05:51:17','2025-05-16 05:51:17','2025-05-16 05:51:17'),(2,'娴嬭瘯鐢ㄦ埛41','test195@example.com','simple_hash_password123','tester',NULL,'active','2025-05-16 05:53:19','2025-05-16 05:53:19','2025-05-16 05:53:19'),(3,'liuhaha',NULL,'1111','tester',NULL,'active',NULL,NULL,NULL),(4,'hahaliu',NULL,'1111','tester',NULL,'active',NULL,NULL,NULL),(5,'2liuhah',NULL,'$2b$12$UR6sc.Wtf9eM5CWvau8JwO1T2iUrrw0fY/wETQccpH614zrv040mG','tester',NULL,'active',NULL,NULL,NULL),(6,'22',NULL,'$2b$12$RBtaZbbwJtjknP2Pv/Cj1ekcAZBhSnOFtOw8O82PkzsnZTTvLn9b.','tester',NULL,'active',NULL,NULL,NULL),(7,'jaj',NULL,'$2b$12$oSaljZzorYwvbbRhyyTjGOlt0fgwnSI3dzioKFdSPzXbOi6vOZdEq','tester',NULL,'active',NULL,NULL,NULL),(8,'12',NULL,'$2b$12$HYE97AWOXz9TbKukkJms8.xi2YeNcS3/0p3k9EMcOXYGoUTSxHRHm','tester',NULL,'active',NULL,NULL,NULL),(9,'1212',NULL,'$2b$12$Sc7YCWE4AhsNGOXq9n4PY.GRh3Gx9fcQe0KUxVphsb5z/MrknAR8a','tester',NULL,'active',NULL,NULL,NULL),(10,'testuser',NULL,'$2b$12$5eN4msGJkRkO698dsowy8uBvMba3kW17hwGfYSr4OuPXGcWPRj.xy','tester',NULL,'active',NULL,NULL,NULL),(11,'12334',NULL,'$2b$12$FZUoN0oG6BeqVO1DyRkDT.nOT6pDnt37eLsIYAi7sKYJvbXhgU2gC','tester',NULL,'active',NULL,NULL,NULL),(12,'admin',NULL,'$2b$12$55lMnQ5t60WtnTGlQA79/u3OKDwvXqFK/Fd/ZtA6ylQfp1LAn57/q','tester',NULL,'active',NULL,NULL,NULL),(13,'admin1',NULL,'$2b$12$bRPJ976YqemsAptYHPasR.oz4usdVZ4GdgoSvT8PLhmEsyBd82Mb.','tester',NULL,'active',NULL,NULL,NULL),(14,'1212121212',NULL,'$2b$12$kNqKYPttmqYAJ4t3q3Zzbela6rmp5hiwRjUM2D6CFe0xOUNva/P3W','tester',NULL,'active',NULL,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-18 16:52:20
