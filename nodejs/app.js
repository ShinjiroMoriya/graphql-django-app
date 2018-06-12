//app.use('/', proxy('http://localhost:' + DJANGO_PORT));
//
//app.listen(NODE_PORT);

var express = require('express');
var proxy = require('http-proxy-middleware');

var NODE_PORT = 4711;

var app = express();

app.get('/', function (req, res) {
  res.send('Hello World!');
});

app.use('/graphql', proxy('http://127.0.0.1:'+ process.env.DJANGO_PORT));
app.listen(NODE_PORT);

//var http = require('http'),
//    httpProxy = require('http-proxy');
//
//var NODE_PORT = 4711;
//
//var proxy = httpProxy.createProxyServer({});
//
//http.createServer(function(req, res) {
//    console.log('foo')
//    if(req.url.indexOf('/render') === 0) {
//        console.log('hoge')
//        proxy.web(req, res, { target: 'http://localhost:' + NODE_PORT });
//
//        // Proxy WebSocket requests if needed
//        proxy.on('upgrade', function(req, socket, head) {
//            proxy.ws(req, socket, head, { target: 'ws://localhost:' + NODE_PORT });
//        });
//    } else {
//        proxy.web(req, res, { target: 'http://localhost:' + process.env.DJANGO_PORT });
//    }
//}).listen(process.env.PORT);
//
//// Example node application running on another port
//http.createServer(function(req, res) {
//    res.writeHead(200, { 'Content-Type': 'text/plain' });
//    res.write('Request successfully proxied to Node.JS app');
//    res.end();
//}).listen(NODE_PORT);
