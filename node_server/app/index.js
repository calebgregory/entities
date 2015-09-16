'use strict';

var express = require('express')
  , morgan  = require('morgan')
  , sass    = require('node-sass-middleware');

var routes  = require('./routes');

var app = module.exports = express();

app.set('port', process.env.PORT || 3000);

app.set('views', __dirname);
app.set('view engine', 'jade');

app.locals.title = 'Entities';

app.use(morgan('dev'));
app.use(express.static('www'));
app.use(sass({
  dest        : 'www/styles',
  outputStyle : 'compressed',
  prefix      : '/styles',
  sourceMap   : app.get('env') === 'production' ? 'false' : true,
  src         : 'www/styles'
}));

app.use('/', routes);

require('../lib/errorHandler/');

var server = app.listen(app.get('port'), () => {
  var port = server.address().port;
  var mode = app.get('env');

  console.log(`Server listening on port ${port} in ${mode} mode . . .`);
});
