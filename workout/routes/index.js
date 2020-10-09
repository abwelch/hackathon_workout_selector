const request = require('request');
var express = require('express');
const { response } = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Home' });
});

/* GET workout plans page. */
router.get('/workouts', (req, res) => {
  res.render('workouts', { title: 'Workout Plans' });
});

/* GET register exercise page. */
router.get('/register', (req, res) => {
  res.render('register', { title: 'Registration' });
});

/* POST register plans page */
router.post('/register', (req, res) => {
  const { body } = req;
  var json = { 
                "username": body.user_name,
                "email": body.user_email,
                "password": body.user_password,
              };

  var options = {
    url: "http://127.0.0.1:5000/signup",
    method: "POST",
    'headers': {'Content-Type': 'application/json'},
    body: JSON.stringify(json)
  };
  request(options, function (error, response) {
    if (error) throw new Error(error);
    console.log(response.body)});
  res.render('back', {title: "Registration"});
});

/* GET pec exercise page. */
router.get('/pecs', (req, res) => {
  res.render('pecs', { title: 'Pectoral Exercises' });
});

/* GET abs exercise page. */
router.get('/abs', (req, res) => {
  res.render('abs', { title: 'Abdominal Exercises' });
});

/* GET back exercise page. */
router.get('/back', (req, res) => {
  res.render('back', { title: 'Back Exercises' });
});

/* GET shoulders exercise page. */
router.get('/shoulders', (req, res) => {
  res.render('shoulders', { title: 'Shoulder Exercises' });
});

/* GET biceps exercise page. */
router.get('/biceps', (req, res) => {
  res.render('biceps', { title: 'Bicep Exercises' });
});

/* GET tricep exercise page. */
router.get('/triceps', (req, res) => {
  res.render('triceps', { title: 'Tricep Exercises' });
});

/* GET create workout page. */
router.get('/create_workout', (req, res) => {
  res.render('create_workout', { title: 'Create Workout'});
});

/* POST create workout page */
router.post('/create_workout', (req, res) => {
  const { body } = req;
  // userID harded coded for now. needs to be properly pulled when authentication is finished
  var json = JSON.stringify({ 
                "userID": 1,
                "workout_title": body.workout_title,
                "workout_descr": body.workout_descr,
                "exercise_title": body.exercise_title,
                "exercise_descr": body.exercise_descr,
                "exercise_sets": body.exercise_sets,
                "exercise_reps": body.exercise_reps
              });

  var options = {
    url: "http://127.0.0.1:5000/create_workout",
    method: "POST",
    'headers': {'Content-Type': 'application/json'},
    body: json
  };

  request(options, function (error, response) {
    if (error) throw new Error(error);
    console.log(response.body)});

  res.render('create_workout', {title: "Create Workout"});
});

/* GET display workout page. */
router.get('/display_workouts', (req, res) => {
  var options = {
    url: "http://127.0.0.1:5000/retrieve_workouts",
    method: "GET",
    'headers': {'Content-Type': 'application/json'},
  };

  request(options, function (error, response) {
    if (error) throw new Error(error);
    obj = JSON.parse(response.body);
    console.log(obj);
    res.render('display_workouts', obj);});
});

module.exports = router;