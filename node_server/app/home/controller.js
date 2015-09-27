'use strict';

var Sources = require('./Sources')

export function index(req,res) {
  Sources.getValuatedSources((err,data) => {
    if(err) console.log(err);

    res.render('home/index',
               { page : 'Home',
                 sources : data });
  })
};

