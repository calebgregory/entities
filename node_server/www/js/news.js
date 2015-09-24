var socket = io()

socket.on('connect', obj => {
  console.log(socket.id);
})

socket.on('news', function(msg) {
  console.log(msg);
  socket.emit('my other event', { my: 'data' });
});
