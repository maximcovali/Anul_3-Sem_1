import React, { Component } from 'react';

class NumeUnic extends Component{
    constructor(){
        super();
    }

    render() {
        return (
            <li>{this.props.nume}<button onClick={this.props.delete}>X</button></li>
        );
    }
}

export default NumeUnic;