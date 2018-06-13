import React from "react";
import { Link } from "react-router-dom";

export default class Top extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = {};
  }

  componentWillMount() {
    this.setState({ text: "Top Page" });
  }

  render() {
    return (
      <div className="container">
        <div className="btn-link">
          <h1>TOP {this.state.text}</h1>
        </div>
        <div className="link-column-wrap">
          <Link to="/profile">プロフィール</Link>
        </div>
      </div>
    );
  }
}
