'use strict';

var parser = require('./parser').parse;
var messenger = require('./messenger');

export function index(req,res) {
  res.render('home/index',
             { page : 'Home' });
};

export function externalWebpage(req,res) {
  var externalWebpage = req.query;

  parser(externalWebpage.url, (err, text) => {
    if(err) throw err;
    messenger.tokenize(text, (err, tokens) => {
      if(err) throw err;
      console.log(tokens);
      res.send(tokens);
    })
  });
}
