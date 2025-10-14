-- MySQL dump 10.13  Distrib 9.4.0, for macos14.7 (x86_64)
--
-- Host: 127.0.0.1    Database: CAN_DB
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `assorbimenti`
--

DROP TABLE IF EXISTS `assorbimenti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assorbimenti` (
  `id_regione` int NOT NULL,
  `punti_forza` text,
  `aree_miglioramento` text,
  PRIMARY KEY (`id_regione`),
  CONSTRAINT `assorbimenti_ibfk_1` FOREIGN KEY (`id_regione`) REFERENCES `regioni` (`id_regione`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assorbimenti`
--

LOCK TABLES `assorbimenti` WRITE;
/*!40000 ALTER TABLE `assorbimenti` DISABLE KEYS */;
INSERT INTO `assorbimenti` VALUES (1,'Emissioni pro capite tra le più basse d’Italia (3,3 t)','Assorbimenti naturali inferiori alla media'),(2,'Elevata elettrificazione degli edifici (29%)','Emissioni pro capite elevate'),(3,'Basse emissioni pro capite','Assorbimenti naturali da migliorare'),(4,'Elevati assorbimenti naturali','Emissioni pro capite elevate'),(5,'Elevati assorbimenti naturali','Emissioni pro capite elevate'),(6,'Basse emissioni pro capite (5,11 t)','Assorbimenti naturali da migliorare'),(7,'Elevati assorbimenti naturali (215 t CO₂/km²)','Emissioni pro capite superiori alla media'),(8,'Buona performance sulle rinnovabili','Emissioni pro capite elevate, soprattutto nel settore industriale'),(9,'Performance industriale positiva','Emissioni pro capite superiori alla media'),(10,NULL,NULL),(11,'Elevati assorbimenti naturali','Emissioni pro capite elevate'),(12,'Emissioni pro capite inferiori alla media nazionale','Assorbimenti forestali da migliorare'),(13,'Basse emissioni pro capite','Assorbimenti naturali inferiori alla media'),(14,'Seconda per assorbimenti naturali (215 t CO₂/km²)','Emissioni pro capite elevate'),(15,'Assorbimenti naturali elevati','Emissioni pro capite elevate'),(16,'Assorbimenti naturali elevati (324 t CO₂/km²)','Emissioni pro capite elevate'),(17,'Emissioni pro capite allineate alla media nazionale','Assorbimenti naturali da migliorare'),(18,'Buone performance sulle emissioni pro capite','Assorbimenti naturali da migliorare'),(19,NULL,NULL),(20,'Emissioni pro capite inferiori alla media nazionale','Assorbimenti naturali da migliorare');
/*!40000 ALTER TABLE `assorbimenti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `azioni`
--

DROP TABLE IF EXISTS `azioni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `azioni` (
  `id_regione` int NOT NULL,
  `fotovoltaico_capacita_gw` decimal(10,3) DEFAULT NULL,
  `quota_produzione_fer_pct` decimal(5,2) DEFAULT NULL,
  `quota_auto_elettriche_pct` decimal(5,2) DEFAULT NULL,
  `risparmi_energetici_mtep_mln` decimal(10,3) DEFAULT NULL,
  PRIMARY KEY (`id_regione`),
  CONSTRAINT `azioni_ibfk_1` FOREIGN KEY (`id_regione`) REFERENCES `regioni` (`id_regione`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `azioni`
--

LOCK TABLES `azioni` WRITE;
/*!40000 ALTER TABLE `azioni` DISABLE KEYS */;
INSERT INTO `azioni` VALUES (1,1.800,6.00,1.00,0.220),(2,2.250,6.00,2.50,0.290),(3,0.600,1.00,0.70,0.030),(4,0.700,2.00,0.20,0.040),(5,NULL,2.00,0.40,0.060),(6,1.600,5.00,2.20,0.250),(7,1.750,8.00,0.80,0.450),(8,3.060,11.00,0.90,0.210),(9,2.000,4.00,1.70,0.300),(10,3.150,14.00,2.00,0.960),(11,1.100,2.00,0.30,0.040),(12,1.200,3.00,0.50,0.080),(13,0.900,3.00,1.20,0.090),(14,1.500,5.00,1.80,0.250),(15,0.500,1.00,0.10,0.020),(16,NULL,NULL,1.30,NULL),(17,NULL,NULL,3.00,NULL),(18,0.800,2.00,NULL,0.070),(19,1.000,3.00,1.50,0.100),(20,1.850,7.00,0.60,0.140);
/*!40000 ALTER TABLE `azioni` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `edifici`
--

DROP TABLE IF EXISTS `edifici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `edifici` (
  `id_regione` int NOT NULL,
  `consumo_medio_kwh_m2y` decimal(12,2) DEFAULT NULL,
  `emissioni_procapite_tco2_ab` decimal(12,3) DEFAULT NULL,
  `quota_elettrico_pct` decimal(5,2) DEFAULT NULL,
  `quota_ape_classe_a_pct` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_regione`),
  CONSTRAINT `edifici_ibfk_1` FOREIGN KEY (`id_regione`) REFERENCES `regioni` (`id_regione`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `edifici`
--

LOCK TABLES `edifici` WRITE;
/*!40000 ALTER TABLE `edifici` DISABLE KEYS */;
INSERT INTO `edifici` VALUES (1,100.00,0.550,17.20,4.00),(2,130.00,0.470,21.40,10.00),(3,60.00,0.640,11.60,1.00),(4,70.00,0.620,13.00,1.00),(5,75.00,0.610,13.70,1.00),(6,115.00,0.500,19.30,6.00),(7,145.00,0.560,25.50,20.00),(8,95.00,0.570,16.50,3.00),(9,135.00,0.520,22.10,9.00),(10,140.00,NULL,23.80,15.00),(11,65.00,0.630,12.30,1.00),(12,85.00,0.580,15.10,1.00),(13,105.00,0.540,17.90,5.00),(14,125.00,0.480,20.70,7.00),(15,55.00,0.650,10.90,1.00),(16,110.00,0.450,18.60,8.00),(17,NULL,NULL,NULL,15.00),(18,80.00,0.600,14.40,1.00),(19,120.00,0.530,20.00,12.00),(20,90.00,0.590,15.80,2.00);
/*!40000 ALTER TABLE `edifici` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emissioni_totali`
--

DROP TABLE IF EXISTS `emissioni_totali`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emissioni_totali` (
  `id_regione` int NOT NULL,
  `co2eq_mln_t` decimal(12,3) DEFAULT NULL,
  PRIMARY KEY (`id_regione`),
  CONSTRAINT `emissioni_totali_ibfk_1` FOREIGN KEY (`id_regione`) REFERENCES `regioni` (`id_regione`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emissioni_totali`
--

LOCK TABLES `emissioni_totali` WRITE;
/*!40000 ALTER TABLE `emissioni_totali` DISABLE KEYS */;
INSERT INTO `emissioni_totali` VALUES (1,20.300),(2,35.700),(3,3.500),(4,1.600),(5,4.300),(6,26.100),(7,27.600),(8,16.500),(9,27.300),(10,65.300),(11,4.800),(12,7.900),(13,5.600),(14,16.900),(15,1.000),(16,4.900),(17,3.700),(18,6.200),(19,6.300),(20,14.900);
/*!40000 ALTER TABLE `emissioni_totali` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `industria`
--

DROP TABLE IF EXISTS `industria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `industria` (
  `id_regione` int NOT NULL,
  `emissioni_per_valore_aggiunto_tco2_per_mln_eur` decimal(12,4) DEFAULT NULL,
  `quota_elettrico_pct` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_regione`),
  CONSTRAINT `industria_ibfk_1` FOREIGN KEY (`id_regione`) REFERENCES `regioni` (`id_regione`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `industria`
--

LOCK TABLES `industria` WRITE;
/*!40000 ALTER TABLE `industria` DISABLE KEYS */;
INSERT INTO `industria` VALUES (1,0.2100,34.20),(2,0.3000,42.50),(3,0.1300,28.90),(4,0.1500,30.20),(5,0.1600,30.80),(6,0.2400,35.90),(7,0.3500,41.00),(8,0.2000,33.60),(9,0.2800,41.70),(10,0.3200,43.80),(11,0.1400,29.60),(12,0.1800,32.10),(13,0.2200,36.50),(14,0.2700,38.80),(15,0.1200,28.30),(16,0.2300,37.20),(17,NULL,39.50),(18,0.1700,31.50),(19,0.2500,45.20),(20,0.1900,32.90);
/*!40000 ALTER TABLE `industria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mix_energetico`
--

DROP TABLE IF EXISTS `mix_energetico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mix_energetico` (
  `id_regione` int NOT NULL,
  `carbone_pct` decimal(5,2) DEFAULT NULL,
  `petrolio_pct` decimal(5,2) DEFAULT NULL,
  `gas_pct` decimal(5,2) DEFAULT NULL,
  `rinnovabili_pct` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_regione`),
  CONSTRAINT `mix_energetico_ibfk_1` FOREIGN KEY (`id_regione`) REFERENCES `regioni` (`id_regione`),
  CONSTRAINT `chk_mix_somma_~100` CHECK (((((`carbone_pct` + `petrolio_pct`) + `gas_pct`) + `rinnovabili_pct`) between 99.0 and 101.0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mix_energetico`
--

LOCK TABLES `mix_energetico` WRITE;
/*!40000 ALTER TABLE `mix_energetico` DISABLE KEYS */;
INSERT INTO `mix_energetico` VALUES (1,0.00,48.00,29.00,22.00),(2,0.00,30.00,56.00,14.00),(3,0.00,38.00,37.00,24.00),(4,0.00,35.00,37.00,28.00),(5,0.00,41.00,21.00,38.00),(6,15.00,43.00,28.00,14.00),(7,0.00,28.00,55.00,17.00),(8,29.00,28.00,30.00,13.00),(9,7.00,37.00,37.00,19.00),(10,0.00,27.00,58.00,15.00),(11,18.00,68.00,0.00,14.00),(12,0.00,31.00,41.00,28.00),(13,0.00,47.00,35.00,19.00),(14,0.00,24.00,28.00,49.00),(15,0.00,27.00,18.00,55.00),(16,3.00,40.00,48.00,9.00),(17,0.00,34.00,26.00,40.00),(18,0.00,32.00,47.00,21.00),(19,7.00,19.00,53.00,20.00),(20,0.00,70.00,21.00,9.00);
/*!40000 ALTER TABLE `mix_energetico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `morfologia_suolo`
--

DROP TABLE IF EXISTS `morfologia_suolo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `morfologia_suolo` (
  `id_regione` int NOT NULL,
  `pianura_pct` decimal(5,2) DEFAULT NULL,
  `collina_pct` decimal(5,2) DEFAULT NULL,
  `montagna_pct` decimal(5,2) DEFAULT NULL,
  `urbano_pct` decimal(5,2) DEFAULT NULL,
  `agricolo_pct` decimal(5,2) DEFAULT NULL,
  `forestale_pct` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`id_regione`),
  CONSTRAINT `morfologia_suolo_ibfk_1` FOREIGN KEY (`id_regione`) REFERENCES `regioni` (`id_regione`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `morfologia_suolo`
--

LOCK TABLES `morfologia_suolo` WRITE;
/*!40000 ALTER TABLE `morfologia_suolo` DISABLE KEYS */;
INSERT INTO `morfologia_suolo` VALUES (1,2.90,5.50,4.40,10.00,50.00,30.00),(2,15.10,4.80,5.20,10.00,45.00,30.00),(3,0.00,4.80,2.30,10.00,50.00,35.00),(4,0.00,1.60,2.30,10.00,50.00,35.00),(5,1.20,3.60,4.40,5.00,50.00,35.00),(6,4.90,7.40,4.20,10.00,40.00,35.00),(7,9.60,6.10,10.40,10.00,35.00,40.00),(8,14.80,7.00,0.30,5.00,60.00,25.00),(9,14.90,2.10,5.10,10.00,45.00,30.00),(10,16.10,2.40,9.10,10.00,40.00,30.00),(11,6.40,13.00,3.10,5.00,50.00,35.00),(12,1.90,5.90,5.90,5.00,50.00,35.00),(13,0.00,5.30,2.80,10.00,50.00,35.00),(14,2.80,12.20,5.40,10.00,45.00,35.00),(15,0.00,0.00,3.10,10.00,45.00,40.00),(16,0.00,1.50,3.30,10.00,45.00,40.00),(17,0.00,0.00,12.80,10.00,45.00,40.00),(18,0.00,3.00,6.60,10.00,45.00,40.00),(19,4.30,1.20,3.10,10.00,45.00,35.00),(20,5.20,12.60,5.90,5.00,50.00,35.00);
/*!40000 ALTER TABLE `morfologia_suolo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `regioni`
--

DROP TABLE IF EXISTS `regioni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `regioni` (
  `id_regione` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(80) NOT NULL,
  `superficie_kmq` decimal(12,2) DEFAULT NULL,
  `densita_demografica` decimal(12,2) DEFAULT NULL,
  `pil` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`id_regione`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regioni`
--

LOCK TABLES `regioni` WRITE;
/*!40000 ALTER TABLE `regioni` DISABLE KEYS */;
INSERT INTO `regioni` VALUES (1,'Campania',13667.85,408.00,23.20),(2,'Emilia-Romagna',22501.82,198.00,43.30),(3,'Umbria',8463.97,101.00,30.50),(4,'Molise',4459.80,65.00,33.20),(5,'Basilicata',10071.59,53.00,27.50),(6,'Lazio',17236.49,331.00,36.10),(7,'Piemonte',25391.67,168.00,26.70),(8,'Puglia',19541.03,198.00,36.70),(9,'Veneto',18351.49,264.00,40.60),(10,'Lombardia',23862.87,421.00,37.80),(11,'Sardegna',24106.30,65.00,23.50),(12,'Calabria',15212.65,120.00,21.00),(13,'Marche',9344.54,159.00,49.10),(14,'Toscana',22985.01,159.00,22.90),(15,'Valle d\'Aosta',3258.61,38.00,46.30),(16,'Liguria',5417.71,279.00,41.80),(17,'Trentino-Alto Adige',13605.97,80.00,37.70),(18,'Abruzzo',10828.89,117.00,31.00),(19,'Friuli-Venezia Giulia',7936.83,150.00,37.70),(20,'Sicilia',25824.33,185.00,26.30);
/*!40000 ALTER TABLE `regioni` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-14 15:52:05
