var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'We got this!' });
});

/* GET workout plans page. */
router.get('/workouts', (req, res) => {
  res.render('workouts', { title: 'Workout Plans' });
});

module.exports = router;
