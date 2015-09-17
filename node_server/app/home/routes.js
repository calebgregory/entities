'use strict';

var express = require('express')
  , router  = express.Router();

var ctrl = require('./controller');

router.get('/', ctrl.index);
router.get('/external-webpage', ctrl.externalWebpage);

module.exports = router;
