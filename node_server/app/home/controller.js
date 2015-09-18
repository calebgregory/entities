'use strict';

var parser = require('./parser').parse;
var nltkClient = require('./nltk-client').client;

export function index(req,res) {
  res.render('home/index',
             { page : 'Home' });
};

export function externalWebpage(req,res) {
  var externalWebpage = req.query;

  parser(externalWebpage.url, (err, text) => {
    if(err) throw err;
    nltkClient(text, (err, entities) => {
      if(err) throw err;
      res.send(entities);
    });
  });
}
