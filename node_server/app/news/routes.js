'use strict';

var express = require('express')
  , router  = express.Router();

var ctrl = require('./controller');

router.get('/', ctrl.index);
router.get('/negative', ctrl.negative);
router.get('/positive', ctrl.positive);

module.exports = router;
