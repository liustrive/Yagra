use easeyagra;
CREATE TABLE `User` (
  `user_name` varchar(32) NOT NULL,
  `user_passwd` varchar(64) NOT NULL,
  `user_email` varchar(100) NOT NULL DEFAULT '',
  `regis_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `user_status` int(4) NOT NULL DEFAULT '0',
  `display_name` varchar(256) NOT NULL DEFAULT '',
  `salt` varchar(32) NOT NULL,
  PRIMARY KEY USING BTREE(`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Tokens` (
  `user_name` varchar(32) NOT NULL,
  `user_token` varchar(64) NOT NULL,
  `token_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY USING BTREE (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `Images` (
  `hashcode` VARCHAR(64) NOT NULL,
  `user_name` varchar(32) NOT NULL,
  `file_name` VARCHAR(64) NOT NULL,
  PRIMARY KEY USING HASH (`hashcode`),
  CONSTRAINT `easeyagra_image_fk` FOREIGN KEY (`user_name`) REFERENCES `User` (`user_name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;