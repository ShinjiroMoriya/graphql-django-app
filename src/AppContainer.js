import React from "react";
import { withRouter } from "react-router-dom";
import { renderRoutes } from "react-router-config";
import { Router } from "react-router-dom";

class AppContainer extends React.Component {
  constructor(props, context) {
    super(props, context);
    if (window.location) {
      this.documentTitle(window.location.pathname);
    }
  }

  documentTitle(pagename) {
    const c_title = "APP";
    const meta = {
      "/": c_title,
      "/profile": `プロフィール｜${c_title}`
    };
    document.title = meta[pagename]
      ? meta[pagename]
      : `ページが存在しません｜${c_title}`;
  }

  componentWillMount() {
    this.props.history.listen((location, action) => {
      if (this.props.location.pathname === location.pathname) {
        window.location.href = location.pathname;
      } else {
        this.documentTitle(location.pathname);
        window.previousLocation = this.props.location;
        window.scrollTo(0, 0);
      }
    });
  }

  render() {
    return (
      <Router history={this.props.history}>
        {renderRoutes(this.props.route.routes)}
      </Router>
    );
  }
}

export default withRouter(AppContainer);
