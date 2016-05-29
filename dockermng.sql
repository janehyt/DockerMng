DROP DATABASE IF EXISTS `final_db`;
CREATE DATABASE  IF NOT EXISTS `final_db` DEFAULT CHARACTER SET utf8;
USE `final_db`;

--
-- Table structure for table `auth_group`
--


DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(13,'api','bind'),(11,'api','container'),(16,'api','creation'),(15,'api','environment'),(9,'api','image'),(12,'api','link'),(14,'api','port'),(10,'api','process'),(8,'api','repository'),(7,'api','volume'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;



--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add volume',7,'add_volume'),(20,'Can change volume',7,'change_volume'),(21,'Can delete volume',7,'delete_volume'),(22,'Can add repository',8,'add_repository'),(23,'Can change repository',8,'change_repository'),(24,'Can delete repository',8,'delete_repository'),(25,'Can add image',9,'add_image'),(26,'Can change image',9,'change_image'),(27,'Can delete image',9,'delete_image'),(28,'Can add process',10,'add_process'),(29,'Can change process',10,'change_process'),(30,'Can delete process',10,'delete_process'),(31,'Can add container',11,'add_container'),(32,'Can change container',11,'change_container'),(33,'Can delete container',11,'delete_container'),(34,'Can add link',12,'add_link'),(35,'Can change link',12,'change_link'),(36,'Can delete link',12,'delete_link'),(37,'Can add bind',13,'add_bind'),(38,'Can change bind',13,'change_bind'),(39,'Can delete bind',13,'delete_bind'),(40,'Can add port',14,'add_port'),(41,'Can change port',14,'change_port'),(42,'Can delete port',14,'delete_port'),(43,'Can add environment',15,'add_environment'),(44,'Can change environment',15,'change_environment'),(45,'Can delete environment',15,'delete_environment'),(46,'Can add creation',16,'add_creation'),(47,'Can change creation',16,'change_creation'),(48,'Can delete creation',16,'delete_creation');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$24000$lInsxi3SVof6$Ff9HNPp3T4glbiz6q7t2bO8t17HlL+snDCDCt2HDWV0=',CURDATE() ,1,'admin','','','admin@test.com',1,1,CURDATE() );
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;



--
-- Table structure for table `api_repository`
--

DROP TABLE IF EXISTS `api_repository`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_repository` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `namespace` varchar(150) NOT NULL,
  `description` longtext,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_repository_name_6dcda42b_uniq` (`name`,`namespace`),
  KEY `api_repository_user_id_b6894623_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_repository_user_id_b6894623_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_repository`
--

