'use strict';

var pg = require('pg');
var conString = process.env.API_DB_URL || 'postgres://localhost/testdb2';

export function getValuatedArticles(pageNumber, cb) {
  pg.connect(conString, (err,client,done) => {

    console.log('made it into Articles model');

    if(err) {
      return console.error('error fetching client from pool', err)
    }

    var numberPerPage = 5;
    var start = pageNumber * numberPerPage;

    // select 'positive' news stories, 5 at a time, starting at the page_number * 5
    // then send to controller
    client.query('SELECT * FROM linkswithsentiment WHERE value > 0 ORDER BY created DESC LIMIT $1 OFFSET $2;',
                 [numberPerPage.toString(), start.toString()],
                 (err, result) => {

      if(err) {
        return console.error('error running query', err);
      }

      cb(null, result.rows)
      client.end();

    });

  });

}
