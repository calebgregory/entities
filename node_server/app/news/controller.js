'use strict';

var Articles = require('./Articles');
var messenger = require('./messenger');

export function index(req,res) {
  res.redirect('/news/page/1')
};

export function positive(req,res) {
  var pageNumber = req.params.page;

  Articles.getValuatedArticles(pageNumber, (err, articles) => {
    messenger.getText(articles[0].url)
    res.render('news/index',
               { page : 'positive',
                 articles : ['caleb'] });
  });
};
