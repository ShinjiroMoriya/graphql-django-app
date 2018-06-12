var express = require('express');
var proxy = require('http-proxy-middleware');

var NODE_PORT = 4711;
var DJANGO_PORT = process.env.DJANGO_PORT || 8000;

var DEV = process.env.DJANGO_PORT === undefined;

var app = express();

app.get('/', function (req, res) {
    res.send('Hello World!');
});

app.use(proxy("/graphql", {
    "target": 'https://localhost:'+ DJANGO_PORT,
}))

if (DEV === true) {
    var fs = require('fs');
    var https = require('https');
    var options = {
        key:  fs.readFileSync('../localhost.key'),
        cert: fs.readFileSync('../localhost.crt')
    };
    var app = https.createServer(options, app);
}

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
