'use strict';

var express = require('express')
  , router  = express.Router();

var ctrl = require('./controller');

module.exports = function(io) {
  router.get('/', ctrl.index);
  router.get('/page/:page', ctrl.positive(io));

  return router;
};
