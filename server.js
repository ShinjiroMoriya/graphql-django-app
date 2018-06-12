import express from 'express';
import React from 'react';
import ReactDOMServer from 'react-dom/server';
import NodeJsx from 'node-jsx';
import proxy from 'http-proxy-middleware';
NodeJsx.install({harmony: true});
import Html from './src/Html';
import App from './src/App';
import asset from './build/asset-manifest.json';
import {readFileSync} from 'fs';
import https  from 'https';
import http from 'http';

const PORT = process.env.PORT || 3000;

const initialData = {
    logo: `/build/${asset['static/media/logo.svg']}`
};
const DJANGO_PORT = process.env.DJANGO_PORT || 8000;
const DEV = process.env.DJANGO_PORT === undefined;

let app = express();

app.use(proxy("/graphql", {
    "target": 'http://localhost:'+ DJANGO_PORT,
}))

app.use('/build', express.static('build'));
app.get('/favicon.ico', (req, res) => res.status(204))
app.get('/', (req, res) => {
    res.status(200);
    res.setHeader('Content-Type', 'text/html');
    res.end(
        ReactDOMServer.renderToStaticMarkup(
            <Html asset={asset} initialData={JSON.stringify(initialData)}>
                <App {...initialData} />
            </Html>
        )
    );
});

if (DEV !== true) {
    const options = {
        key:  readFileSync('../localhost.key'),
        cert: readFileSync('../localhost.crt')
    };
    https.createServer(options, app).listen(PORT);
} else {
    http.createServer(app).listen(PORT);
}