LOCK TABLES `api_repository` WRITE;
/*!40000 ALTER TABLE `api_repository` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_repository` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_volume`
--

DROP TABLE IF EXISTS `api_volume`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_volume` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `path` varchar(250) NOT NULL,
  `private` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_volume_user_id_2a9c44c9_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_volume_user_id_2a9c44c9_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_volume`
--

LOCK TABLES `api_volume` WRITE;
/*!40000 ALTER TABLE `api_volume` DISABLE KEYS */;
INSERT INTO `api_volume` VALUES (1,'/var/run/docker.sock','/var/run/docker.sock',0,1);
/*!40000 ALTER TABLE `api_volume` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_image`
--

DROP TABLE IF EXISTS `api_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `repository` varchar(250) NOT NULL,
  `tag` varchar(150) NOT NULL,
  `status` varchar(2) NOT NULL,
  `isbuild` tinyint(1) NOT NULL,
  `builddir` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_image_repository_3f10d0c8_uniq` (`repository`,`tag`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_image`
--

LOCK TABLES `api_image` WRITE;
/*!40000 ALTER TABLE `api_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_image_users`
--

DROP TABLE IF EXISTS `api_image_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_image_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_image_users_image_id_de328ae0_uniq` (`image_id`,`user_id`),
  KEY `api_image_users_user_id_7ad906a1_fk_auth_user_id` (`user_id`),
  CONSTRAINT `api_image_users_image_id_3672b116_fk_api_image_id` FOREIGN KEY (`image_id`) REFERENCES `api_image` (`id`),
  CONSTRAINT `api_image_users_user_id_7ad906a1_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_image_users`
--

LOCK TABLES `api_image_users` WRITE;
/*!40000 ALTER TABLE `api_image_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_image_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_container`
--

DROP TABLE IF EXISTS `api_container`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_container` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `command` varchar(150) DEFAULT NULL,
  `restart` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `image_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `api_container_f33175e6` (`image_id`),
  KEY `api_container_e8701ad4` (`user_id`),
  CONSTRAINT `api_container_image_id_a4c865e4_fk_api_image_id` FOREIGN KEY (`image_id`) REFERENCES `api_image` (`id`),
  CONSTRAINT `api_container_user_id_9932961d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_container`
--

LOCK TABLES `api_container` WRITE;
/*!40000 ALTER TABLE `api_container` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_container` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `api_bind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_bind` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(250) NOT NULL,
  `container_id` int(11) NOT NULL,
  `volume_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_bind_container_id_56b939e4_uniq` (`container_id`,`path`),
  KEY `api_bind_5733dad4` (`container_id`),
  KEY `api_bind_654102bb` (`volume_id`),
  CONSTRAINT `api_bind_container_id_6e3d04fe_fk_api_container_id` FOREIGN KEY (`container_id`) REFERENCES `api_container` (`id`),
  CONSTRAINT `api_bind_volume_id_ba92de09_fk_api_volume_id` FOREIGN KEY (`volume_id`) REFERENCES `api_volume` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_bind`
--

LOCK TABLES `api_bind` WRITE;
/*!40000 ALTER TABLE `api_bind` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_bind` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_creation`
--

DROP TABLE IF EXISTS `api_creation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_creation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `count` int(11) NOT NULL,
  `date` date NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_creation_user_id_4c119038_uniq` (`user_id`,`date`),
  CONSTRAINT `api_creation_user_id_f816e1d0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_creation`
--

LOCK TABLES `api_creation` WRITE;
/*!40000 ALTER TABLE `api_creation` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_creation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_environment`
--

DROP TABLE IF EXISTS `api_environment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_environment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(150) NOT NULL,
  `value` varchar(150) NOT NULL,
  `container_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_environment_container_id_508ad4f1_uniq` (`container_id`,`key`),
  CONSTRAINT `api_environment_container_id_f9617345_fk_api_container_id` FOREIGN KEY (`container_id`) REFERENCES `api_container` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_environment`
--

LOCK TABLES `api_environment` WRITE;
/*!40000 ALTER TABLE `api_environment` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_environment` ENABLE KEYS */;
UNLOCK TABLES;



--
-- Table structure for table `api_link`
--

DROP TABLE IF EXISTS `api_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alias` varchar(150) NOT NULL,
  `container_id` int(11) NOT NULL,
  `link_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_link_container_id_b03cded1_uniq` (`container_id`,`alias`),
  KEY `api_link_link_id_0b51cf7a_fk_api_container_id` (`link_id`),
  CONSTRAINT `api_link_container_id_f36c8fae_fk_api_container_id` FOREIGN KEY (`container_id`) REFERENCES `api_container` (`id`),
  CONSTRAINT `api_link_link_id_0b51cf7a_fk_api_container_id` FOREIGN KEY (`link_id`) REFERENCES `api_container` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_link`
--

LOCK TABLES `api_link` WRITE;
/*!40000 ALTER TABLE `api_link` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_port`
--

DROP TABLE IF EXISTS `api_port`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_port` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `port` int(11) NOT NULL,
  `external` tinyint(1) NOT NULL,
  `expose` varchar(5),
  `container_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_port_container_id_90bf0996_uniq` (`container_id`,`port`),
  CONSTRAINT `api_port_container_id_bc55dbc3_fk_api_container_id` FOREIGN KEY (`container_id`) REFERENCES `api_container` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_port`
--

LOCK TABLES `api_port` WRITE;
/*!40000 ALTER TABLE `api_port` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_port` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_process`
--

DROP TABLE IF EXISTS `api_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_process` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` varchar(150) NOT NULL,
  `status` varchar(100) DEFAULT NULL,
  `detail` longtext,
  `proc` varchar(150) DEFAULT NULL,
  `image_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_process_pid_b1588072_uniq` (`pid`,`image_id`),
  KEY `api_process_image_id_e3ebf0a1_fk_api_image_id` (`image_id`),
  CONSTRAINT `api_process_image_id_e3ebf0a1_fk_api_image_id` FOREIGN KEY (`image_id`) REFERENCES `api_image` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_process`
--

LOCK TABLES `api_process` WRITE;
/*!40000 ALTER TABLE `api_process` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_process` ENABLE KEYS */;
UNLOCK TABLES;







-- /*!40101 SET character_set_client = @saved_cs_client */;


-- /*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

-- /*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
-- /*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
-- !40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS ;
-- /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
-- /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
-- /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
-- /*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-30  2:07:52
