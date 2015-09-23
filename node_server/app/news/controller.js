'use strict';

export function index(req,res) {
  res.render('news/index',
             { page : 'news' });
};

export function positive(req,res) {
  res.render('news/index',
             { page : 'positive' });
};

export function negative(req,res) {
  res.render('news/index',
             { page : 'negative' });
};
