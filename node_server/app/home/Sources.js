'use strict;'

var pg = require('pg');
var conString = process.env.SENTIMENT_DB_URL || 'postgres://localhost/testdb';

export function getValuatedSources(cb) {

  pg.connect(conString, (err,client,done) => {

    if(err) {
      return console.error('error fetching client from pool', err);
    }

    client.query(
      'SELECT  S.sourceid, S.name, SUM(sv.value), COUNT(vl.linkid) '+
      'FROM sources AS S '+
      'INNER JOIN visitedLinks AS VL '+
      'ON VL.sourceid = S.sourceid '+
      'INNER JOIN associations AS A '+
      'ON A.linkid = VL.linkid '+
      'INNER JOIN sentimentval AS SV '+
      'ON SV.word = A.word '+
      'GROUP BY S.sourceid, S.name '+
      'ORDER BY SUM(SV.value) DESC;',
      [],
      (err,result) => {
        if(err) return console.error('error running query', err);

        cb(null, result.rows);
        client.end();

      });

  });

}
