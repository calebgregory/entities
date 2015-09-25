'use strict';

export function gimme(io, data) {

  console.log('made it into socket');
  io.sockets.emit('news', data.result);

}
