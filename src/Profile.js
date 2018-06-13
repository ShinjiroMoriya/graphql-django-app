import React from "react";
import { Link } from "react-router-dom";

export default class Profile extends React.Component {
  constructor(props, context) {
    super(props, context);
    this.state = {};
  }

  componentWillMount() {
    this.setState({ text: "Profile Page" });
  }

  render() {
    return (
      <div className="container">
        <h1>プロフィール {this.state.text}</h1>
        <Link to="/">トップへ</Link>
      </div>
    );
  }
}
