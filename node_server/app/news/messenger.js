'use strict';

var celery = require('node-celery');

export function getText(articles, cb) {

  console.log('made it into messenger');

  var urls = articles.map(article => { return article.url; });

  var client = celery.createClient({
    CELERY_BROKER_URL: 'amqp://guest:guest@localhost:5672//',
    CELERY_RESULT_BACKEND: 'amqp',
    CELERY_TASK_SERIALIZER: 'json'
  });

  client.on('connect', () => {

    console.log ('made it into celery')
    urls.forEach(url => {
      var result = client.call('framework.tasks.visit', [url]);
      setTimeout(() => {
        result.on('ready', data => {
          cb(null, data);
        });
      }, 250);
    })
  });
}
