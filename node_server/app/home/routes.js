'use strict';

var express = require('express')
  , router  = express.Router();

var ctrl = require('./controller');

router.get('/', ctrl.index);

module.exports = router;
