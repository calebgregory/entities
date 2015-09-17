'use strict';

export function index(req,res) {
  res.render('home/index',
             { page : 'Home' });
};

export function externalWebpage(req,res) {
  res.send(req.query);
}
