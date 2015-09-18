'use strict';

var request = require('request');
var htmlparser = require('htmlparser2');

export function parse(url, cb) {
  var data = '';
  var inBody = false;

  var parser = new htmlparser.Parser({
    onopentagname: name => {
      if(name === 'body') inBody = true;
      else if(name === 'script' || name === 'style') inBody = false;
    },
    ontext: text => {
      if(inBody) data+=text;
    },
    onclosetag: name => {
      if(name === 'body') inBody = false;
      else if(name === 'script' || name === 'style') inBody = true;
    },
    onend: () => {
      cb(null, JSON.stringify(data));
    }
  }, {decodeEntities: true});

  request(url, (err,response,body) => {
    if(err) {
      cb(err)
      throw err;
    }

    parser.write(body);
    parser.end();

  });
}
