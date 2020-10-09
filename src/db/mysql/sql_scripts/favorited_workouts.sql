CREATE TABLE favorited_workouts (
    id int PRIMARY KEY AUTO_INCREMENT,
    workoutID int NOT NULL,
    userID int NOT NULL,
    FOREIGN KEY (workoutID) REFERENCES workout_plans(id),
    FOREIGN KEY (userID) REFERENCES users(id)
)