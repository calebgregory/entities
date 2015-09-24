'use strict';

var Articles = require('./Articles');
var ac = require('./article-content');

export function index(req,res) {
  res.redirect('/news/page/1')
};

export function positive(req,res) {
  var pageNumber = req.params.page;

  Articles.getValuatedArticles(pageNumber, (err, articles) => {
    res.render('news/index',
               { page : 'positive',
                 articles : articles });
  });
};
