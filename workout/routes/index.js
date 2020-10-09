var express = require('express');
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
  const { body } = req
  var json = { 
                username: body.user_name,
                email: body.user_email,
                password: body.user_password,
                title: "back attack"
              }
  res.render('back', json);
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

module.exports = router;