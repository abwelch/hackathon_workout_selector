CREATE TABLE exercises (
    id int PRIMARY KEY AUTO_INCREMENT,
    title varchar(50) NOT NULL,
    descr varchar(200) NOT NULL,
    sets int NOT NULL,
    reps int NOT NULL,
    workoutID int NOT NULL,
    FOREIGN KEY (workoutID) REFERENCES workout_plans(id)
)