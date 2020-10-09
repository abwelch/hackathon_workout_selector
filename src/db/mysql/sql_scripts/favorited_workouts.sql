CREATE TABLE favorited_workouts (
    id int PRIMARY KEY AUTO_INCREMENT,
    int workoutID NOT NULL,
    int userID NOT NULL,
    FOREIGN KEY (workoutID) REFERENCES workout_plans(id),
    FOREIGN KEY (userID) REFERENCES users(id)
)