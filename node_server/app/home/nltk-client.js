'use strict';

var amqp = require('amqplib/callback_api');

export function client(data, cb) {
  if(!data) cb((new Error('No input data received')));

  amqp.connect('amqp://localhost', (err, conn) => {
    conn.createChannel((err,ch) => {
      ch.assertQueue('', {exclusive: true}, (err, q) => {
        var corr = generateUuid();
        var message = data;

        console.log(' [x] Requesting message: %s', `${message.slice(0,10)}...${message.slice(-10)}`)

        ch.consume(q.queue, msg => {
          if(msg.properties.correlationId === corr) {
            console.log(' [.] Got %s', msg.content.toString());
            setTimeout(() => { conn.close(); process.exit(0) }, 500);
          }
        }, {noAck: true});

        ch.sendToQueue('nltk_queue',
                      new Buffer(message),
                      { correlationId: corr,
                        replyTo: q.queue });
      });
    });
  });
}

function generateUuid() {
  return Math.random().toString() +
         Math.random().toString() +
         Math.random().toString();
}
