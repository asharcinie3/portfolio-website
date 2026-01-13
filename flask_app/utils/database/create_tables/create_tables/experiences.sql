CREATE TABLE IF NOT EXISTS `experiences` (
`experience_id`     int(11)       NOT NULL 	 AUTO_INCREMENT     COMMENT 'The unique identifier for each experience',
`position_id`       int(11)       NOT NULL 			            COMMENT 'The position id referenced from postions table',
`name`              varchar(100)  NOT NULL			            COMMENT 'The name of the experience',
`description`       varchar(500)  NOT NULL                      COMMENT 'A description of the experience',
`hyperlink`         varchar(500)  DEFAULT NULL                  COMMENT 'A link to learn more about the experience',
PRIMARY KEY (`experience_id`),
FOREIGN KEY (position_id) REFERENCES positions(position_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Experiences I have';

