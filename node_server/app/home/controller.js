'use strict';

export function index(req,res) {
  res.render('home/index',
             { page : 'Home' });
};
