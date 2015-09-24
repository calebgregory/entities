'use strict';

var express = require('express')
  , router  = express.Router();

var home    = require('./home/routes');
var news    = require('./news/routes')

router.use('/', home);
router.use('/news', news)


export default router;
