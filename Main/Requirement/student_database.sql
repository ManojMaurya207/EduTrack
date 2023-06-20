-- MySQL dump 10.12
--
-- Host: localhost    Database: student_database
-- ------------------------------------------------------
-- Server version	6.0.0-alpha-community-nt-debug

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
CREATE TABLE `class` (
  `std_id` varchar(10) NOT NULL,
  PRIMARY KEY (`std_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES ('10th std'),('5th std'),('6th std'),('7th std'),('8th std'),('9th std');
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `stud_id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gen` char(1) NOT NULL,
  `std_code` varchar(10) NOT NULL,
  `dob` date NOT NULL,
  `phone_no` bigint(10) NOT NULL,
  `address` varchar(60) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`stud_id`),
  KEY `std_code` (`std_code`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`std_code`) REFERENCES `class` (`std_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (101,'Ankit Prajapati','M','10th std','2008-11-26',8097206002,'Hingwala Lane Ghatkopar, Mumbai,400077',NULL,NULL),(102,'Manoj Maurya','M','10th std','2008-08-29',9372313346,'vijay nagar,chembur, Mumbai,400074,India',NULL,NULL),(103,'Dhruv Kushvaha','M','10th std','2008-04-11',9136842301,'Konkan Lane Ghatkopar, Mumbai,400077',NULL,NULL),(104,'Yoshita Ahuja','F','9th std','2008-08-04',9366313346,'vijay nagar,chembur, Mumbai,400074,India',NULL,NULL),(105,'Soman Kushvaha','F','8th std','2010-01-18',9004807723,'Shabari Hotel Vashi Navi Mumbai, 400094',NULL,NULL),(106,'Aditi mehra','F','8th std','2007-03-12',9366313046,'vijay nagar,chembur, Mumbai,400074,India',NULL,NULL),(107,'Sita raman','F','8th std','2008-06-21',8136843301,'Navjeevan Lane Ghatkopar, Mumbai,400037',NULL,NULL),(108,'Garima Maurya','F','7th std','2006-06-02',9123313346,'Shabari Hotel Vashi Navi Mumbai,400703,',NULL,NULL),(109,'Rohan Singh','M','7th std','2011-05-21',9133442332,'Western Highway Sativali Vasai 401202',NULL,NULL),(110,'Aditiya mehra','M','6th std','2013-03-01',9366312046,'vijay nagar,chembur, Mumbai,400074,India',NULL,NULL),(111,'Ram Charan','M','6th std','2014-03-11',9930443301,'Plaza Theatre Shivaji Mandir Kelkar Marg Dadar Mumbai-400028',NULL,NULL),(112,'Suhani mishra','F','5th std','2008-05-30',8098942332,'Sassoon Dock Road Colaba, Mumbai-400005',NULL,NULL),(113,'Manish Mehra','M','5th std','2013-05-18',9098789098,'mahul goan,chembur,mumbai-74',NULL,NULL),(114,'Neha Kanojiya','F','6th std','2012-10-10',8879098766,'ganesh nagar,chembur,mumbai-74',NULL,NULL),(115,'Aishwarya Yadav','F','7th std','2011-06-12',9976713390,'Ghatkopar ,chembur,mumbai-71',NULL,NULL),(116,'Ridhika Maurya ','F','5th std','2013-09-17',9845787898,'palghar,chembur-74',NULL,NULL),(117,'Riya Saw','F','8th std','2010-06-17',8756330922,'Thakkar Bappa,kurla,chembur,mumbai-74',NULL,NULL),(118,'Khushi Ram','F','7th std','2011-06-05',9536851056,'Ashok nagar,chembur,mumbai-74',NULL,NULL),(119,'Rudra Singh','M','7th std','2010-08-05',9674165743,'vijay nagar,chembur,mumbai-400074',NULL,NULL),(120,'Umesh Dok','M','5th std','2013-07-19',8967889876,'Bharat nagar,chembur,mumbai-400071',NULL,NULL),(121,'Chetna Bhat','F','5th std','2013-01-11',8755674565,'Navjeevan Society ,chembur,mumbai-400074',NULL,NULL),(122,'Vinat Golekar','M','6th std','2012-03-27',9855908213,'Ambarnath,mumbai-74',NULL,NULL),(123,'Mansi Khaste','F','7th std','2011-04-26',9926578909,'mahul road,chembur,mumbai-400074',NULL,NULL);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
CREATE TABLE `subject` (
  `sub_id` int(5) NOT NULL,
  `sub_name` varchar(20) NOT NULL,
  PRIMARY KEY (`sub_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES (1,'English'),(2,'Hindi'),(3,'Marathi'),(4,'Mathematics'),(5,'Science'),(6,'Social_Studies'),(7,'Physical_training');
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teach_class`
--

DROP TABLE IF EXISTS `teach_class`;
CREATE TABLE `teach_class` (
  `teacher_code` int(5) NOT NULL DEFAULT '0',
  `std_code` varchar(10) NOT NULL DEFAULT '',
  `sub_code` int(5) DEFAULT NULL,
  PRIMARY KEY (`teacher_code`,`std_code`),
  KEY `std_code` (`std_code`),
  KEY `sub_code` (`sub_code`),
  CONSTRAINT `teach_class_ibfk_1` FOREIGN KEY (`teacher_code`) REFERENCES `teacher` (`teacher_id`),
  CONSTRAINT `teach_class_ibfk_2` FOREIGN KEY (`std_code`) REFERENCES `class` (`std_id`),
  CONSTRAINT `teach_class_ibfk_3` FOREIGN KEY (`sub_code`) REFERENCES `subject` (`sub_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `teach_class`
--

LOCK TABLES `teach_class` WRITE;
/*!40000 ALTER TABLE `teach_class` DISABLE KEYS */;
INSERT INTO `teach_class` VALUES (501,'8th std',1),(502,'5th std',1),(503,'10th std',1),(504,'9th std',1),(505,'6th std',1),(505,'7th std',1),(507,'10th std',2),(507,'6th std',2),(507,'8th std',2),(510,'5th std',2),(510,'7th std',2),(510,'9th std',2),(507,'5th std',3),(507,'7th std',3),(507,'9th std',3),(510,'10th std',3),(510,'6th std',3),(510,'8th std',3),(506,'10th std',4),(506,'6th std',4),(506,'9th std',4),(509,'5th std',4),(509,'7th std',4),(509,'8th std',4),(501,'5th std',5),(503,'7th std',5),(504,'10th std',5),(504,'6th std',5),(505,'8th std',5),(505,'9th std',5),(501,'10th std',6),(502,'7th std',6),(502,'9th std',6),(503,'6th std',6),(504,'8th std',6),(505,'5th std',6),(508,'10th std',7),(508,'5th std',7),(508,'6th std',7),(508,'7th std',7),(508,'8th std',7),(508,'9th std',7);
/*!40000 ALTER TABLE `teach_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher` (
  `teacher_id` int(5) NOT NULL DEFAULT '0',
  `name` varchar(20) NOT NULL,
  `gen` char(1) NOT NULL,
  `quali` varchar(10) NOT NULL,
  `dob` date NOT NULL,
  `phone_no` bigint(10) NOT NULL,
  `address` varchar(60) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(15) NOT NULL,
  PRIMARY KEY (`teacher_id`),
  UNIQUE KEY `phone_no` (`phone_no`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES (501,'Madhavi vaidya','F','PhD','1986-08-12',9869026553,'Tata colony chembur mumbai-40070','madhavi_vaidya','python123'),(502,'Rajshree date','F','M.ed','1996-01-27',8425899501,'Shivaji maharaj lane ghatkopar mumbai-40070','rajshree_date','mysql123'),(503,'Kamlakar bhopatkar','M','M.ed','1990-02-17',8452899501,'Shivaji nagar thane mumbai-400074','kamlakar_bhopatkar','dm123'),(504,'Karan Lodha','M','B.ed','1991-11-16',8002899501,'Harshvardan chock kalyan mumbai-400084','karan_lodha','lodha123'),(505,'Simran Kaur','F','M.ed','1997-05-26',8002899789,'Harshvardan chock kalyan mumbai-400084','simran_lodha','simran123'),(506,'Sujit Chavan','M','PhD','1995-07-20',8850172221,'Jambli Naka Opp Ganpati Temple Thane Mumbai,400601','sujit_chavan','sujit123'),(507,'Laxmi tiwari','F','B.ed','1997-02-27',8456299501,'Gandhi nagar pavai mumbai-400074','Laxmi_tiwari','cpp123'),(508,'Amit Pore ','M','D.ed','1976-02-22',7699012345,'Bhandup ,kharghar ,mumbai-400074','Amit_123','Drawing_123'),(509,'Rupanjali Kate','F','B.ed','1980-06-09',8809126789,'Raj Residency,andheri,mumbai-71','Rupan_123','Math_123'),(510,'Rajkumar Prajapati','M','D.ed','1970-04-08',9372148495,'lotus villa,malad,mumbai-72','Raj_123','Hindi_123');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-24 19:00:39
