var http = require('http'),
    httpProxy = require('http-proxy');

var NODE_PORT = 4711;

var proxy = httpProxy.createProxyServer({});

http.createServer(function(req, res) {
    // For all URLs beginning with /channel proxy to the Node.JS app, for all other URLs proxy to the Django app running on DJANGO_PORT
    if(req.url.indexOf('/render') === 0) {
        // Depending on your application structure you can proxy to a node application running on another port, or serve content directly here
        proxy.web(req, res, { target: 'http://localhost:' + NODE_PORT });

        // Proxy WebSocket requests if needed
        proxy.on('upgrade', function(req, socket, head) {
            proxy.ws(req, socket, head, { target: 'ws://localhost:' + NODE_PORT });
        });
    } else {
        proxy.web(req, res, { target: 'http://localhost:' + process.env.DJANGO_PORT });
    }
}).listen(process.env.PORT);

// Example node application running on another port
http.createServer(function(req, res) {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.write('Request successfully proxied to Node.JS app');
    res.end();
}).listen(NODE_PORT);
