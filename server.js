import express from "express";
import React from "react";
import ReactDOMServer from "react-dom/server";
import proxy from "http-proxy-middleware";
import asset from "./build/asset-manifest.json";
import https from "https";
import http from "http";
import path from "path";
import { readFile, readFileSync } from "fs";
import StaticRouter from "react-router-dom/StaticRouter";
import { renderRoutes } from "react-router-config";
import Routes from "./src/Routes";

if (typeof window === "undefined") {
  global.window = {};
}

const PORT = process.env.PORT || 3000;
const DJANGO_PORT = process.env.DJANGO_PORT || 8000;
const DEV = process.env.DJANGO_PORT === undefined;

let app = express();

app.use(
  proxy("/graphql", {
    target: "http://localhost:" + DJANGO_PORT
  })
);

app.use("/build", express.static("build"));
app.get("/favicon.ico", (req, res) => res.status(204));
app.get("*", (req, res, next) => {
  const filePath = path.resolve(__dirname, "build", "index.html");

  readFile(filePath, "utf8", (err, htmlData) => {
    if (err) {
      console.error("err", err);
      return res.status(404).end();
    }
    const context = {};

    const html = ReactDOMServer.renderToStaticMarkup(
      <StaticRouter location={req.url} context={context}>
        {renderRoutes(Routes)}
      </StaticRouter>
    );

    return res.send(
      htmlData
        .replace('<div id="root"></div>', `<div id="root">${html}</div>`)
        .replace(
          '<script type="text/javascript" src="/static/',
          '<script type="text/javascript" src="/build/static/'
        )
        .replace(
          '<link rel="shortcut icon" href="/favicon.ico">',
          '<link rel="shortcut icon" href="/build/favicon.ico">'
        )
    );
  });
});

if (DEV === true) {
  const options = {
    key: readFileSync("../localhost.key"),
    cert: readFileSync("../localhost.crt")
  };
  https.createServer(options, app).listen(PORT);
} else {
  http.createServer(app).listen(PORT);
}
