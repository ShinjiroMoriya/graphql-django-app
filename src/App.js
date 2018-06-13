import React, { Component } from "react";
import { BrowserRouter } from "react-router-dom";
import { renderRoutes } from "react-router-config";
import Routes from "./Routes";

export default class App extends Component {
  render() {
    return <BrowserRouter>{renderRoutes(Routes)}</BrowserRouter>;
  }
}
