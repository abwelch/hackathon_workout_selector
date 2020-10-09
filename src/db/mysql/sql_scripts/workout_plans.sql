CREATE TABLE workout_plans (
    id int PRIMARY KEY AUTO_INCREMENT,
    upvotes int NOT NULL,
    title varchar(50) NOT NULL, 
    descr varchar(300) NOT NULL,
    total_exercises int NOT NULL,
    creatorID int NOT NULL,
    FOREIGN KEY (creatorID) REFERENCES users(id)
)