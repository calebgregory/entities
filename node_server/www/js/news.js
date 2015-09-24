var socket = io()

var articles = document.getElementsByClassName('articles')[0];

socket.on('connect', obj => {
  console.log('>> hello, you are connected on',socket.id);
})

socket.on('news', msg => {
  msg = JSON.parse(msg);

  var article = document.createElement('DIV');
  article.classList.add('article')

  var h1 = document.createElement('H1');
  h1.classList.add('headline');
  var textNode = document.createTextNode(msg.headline);
  h1.appendChild(textNode);
  article.appendChild(h1);

  var content = document.createElement('DIV');
  content.classList.add('content');
  article.appendChild(content);

  msg.content.forEach(paragraph => {
    var p = document.createElement('P');
    var textNode = document.createTextNode(paragraph);
    p.appendChild(textNode);
    content.appendChild(p);
  });

  articles.appendChild(article);
});

function generateHeadline(msg) {
  //var newDiv = $('.articles').append($('div'));
  //newDiv.addClass('article');
  //var newHeadline = newDiv.append($('h2'));
  //newHeadline.addClass('headline').text(msg.headline);
}
