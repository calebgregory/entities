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
    messenger.send(text, err => {
      if(err) throw err;
      messenger.receive((err, entities) => {
        if(err) throw err;
        res.send(entities);
      });
    });
  });
}
