import React, { Component } from 'react';

class Html extends Component {
    constructor(props) {
      super(props);
    }
    render() {
        return (
            <html>
                <head>
                    <title>App</title>
                    <link rel="stylesheet" href={`/build/${this.props.asset['main.css']}`} />
                </head>
                <body>
                    <div id="root">{this.props.children}</div>
                    <script id="initial-data" type="text/plain" data-json={this.props.initialData}></script>
                    <script src={`/build/${this.props.asset['main.js']}`}></script>
                </body>
            </html>
        );
    }
};

export default Html;