'use strict';

var celery = require('node-celery');

export function getText(articles, cb) {

  console.log('made it into messenger');

  var articles = articles.map(article => {
    return {
      url : article.url,
      sentimentValue : article.value
    };
  });

  var client = celery.createClient({
    CELERY_BROKER_OPTIONS: {
      host: 'local',
      port: '5672',
      CELERY_RESULT_BACKEND: 'amqp://',
      CELERY_TASK_SERIALIZER: 'json'
    }
  });

  client.on('error', err => {
    console.log(err);
  })

  client.on('connect', () => {

    console.log ('made it into celery')

    articles.forEach(article => {
      var result = client.call('framework.tasks.visit', [article.url, article.sentimentValue]);
      console.log('called task')

      setTimeout(() => {
        result.on('ready', data => {
          console.log(data)
          cb(null, data);
        });
      }, 250);

    });

  });
}
