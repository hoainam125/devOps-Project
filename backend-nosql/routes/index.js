var express = require('express');
var router = express.Router();

router.use((req, res, next) => {
  res.locals.user = req.session.user;
  if (!res.locals.user) {
    res.locals.user = {}
  }
  next();
})

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'WUW' });
});

router.get('/signin', (req, res, next) => {
  if (req.session.user) {
    res.redirect('/dashboard');
    return ;
  }

  res.render('signin');
});

router.get('/signup', (req, res, next) => {
  if (req.session.user) {
    res.redirect('/dashboard');
    return ;
  }

  res.render('signup');
});

router.get('/dashboard', (req, res, next) => {
  if (!req.session.user) {
    res.redirect('/login');
    return ;
  }

  res.render('dashboard', {user: req.session.user});
});

module.exports = router;
