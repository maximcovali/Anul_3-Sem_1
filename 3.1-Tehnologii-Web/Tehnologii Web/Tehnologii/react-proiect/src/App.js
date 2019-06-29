import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import NumeUnic from "./NumeUnic";

class App extends Component {
  constructor(){
    super(); // ne permite sa folosim cuvantul this in javascript
    this.state = {
      numes: [],
      numeCurent: ""
    };
  }

  onInputChange = e => {
    this.setState({numeCurent: e.target.value})
  }

  onClick = () => {
    // (adaug la vechea lista valori noi)
    let numeCopy = this.state.numes.slice(); // creez o copie identica
    numeCopy.push(this.state.numeCurent);   // adaug noul nume la sfarsitul listei

    // set the state properly
    this.setState({ numes: numeCopy, numeCurent: ""}) //nume curent devine din nou un empty string
  }

  stergeNume = i => {
    let numeCopy = this.state.numes.slice();

    numeCopy.splice(i, 1);
    this.setState ({ numes: numeCopy});
  }

    render() {
      // vreau o lista cu numele
      let listaNumeUl = this.state.numes.map((e, index) => {
        return (
        <NumeUnic nume={e} delete={() => this.stergeNume()}/>
        );
      });

      return (
        <div>
          <input placeholder="Introduceti numele" value={this.state.numeCurent}
          onChange = {this.onInputChange} />
          <button onClick ={this.onClick} >Adauga!</button>
          <br />
          {this.state.numes.length === 0 ? "Nu a fost adaugat nici un nume pana acum" : <ul>{listaNumeUl} </ul>}
        </div>
      );
    }
  }

export default App;
