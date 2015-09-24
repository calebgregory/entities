'use strict';

var pg = require('pg');
var conString = process.env.API_DB_URL || 'postgres://localhost/testdb2';

export function getValuatedArticles(newsSource, pageNumber, cb) {

  pg.connect(conString, (err,client,done) => {

    console.log('made it into Articles model');

    if(err) {
      return console.error('error fetching client from pool', err)
    }

    var numberPerPage = 5;
    var start = (1 - pageNumber) * numberPerPage;

    console.log('newSource:', newsSource)
    // select 'positive' news stories, 5 at a time, starting at the page_number * 5
    // then send to controller
    client.query("SELECT * FROM linkswithsentiment WHERE sourcename = $1 AND value > 0 ORDER BY created DESC LIMIT $2 OFFSET $3;",
                 [newsSource.toString(), numberPerPage.toString(), start.toString()],
                 (err, result) => {

      if(err) {
        return console.error('error running query', err);
      }

      console.log(result.rows);

      cb(null, result.rows)
      client.end();

    });

  });

}
