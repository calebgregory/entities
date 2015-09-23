'use strict';

var express = require('express')
  , less = require('less-middleware')
  , morgan  = require('morgan')
  , path    = require('path');

var routes  = require('./routes');

var app = module.exports = express();

app.set('port', process.env.PORT || 3000);

app.set('views', __dirname);
app.set('view engine', 'jade');

app.use(less(path.join(process.cwd(),'www')));

app.locals.title = 'Entities';

app.use(morgan('dev'));

app.use(express.static((path.join(process.cwd(),'www'))));
app.use('/', routes);

require('../lib/errorHandler/');

var server = app.listen(app.get('port'), () => {
  var port = server.address().port;
  var mode = app.get('env');

  console.log(`Server listening on port ${port} in ${mode} mode . . .`);
});
