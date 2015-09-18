'use strict';

var amqp = require('amqplib/callback_api');

export function send(data, cb) {
  if(!data) cb((new Error('No input data received')));

  amqp.connect('amqp://localhost', (err, conn) => {
    conn.createChannel((err, ch) => {
      var q = 'nltk_away';

      ch.assertQueue(q, {durable: false});
      ch.sendToQueue(q, new Buffer(data));
      console.log(' [x] Sent %s', (`${data.slice(0,10)}...${data.slice(-10)}`));

      setTimeout(() => { conn.close(); cb(); }, 500);
    });
  });
}

export function receive(cb) {
  amqp.connect('amqp://localhost', (err, conn) => {
    conn.createChannel((err, ch) => {
      var q = 'nltk_back';

      ch.assertQueue(q, {durable: false});

      console.log(' [*] Waiting for messages in %s. To exit, press CTRL+C', q);
      ch.consume(q, msg => {
        console.log(' [x] Received %s', `${msg.content.toString().slice(0,20)}...`)
        cb(null, msg);
      }, {noAck: true});
    });
  });
}

function generateUuid() {
  return Math.random().toString() +
         Math.random().toString() +
         Math.random().toString();
}
