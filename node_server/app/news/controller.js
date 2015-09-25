'use strict';

var Articles = require('./Articles');
var messenger = require('./messenger');
var emit = require('./emit');

var newsSourceMap = {
  'hp': 'Huffington Post',
  'cnn': 'CNN',
  'npr': 'NPR',
  'aj': 'Al Jazeera',
  'fn': 'Fox News',
  'nyt': 'New York Times'
};

export function index(req,res) {
  res.redirect('/')
};

export function page(io) {
  return function(req,res) {

    var pageNumber = req.params.page;

    var newsSource = newsSourceMap[req.params.source];

    Articles.getValuatedArticles(newsSource, pageNumber, (err, articles) => {
      if(err) console.log(err);

      console.log('made it into controller')

      messenger.getText(articles, (err, data) => {
        if(err) console.log(err);
        emit.gimme(io, data);
      });

      res.render('news/index',
                 { source : newsSource,
                   reqsrc : req.params.source,
                   page : pageNumber });
    });
  };
}
