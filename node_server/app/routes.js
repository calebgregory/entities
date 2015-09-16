'use strict';

var express = require('express')
  , router  = express.Router();

var home    = require('./home/routes');

router.use('/', home);

export default router;
