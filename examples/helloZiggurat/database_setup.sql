SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

-- --------------------------------------------------------
-- Database: `ziggurattest`
--

CREATE DATABASE IF NOT EXISTS `ziggurattest`;
USE `ziggurattest`;

-- --------------------------------------------------------
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
CREATE TABLE IF NOT EXISTS `test` (
  `i` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'index',
  `cts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'created timestamp',
  `upts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'updated timestamp',
  `info` text NOT NULL COMMENT 'info data',
  PRIMARY KEY (`i`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Example test table for Hello Ziggurat example' AUTO_INCREMENT=1 ;

-- --------------------------------------------------------
-- User: `ziggtestuser`
--

CREATE USER `ziggtestuser`@`localhost` IDENTIFIED BY 'password12345';
GRANT ALL PRIVILEGES ON `ziggurattest`.* TO `ziggtestuser`@`localhost`;
FLUSH PRIVILEGES;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
