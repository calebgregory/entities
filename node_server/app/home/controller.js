'use strict';
var parser = require('./parser').parse;

export function index(req,res) {
  res.render('home/index',
             { page : 'Home' });
};

export function externalWebpage(req,res) {
  var externalWebpage = req.query;
  parser(externalWebpage.url, data => {
    res.send(data);
  })
}
