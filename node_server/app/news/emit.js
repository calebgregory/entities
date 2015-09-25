'use strict';

export function gimme(io, data) {

  io.sockets.emit('news', data.result);

}
