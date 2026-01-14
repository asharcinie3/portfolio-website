CREATE TABLE IF NOT EXISTS `skills` (
`skill_id`          int(11)       NOT NULL AUTO_INCREMENT   COMMENT 'The unique identifier for each skill',
`experience_id`     int(11)       NOT NULL 			        COMMENT 'The exeperienced id referenced from experiences table',
`name`              varchar(100)  NOT NULL			        COMMENT 'The name of the skill',
`skill_level`       int(11)       NOT NULL                  COMMENT 'The level of the skill',
PRIMARY KEY (`skill_id`),
FOREIGN KEY (experience_id) REFERENCES experiences(experience_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Skills I have';

