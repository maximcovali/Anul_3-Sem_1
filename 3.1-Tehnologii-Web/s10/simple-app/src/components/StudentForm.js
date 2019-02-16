import React, { Component } from 'react'

class StudentForm extends Component {
  constructor(props){
    super(props)
    this.state = {
      firstName : '',
      lastName : '',
      age : -1,
      email : ''
    }
    this.handleChange = (evt) => {
      this.setState({
        [evt.target.name] : evt.target.value
      })
    }
  }
  render() {
    return (
      <div>
        <form>
            <label for="firstName">First name</label>
            <input type="text" id="firstName" name="firstName" onChange={this.handleChange} />
            <label for="lastName">Last name</label>
            <input type="text" id="lastName" name="lastName" onChange={this.handleChange} />
            <label for="age">Age</label>
            <input type="text" id="age" name="age" onChange={this.handleChange} />
            <label for="email">Email</label>
            <input type="text" id="email" name="email" onChange={this.handleChange} />
            <input type="button" value="add" onClick={() => this.props.onAdd({
              firstName : this.state.firstName,
              lastName : this.state.lastName,
              age : this.state.age,
              email : this.state.email
            })} /> 
        </form>
      </div>
    )
  }
}

export default StudentForm
