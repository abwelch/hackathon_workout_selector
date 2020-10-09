CREATE TABLE exercises (
    id int PRIMARY KEY AUTO_INCREMENT,
    name varchar(50) NOT NULL,
    descr varchar(200) NOT NULL,
    workoutID int NOT NULL,
    FOREIGN KEY (workoutID) REFERENCES workout_plans(id)
)