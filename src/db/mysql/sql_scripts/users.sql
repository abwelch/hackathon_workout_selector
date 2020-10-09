CREATE TABLE users (
    id int PRIMARY KEY AUTO_INCREMENT,
    username varchar(30) NOT NULL,
    email varchar(60) NOT NULL,
    password varchar(32) NOT NULL
)