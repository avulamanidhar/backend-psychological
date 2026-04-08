-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: psychological
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `api_activitylog`
--

DROP TABLE IF EXISTS `api_activitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_activitylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activity_type` varchar(50) NOT NULL,
  `duration_minutes` int NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `details` json NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_activitylog_user_id_460724d0_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_activitylog_user_id_460724d0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_activitylog`
--

LOCK TABLES `api_activitylog` WRITE;
/*!40000 ALTER TABLE `api_activitylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_activitylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_aianalysis`
--

DROP TABLE IF EXISTS `api_aianalysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_aianalysis` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `subtitle` varchar(200) NOT NULL,
  `steps` json NOT NULL,
  `confidence_level` int NOT NULL,
  `data_points_count` int NOT NULL,
  `weeks_count` int NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_aianalysis_user_id_4f7a5d52_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_aianalysis_user_id_4f7a5d52_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_aianalysis`
--

LOCK TABLES `api_aianalysis` WRITE;
/*!40000 ALTER TABLE `api_aianalysis` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_aianalysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_aitransparency`
--

DROP TABLE IF EXISTS `api_aitransparency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_aitransparency` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `section_key` varchar(50) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `section_key` (`section_key`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_aitransparency`
--

LOCK TABLES `api_aitransparency` WRITE;
/*!40000 ALTER TABLE `api_aitransparency` DISABLE KEYS */;
INSERT INTO `api_aitransparency` VALUES (1,'how_it_works','How AI Works','Our AI analyzes patterns in your mood logs and journal entries to provide personalized insights. It recognizes linguistic and behavioral patterns — it does not understand emotions like a human.','2026-03-11 03:40:02.960711'),(2,'limitations','Limitations','● AI is not a substitute for professional therapy\n● It cannot diagnose mental health conditions\n● In crisis situations, it directs you to human resources\n● Insights are probabilistic, not definitive','2026-03-11 03:40:02.967752'),(3,'data_usage','Data Usage','Your data is used solely to improve your personal experience. We do not sell or share your data with third parties. All processing happens on-device.','2026-03-11 03:40:02.974146');
/*!40000 ALTER TABLE `api_aitransparency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_appconfig`
--

DROP TABLE IF EXISTS `api_appconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_appconfig` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `key` varchar(50) NOT NULL,
  `value` longtext NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_appconfig`
--

LOCK TABLES `api_appconfig` WRITE;
/*!40000 ALTER TABLE `api_appconfig` DISABLE KEYS */;
INSERT INTO `api_appconfig` VALUES (1,'support_email','support@mindguard.ai','Global support email'),(2,'min_app_version','1.0.0','Minimum required app version'),(3,'maintenance_mode','false','If true, show maintenance screen');
/*!40000 ALTER TABLE `api_appconfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_chatmessage`
--

DROP TABLE IF EXISTS `api_chatmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_chatmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `is_user` tinyint(1) NOT NULL,
  `mode` varchar(20) NOT NULL,
  `language` varchar(20) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `risk_level` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_chatmessage_user_id_f447108a_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_chatmessage_user_id_f447108a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=261 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_chatmessage`
--

LOCK TABLES `api_chatmessage` WRITE;
/*!40000 ALTER TABLE `api_chatmessage` DISABLE KEYS */;
INSERT INTO `api_chatmessage` VALUES (191,'Help me relax',1,'General','English','2026-03-28 07:10:59.977916',60,'LOW'),(192,'I\'m sorry, the AI took too long to respond. Please try again later.',0,'General','English','2026-03-28 07:11:47.360308',60,'LOW'),(193,'Help me relax',1,'General','English','2026-03-28 07:18:41.317580',60,'LOW'),(194,'I\'m sorry, AI currently unavailable. Please try again later.',0,'General','English','2026-03-28 07:18:47.778437',60,'LOW'),(195,'Help me relax',1,'General','English','2026-03-28 07:48:03.537506',60,'LOW'),(196,'I hear you, and thank you for sharing that with me. Could you tell me a bit more about how you\'re feeling? I\'m here to listen and help.',0,'General','English','2026-03-28 07:48:03.561382',60,'LOW'),(197,'Tell me a joke',1,'General','English','2026-03-28 07:48:11.613627',60,'LOW'),(198,'I hear you, and thank you for sharing that with me. Could you tell me a bit more about how you\'re feeling? I\'m here to listen and help.',0,'General','English','2026-03-28 07:48:11.633179',60,'LOW'),(199,'Suggest a song',1,'General','English','2026-03-28 07:48:18.010620',60,'LOW'),(200,'Music is great therapy! What mood are you in? \n\nIf you want to relax, try this calming Lo-Fi mix: https://www.youtube.com/watch?v=jfKfPfyJRdk',0,'General','English','2026-03-28 07:48:18.027098',60,'LOW'),(201,'I had a great day!',1,'General','English','2026-03-28 07:48:28.341858',60,'LOW'),(202,'Make sure you eat something healthy and delicious! Nourishing your body is a great way to improve your mood and energy.',0,'General','English','2026-03-28 07:48:28.357251',60,'LOW'),(203,'Sleep tips?',1,'General','English','2026-03-28 07:48:37.276446',60,'LOW'),(204,'Sleep difficulties can be really hard. Try to avoid screens before bed. \n\nHere is a wonderful sleep meditation video you can play in the background: https://www.youtube.com/watch?v=aEqlQvczzso',0,'General','English','2026-03-28 07:48:37.297355',60,'LOW'),(205,'hi',1,'General','English','2026-03-28 07:48:46.590895',60,'LOW'),(206,'Hello there! ? I\'m MindGuard. How are you feeling today? You can share anything with me.',0,'General','English','2026-03-28 07:48:46.607015',60,'LOW'),(207,'had your food',1,'General','English','2026-03-28 07:49:01.008379',60,'LOW'),(208,'Make sure you eat something healthy and delicious! Nourishing your body is a great way to improve your mood and energy.',0,'General','English','2026-03-28 07:49:01.023841',60,'LOW'),(209,'Help me relax',1,'General','English','2026-03-28 08:15:55.065080',60,'LOW'),(210,'I hear you, and thank you for sharing that with me. Could you tell me a bit more about how you\'re feeling? I\'m here to listen and help.',0,'General','English','2026-03-28 08:15:55.098406',60,'LOW'),(211,'I feel stressed',1,'General','English','2026-03-28 08:16:07.942910',60,'LOW'),(212,'I notice you\'re feeling stressed. Let\'s try a quick breathing exercise: Inhale for 4s, hold for 4s, exhale for 4s. \n\nYou can also check out this relaxing 10-minute stress relief video: https://www.youtube.com/watch?v=inpok4MKVLM\n\n? Also, from our trained MindGuard Knowledge Base: Stress is a feeling of emotional or physical tension. It can come from any event or thought that makes you feel frustrated, angry, or nervous. Strategies: Exercise, Mindfulness, Time management, Setting boundaries',0,'General','English','2026-03-28 08:16:07.950178',60,'LOW'),(213,'Help me relax',1,'General','English','2026-04-06 08:47:54.912436',63,'LOW'),(214,'I hear you, and thank you for sharing that with me. Could you tell me a bit more about how you\'re feeling? I\'m here to listen and help.',0,'General','English','2026-04-06 08:47:54.958283',63,'LOW'),(241,'I feel stressed',1,'General','English','2026-04-06 10:06:44.083993',65,'LOW'),(242,'I notice you\'re feeling stressed. Let\'s try a quick breathing exercise: Inhale for 4s, hold for 4s, exhale for 4s. \n\nYou can also check out this relaxing 10-minute stress relief video: https://www.youtube.com/watch?v=inpok4MKVLM\n\n? Also, from our trained MindGuard Knowledge Base: Stress is a feeling of emotional or physical tension. It can come from any event or thought that makes you feel frustrated, angry, or nervous. Strategies: Exercise, Mindfulness, Time management, Setting boundaries',0,'General','English','2026-04-06 10:06:44.109625',65,'LOW'),(243,'Help me relax',1,'General','English','2026-04-06 10:09:29.883235',65,'LOW'),(244,'I hear you, and thank you for sharing that with me. Could you tell me a bit more about how you\'re feeling? I\'m here to listen and help.',0,'General','English','2026-04-06 10:09:29.994408',65,'LOW'),(245,'Suggest a song',1,'General','English','2026-04-06 10:09:39.922939',65,'LOW'),(246,'Music is great therapy! What mood are you in? \n\nIf you want to relax, try this calming Lo-Fi mix: https://www.youtube.com/watch?v=jfKfPfyJRdk',0,'General','English','2026-04-06 10:09:39.936997',65,'LOW'),(247,'I feel lonely',1,'General','English','2026-04-06 10:09:47.131671',65,'LOW'),(248,'I know feeling lonely is hard. I am always here to chat with you! \n\nSometimes watching comforting videos helps. Check this out: https://www.youtube.com/watch?v=n3Xv_g3g-mA',0,'General','English','2026-04-06 10:09:47.141930',65,'LOW'),(249,'Sleep tips?',1,'General','English','2026-04-06 10:09:55.097264',65,'LOW'),(250,'Sleep difficulties can be really hard. Try to avoid screens before bed. \n\nHere is a wonderful sleep meditation video you can play in the background: https://www.youtube.com/watch?v=aEqlQvczzso',0,'General','English','2026-04-06 10:09:55.110664',65,'LOW'),(251,'I had a great day!',1,'General','English','2026-04-06 10:10:01.247011',65,'LOW'),(252,'Make sure you eat something healthy and delicious! Nourishing your body is a great way to improve your mood and energy.',0,'General','English','2026-04-06 10:10:01.258255',65,'LOW'),(253,'I\'m stressed about work',1,'General','English','2026-04-08 09:00:45.636863',65,'LOW'),(254,'I notice you\'re feeling stressed. Let\'s try a quick breathing exercise: Inhale for 4s, hold for 4s, exhale for 4s. \n\nYou can also check out this relaxing 10-minute stress relief video: https://www.youtube.com/watch?v=inpok4MKVLM\n\n? Also, from our trained MindGuard Knowledge Base: Stress is a feeling of emotional or physical tension. It can come from any event or thought that makes you feel frustrated, angry, or nervous. Strategies: Exercise, Mindfulness, Time management, Setting boundaries',0,'General','English','2026-04-08 09:00:45.660177',65,'LOW'),(255,'I feel anxious',1,'General','English','2026-04-08 09:00:57.021345',65,'LOW'),(256,'It sounds like you\'re experiencing some anxiety. Take a deep breath. \n\nTry this grounding technique or check out this guided anxiety relief meditation: https://www.youtube.com/watch?v=O-6f5wQXSu8',0,'General','English','2026-04-08 09:00:57.042387',65,'LOW'),(257,'I can\'t sleep',1,'General','English','2026-04-08 09:01:03.957949',65,'LOW'),(258,'Sleep difficulties can be really hard. Try to avoid screens before bed. \n\nHere is a wonderful sleep meditation video you can play in the background: https://www.youtube.com/watch?v=aEqlQvczzso',0,'General','English','2026-04-08 09:01:03.977264',65,'LOW'),(259,'Find a doctor',1,'General','English','2026-04-08 09:01:10.807720',65,'LOW'),(260,'I hear you, and thank you for sharing that with me. Could you tell me a bit more about how you\'re feeling? I\'m here to listen and help.',0,'General','English','2026-04-08 09:01:10.825586',65,'LOW');
/*!40000 ALTER TABLE `api_chatmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_detectedpattern`
--

DROP TABLE IF EXISTS `api_detectedpattern`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_detectedpattern` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `confidence` varchar(10) NOT NULL,
  `pattern_type` varchar(20) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_detectedpattern_user_id_0e178dd2_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_detectedpattern_user_id_0e178dd2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_detectedpattern`
--

LOCK TABLES `api_detectedpattern` WRITE;
/*!40000 ALTER TABLE `api_detectedpattern` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_detectedpattern` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_faq`
--

DROP TABLE IF EXISTS `api_faq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_faq` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question` varchar(255) NOT NULL,
  `answer` longtext NOT NULL,
  `order` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_faq`
--

LOCK TABLES `api_faq` WRITE;
/*!40000 ALTER TABLE `api_faq` DISABLE KEYS */;
INSERT INTO `api_faq` VALUES (1,'How do I log my mood?','You can log your mood by clicking the \'+\' button on the home screen and selecting your current emotion.',1),(2,'Is my data secure?','Yes, we use industry-standard encryption to protect your data. Your privacy is our top priority.',2),(3,'How does the AI analysis work?','The AI analyzes your mood patterns and journal entries to provide personalized insights and suggestions.',3);
/*!40000 ALTER TABLE `api_faq` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_feedback`
--

DROP TABLE IF EXISTS `api_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_feedback` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(100) NOT NULL,
  `message` longtext NOT NULL,
  `rating` int NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_feedback_user_id_af9adbfc_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_feedback_user_id_af9adbfc_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_feedback`
--

LOCK TABLES `api_feedback` WRITE;
/*!40000 ALTER TABLE `api_feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_howitworksstep`
--

DROP TABLE IF EXISTS `api_howitworksstep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_howitworksstep` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `order` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_howitworksstep`
--

LOCK TABLES `api_howitworksstep` WRITE;
/*!40000 ALTER TABLE `api_howitworksstep` DISABLE KEYS */;
INSERT INTO `api_howitworksstep` VALUES (1,'Log Your Mood','Daily check-ins with emojis, journaling, and stress tracking.',1),(2,'Get AI Insights','Our AI analyzes patterns to help you understand emotional triggers.',2),(3,'Find Support','Access coping tools, guided exercises, and professional resources.',3);
/*!40000 ALTER TABLE `api_howitworksstep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_moodentry`
--

DROP TABLE IF EXISTS `api_moodentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_moodentry` (
  `id` varchar(100) NOT NULL,
  `timestampMillis` bigint NOT NULL,
  `moodName` varchar(50) NOT NULL,
  `moodImageResId` int NOT NULL,
  `intensity` int NOT NULL,
  `triggers` json NOT NULL,
  `journal` longtext,
  `aiReflection` longtext,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_moodentry_user_id_3c25cfcb_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_moodentry_user_id_3c25cfcb_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_moodentry`
--

LOCK TABLES `api_moodentry` WRITE;
/*!40000 ALTER TABLE `api_moodentry` DISABLE KEYS */;
INSERT INTO `api_moodentry` VALUES ('01c39d18-207f-4022-a6d6-a2e1fed2a5f6',1774599279303,'Sad',2131165377,50,'[\"Sleep\"]','','Based on this entry, you were experiencing sad emotions with moderate intensity. Sleep appear to be contributing factors.',NULL),('0e945b12-c305-47d5-bf33-0c28be709f9c',1775470096829,'Great',2131165372,82,'[\"Other\"]','','Based on this entry, you were experiencing great emotions with high intensity. Other appear to be contributing factors.',66),('26d8fba9-5376-43b8-9c83-4050a7103cb0',1774668316296,'Good',2131165373,50,'[\"Work\"]','','Based on this entry, you were experiencing good emotions with moderate intensity. Work appear to be contributing factors.',NULL),('32aaf4ec-6504-413a-8bbd-50e5aa4e242d',1775469907848,'Great',2131165372,82,'[\"Other\"]','','Based on this entry, you were experiencing great emotions with high intensity. Other appear to be contributing factors.',65),('8c475b7d-7b50-4029-a084-2f45e64bd682',1774685792518,'Low',2131165376,72,'[\"Relationships\"]','','Based on this entry, you were experiencing low emotions with high intensity. Relationships appear to be contributing factors.',60),('f20104b9-caa0-4299-b2c1-abee0af5ef55',1774671162238,'Sad',2131165377,50,'[\"Work\"]','','Based on this entry, you were experiencing sad emotions with moderate intensity. Work appear to be contributing factors.',60),('mood_web_1775638738303',1775638738303,'Okay',3,50,'[\"Sleep\"]','','Based on this entry, you were experiencing okay emotions with moderate intensity. Sleep appear to be contributing factors.',65);
/*!40000 ALTER TABLE `api_moodentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_notification`
--

DROP TABLE IF EXISTS `api_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_notification_user_id_6cede59e_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_notification_user_id_6cede59e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_notification`
--

LOCK TABLES `api_notification` WRITE;
/*!40000 ALTER TABLE `api_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_passwordresetlog`
--

DROP TABLE IF EXISTS `api_passwordresetlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_passwordresetlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `action` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_passwordresetlog`
--

LOCK TABLES `api_passwordresetlog` WRITE;
/*!40000 ALTER TABLE `api_passwordresetlog` DISABLE KEYS */;
INSERT INTO `api_passwordresetlog` VALUES (3,'maniyadavrc@gmail.com','10.213.230.119','2026-03-27 03:03:56.865362','REQUEST'),(4,'maniyadavrc@gmail.com','10.213.230.119','2026-03-27 03:04:00.670597','EMAIL_SEND_FAIL'),(5,'maniyadavrc@gmail.com','10.213.230.119','2026-03-27 03:04:16.349530','REQUEST'),(6,'maniyadavrc@gmail.com','10.213.230.119','2026-03-27 03:04:20.427086','EMAIL_SEND_FAIL'),(7,'manikantayadav2007@gmail.com','10.213.230.119','2026-03-27 03:35:04.189088','REQUEST'),(8,'manikantayadav2007@gmail.com','10.213.230.119','2026-03-27 03:35:07.992234','REQUEST'),(9,'manikantayadav2007@gmail.com','10.213.230.119','2026-03-27 03:35:13.920713','REQUEST'),(10,'maniyadavrc@gmail.com','10.213.230.119','2026-03-27 03:40:07.061310','REQUEST'),(11,'manikantayadav2007@gmail.com','10.213.230.119','2026-03-28 03:20:35.358835','REQUEST'),(12,'manikantayadav2007@gmail.com','10.213.230.119','2026-03-28 03:23:41.202783','REQUEST');
/*!40000 ALTER TABLE `api_passwordresetlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_passwordresetotp`
--

DROP TABLE IF EXISTS `api_passwordresetotp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_passwordresetotp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `otp` varchar(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expiry_time` datetime(6) NOT NULL,
  `attempts` int NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `user_id` int DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_passwordresetotp_user_id_f36296cf_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_passwordresetotp_user_id_f36296cf_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_passwordresetotp`
--

LOCK TABLES `api_passwordresetotp` WRITE;
/*!40000 ALTER TABLE `api_passwordresetotp` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_passwordresetotp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_privacypolicy`
--

DROP TABLE IF EXISTS `api_privacypolicy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_privacypolicy` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `version` varchar(20) NOT NULL,
  `content` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `version` (`version`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_privacypolicy`
--

LOCK TABLES `api_privacypolicy` WRITE;
/*!40000 ALTER TABLE `api_privacypolicy` DISABLE KEYS */;
INSERT INTO `api_privacypolicy` VALUES (1,'1.0.0','\n            # Privacy & Consent\n            \n            Welcome to MindGuard AI. Your privacy is our top priority.\n            \n            ### 1. Data Collection\n            We collect mood logs, journal entries, and activity data to provide personalized insights.\n            \n            ### 2. Encryption\n            All your personal data is encrypted with AES-256 standards. We cannot access your private thoughts.\n            \n            ### 3. Your Choices\n            You have full control over your data. You can export or delete your account at any time.\n            ',1,'2026-03-11 06:46:52.107183');
/*!40000 ALTER TABLE `api_privacypolicy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_recommendation`
--

DROP TABLE IF EXISTS `api_recommendation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_recommendation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `duration` varchar(20) NOT NULL,
  `difficulty` varchar(20) NOT NULL,
  `type` varchar(50) NOT NULL,
  `image_tag` varchar(20) NOT NULL,
  `action_text` varchar(50) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_recommendation_user_id_8906e40b_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_recommendation_user_id_8906e40b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_recommendation`
--

LOCK TABLES `api_recommendation` WRITE;
/*!40000 ALTER TABLE `api_recommendation` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_recommendation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_userprofile`
--

DROP TABLE IF EXISTS `api_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `avatar_name` varchar(100) NOT NULL,
  `language` varchar(20) NOT NULL,
  `text_size` varchar(20) NOT NULL,
  `notifications_enabled` tinyint(1) NOT NULL,
  `notification_time` varchar(20) NOT NULL,
  `mental_health_score` int NOT NULL,
  `user_id` int NOT NULL,
  `bio` longtext,
  `goals` json NOT NULL DEFAULT (_utf8mb4'[]'),
  `age_range` varchar(50) DEFAULT NULL,
  `high_contrast` tinyint(1) NOT NULL,
  `screen_reader` tinyint(1) NOT NULL,
  `anonymous_analytics` tinyint(1) NOT NULL,
  `essential_data_processing` tinyint(1) NOT NULL,
  `privacy_consent_accepted` tinyint(1) NOT NULL,
  `privacy_policy_version` varchar(20) NOT NULL,
  `emergency_alerts_enabled` tinyint(1) NOT NULL,
  `mood_alerts_enabled` tinyint(1) NOT NULL,
  `weekly_insights_enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `api_userprofile_user_id_5a1c1c92_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_userprofile`
--

LOCK TABLES `api_userprofile` WRITE;
/*!40000 ALTER TABLE `api_userprofile` DISABLE KEYS */;
INSERT INTO `api_userprofile` VALUES (58,'avatar_4','English','Medium',1,'9:00 AM',47,60,NULL,'[\"Smart Alerts\", \"Breathing\", \"AI Support\", \"Journaling\", \"Meditation\"]','18 - 24',0,0,0,1,1,'1.0.0',1,1,1),(61,'default_avatar','English','Medium',1,'9:00 AM',0,63,NULL,'[]',NULL,0,0,0,1,0,'1.0.0',1,1,0),(63,'?','English','Medium',1,'9:00 AM',45,65,NULL,'[\"Build Resilience\"]','18 – 24',1,1,1,1,1,'1.0.0',1,1,1),(64,'avatar_1','English','Medium',1,'9:00 AM',25,66,NULL,'[\"Meditation\", \"Smart Alerts\", \"Breathing\", \"AI Support\", \"Journaling\"]','18 - 24',1,1,1,1,1,'1.0.0',1,1,1);
/*!40000 ALTER TABLE `api_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add mood entry',7,'add_moodentry'),(26,'Can change mood entry',7,'change_moodentry'),(27,'Can delete mood entry',7,'delete_moodentry'),(28,'Can view mood entry',7,'view_moodentry'),(29,'Can add activity log',8,'add_activitylog'),(30,'Can change activity log',8,'change_activitylog'),(31,'Can delete activity log',8,'delete_activitylog'),(32,'Can view activity log',8,'view_activitylog'),(33,'Can add user profile',10,'add_userprofile'),(34,'Can change user profile',10,'change_userprofile'),(35,'Can delete user profile',10,'delete_userprofile'),(36,'Can view user profile',10,'view_userprofile'),(37,'Can add chat message',9,'add_chatmessage'),(38,'Can change chat message',9,'change_chatmessage'),(39,'Can delete chat message',9,'delete_chatmessage'),(40,'Can view chat message',9,'view_chatmessage'),(41,'Can add feedback',11,'add_feedback'),(42,'Can change feedback',11,'change_feedback'),(43,'Can delete feedback',11,'delete_feedback'),(44,'Can view feedback',11,'view_feedback'),(45,'Can add ai analysis',12,'add_aianalysis'),(46,'Can change ai analysis',12,'change_aianalysis'),(47,'Can delete ai analysis',12,'delete_aianalysis'),(48,'Can view ai analysis',12,'view_aianalysis'),(49,'Can add ai transparency',13,'add_aitransparency'),(50,'Can change ai transparency',13,'change_aitransparency'),(51,'Can delete ai transparency',13,'delete_aitransparency'),(52,'Can view ai transparency',13,'view_aitransparency'),(53,'Can add detected pattern',14,'add_detectedpattern'),(54,'Can change detected pattern',14,'change_detectedpattern'),(55,'Can delete detected pattern',14,'delete_detectedpattern'),(56,'Can view detected pattern',14,'view_detectedpattern'),(57,'Can add faq',15,'add_faq'),(58,'Can change faq',15,'change_faq'),(59,'Can delete faq',15,'delete_faq'),(60,'Can view faq',15,'view_faq'),(61,'Can add how it works step',16,'add_howitworksstep'),(62,'Can change how it works step',16,'change_howitworksstep'),(63,'Can delete how it works step',16,'delete_howitworksstep'),(64,'Can view how it works step',16,'view_howitworksstep'),(65,'Can add app config',17,'add_appconfig'),(66,'Can change app config',17,'change_appconfig'),(67,'Can delete app config',17,'delete_appconfig'),(68,'Can view app config',17,'view_appconfig'),(69,'Can add notification',18,'add_notification'),(70,'Can change notification',18,'change_notification'),(71,'Can delete notification',18,'delete_notification'),(72,'Can view notification',18,'view_notification'),(73,'Can add recommendation',19,'add_recommendation'),(74,'Can change recommendation',19,'change_recommendation'),(75,'Can delete recommendation',19,'delete_recommendation'),(76,'Can view recommendation',19,'view_recommendation'),(77,'Can add privacy policy',20,'add_privacypolicy'),(78,'Can change privacy policy',20,'change_privacypolicy'),(79,'Can delete privacy policy',20,'delete_privacypolicy'),(80,'Can view privacy policy',20,'view_privacypolicy'),(81,'Can add password reset otp',21,'add_passwordresetotp'),(82,'Can change password reset otp',21,'change_passwordresetotp'),(83,'Can delete password reset otp',21,'delete_passwordresetotp'),(84,'Can view password reset otp',21,'view_passwordresetotp'),(85,'Can add password reset log',22,'add_passwordresetlog'),(86,'Can change password reset log',22,'change_passwordresetlog'),(87,'Can delete password reset log',22,'delete_passwordresetlog'),(88,'Can view password reset log',22,'view_passwordresetlog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (60,'pbkdf2_sha256$1200000$vixz9omB5vrXdNl0UbtgA9$Z6lkpwhcFSWhnb7kxLt7yS66hYbery5Ox9SYblDd2SQ=',NULL,0,'vamsigupta','','','vamsigupta8@gmail.com',0,1,'2026-03-28 04:12:21.597645'),(63,'pbkdf2_sha256$1200000$OFasecpARNSVMlBXHKF6qV$T72ENy3vXJPTFq9OZj1uPIG73D/h3lr0mY7plUZJBDs=',NULL,0,'relaxuser1775465263','','','relaxuser1775465263@t.com',0,1,'2026-04-06 08:47:44.227165'),(65,'pbkdf2_sha256$1200000$IjomSpSZ9tvRKDPMeiRsWR$T3cGG5NdZ1Ur3XpOXzSZgdbkAJTCgNTJk+90acA9FFE=',NULL,0,'avulaManidhar','','','manikantayadav2007@gmail.com',0,1,'2026-04-06 10:04:27.563876'),(66,'pbkdf2_sha256$1200000$XNtXykkun4632cA6BKtD1D$8pB3//pSd5MpImoKHSfPjdLYEtpVcr4e7TcLt+/7PAI=',NULL,0,'ManiYadav','','','maniyadavrc@gmail.com',0,1,'2026-04-06 10:07:43.175712');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(8,'api','activitylog'),(12,'api','aianalysis'),(13,'api','aitransparency'),(17,'api','appconfig'),(9,'api','chatmessage'),(14,'api','detectedpattern'),(15,'api','faq'),(11,'api','feedback'),(16,'api','howitworksstep'),(7,'api','moodentry'),(18,'api','notification'),(22,'api','passwordresetlog'),(21,'api','passwordresetotp'),(20,'api','privacypolicy'),(19,'api','recommendation'),(10,'api','userprofile'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-03-07 03:08:52.699991'),(2,'auth','0001_initial','2026-03-07 03:08:55.128340'),(3,'admin','0001_initial','2026-03-07 03:08:55.712936'),(4,'admin','0002_logentry_remove_auto_add','2026-03-07 03:08:55.729566'),(5,'admin','0003_logentry_add_action_flag_choices','2026-03-07 03:08:55.747251'),(6,'api','0001_initial','2026-03-07 03:08:56.072084'),(7,'contenttypes','0002_remove_content_type_name','2026-03-07 03:08:56.772773'),(8,'auth','0002_alter_permission_name_max_length','2026-03-07 03:08:57.028365'),(9,'auth','0003_alter_user_email_max_length','2026-03-07 03:08:57.078866'),(10,'auth','0004_alter_user_username_opts','2026-03-07 03:08:57.094746'),(11,'auth','0005_alter_user_last_login_null','2026-03-07 03:08:57.280709'),(12,'auth','0006_require_contenttypes_0002','2026-03-07 03:08:57.296844'),(13,'auth','0007_alter_validators_add_error_messages','2026-03-07 03:08:57.313943'),(14,'auth','0008_alter_user_username_max_length','2026-03-07 03:08:57.585986'),(15,'auth','0009_alter_user_last_name_max_length','2026-03-07 03:08:57.782695'),(16,'auth','0010_alter_group_name_max_length','2026-03-07 03:08:57.814076'),(17,'auth','0011_update_proxy_permissions','2026-03-07 03:08:57.825887'),(18,'auth','0012_alter_user_first_name_max_length','2026-03-07 03:08:57.975532'),(19,'sessions','0001_initial','2026-03-07 03:08:58.083073'),(20,'api','0002_activitylog_chatmessage_userprofile','2026-03-09 08:13:27.729974'),(21,'api','0003_userprofile_bio_userprofile_goals_feedback','2026-03-09 08:27:48.725867'),(22,'api','0004_aianalysis','2026-03-11 03:27:01.758232'),(23,'api','0005_aitransparency','2026-03-11 03:38:21.113411'),(24,'api','0006_detectedpattern','2026-03-11 03:48:41.711365'),(25,'api','0007_userprofile_age_range','2026-03-11 04:08:18.868892'),(26,'api','0008_faq','2026-03-11 04:16:09.717296'),(27,'api','0009_howitworksstep','2026-03-11 04:28:48.144281'),(28,'api','0010_userprofile_high_contrast_userprofile_screen_reader','2026-03-11 04:38:51.944407'),(29,'api','0011_appconfig','2026-03-11 04:51:15.306541'),(30,'api','0012_notification','2026-03-11 05:24:50.248345'),(31,'api','0013_recommendation','2026-03-11 06:30:34.858233'),(32,'api','0014_privacypolicy_userprofile_anonymous_analytics_and_more','2026-03-11 06:41:34.675311'),(33,'api','0015_userprofile_emergency_alerts_enabled_and_more','2026-03-11 07:29:09.408044'),(34,'api','0016_chatmessage_risk_level_passwordresetotp','2026-03-19 05:44:15.873055'),(35,'api','0017_passwordresetlog_and_more','2026-03-26 10:58:54.337565');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-08 14:49:46
