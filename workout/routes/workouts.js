var express = require('express');
var router = express.Router();

/* GET workout plans page. */
router.get('/workouts', function(req, res) {
  res.render('workouts', { title: 'Workout Plans' });
});

module.exports = router;
