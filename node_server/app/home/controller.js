'use strict';

var parser = require('./parser').parse;
var messenger = require('./messenger');
var Sources = require('./Sources')

export function index(req,res) {
  Sources.getValuatedSources((err,data) => {
    if(err) console.log(err);

    console.log(data);
    res.render('home/index',
               { page : 'Home',
                 sources : data });
  })
};

