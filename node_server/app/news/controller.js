'use strict';

var Articles = require('./Articles');
var messenger = require('./messenger');
var emit = require('./emit');

export function index(req,res) {
  res.redirect('/news/page/1')
};

export function page(io) {
  return function(req,res) {
    var pageNumber = req.params.page;

    Articles.getValuatedArticles(pageNumber, (err, articles) => {
      if(err) console.log(err);

      console.log('made it into controller')

      messenger.getText(articles, (err, data) => {
        if(err) console.log(err);
        emit.gimme(io, data);
      });

      res.render('news/index',
                 { page : 'positive',
                   articles : ['caleb'] });
    });
  };
}
