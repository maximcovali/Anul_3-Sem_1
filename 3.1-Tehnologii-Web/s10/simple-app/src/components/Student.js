import React, { Component } from 'react'

class Student extends Component {
  constructor(props){
    super(props)
    this.state = {
      isEditing : false,
      firstName  : this.props.item.firstName,
      lastName : this.props.item.lastName,
      age : this.props.item.age,
      email : this.props.item.email
    }
    this.handleChange = (evt) => {
      this.setState({
        [evt.target.name] : evt.target.value
      })
    }
  }
  render() {
    let {item} = this.props
    if (this.state.isEditing){
      return (
        <div>
          I am             
          <input type="text" id="firstName" name="firstName" onChange={this.handleChange} value={this.state.firstName} />  
          <input type="text" id="lastName" name="lastName" onChange={this.handleChange} value={this.state.lastName} />. 
          My age is  
          <input type="text" id="age" name="age" onChange={this.handleChange} value={this.state.age} />
          and i can be contacted at
          <input type="text" id="email" name="email" onChange={this.handleChange} value={this.state.email} />
          <input type="button" value="cancel" onClick={() => this.setState({isEditing : false})} />
          <input type="button" value="save" onClick={() => { 
              this.props.onSave(item.id, {
                firstName : this.state.firstName,
                lastName : this.state.lastName,
                age : this.state.age,
                email : this.state.email
              })
              this.setState({isEditing : false})
            }
          } />
        </div>
      )
    }
    else{
      return (
        <div>
          I am {item.firstName} {item.lastName}. My age is {item.age} and i can be contacted at {item.email}
          <input type="button" value="delete" onClick={() => this.props.onDelete(item.id)} />
          <input type="button" value="edit" onClick={() => this.setState({isEditing : true})} />
          <input type="button" value="show grades" onClick={() => this.props.onSelect(item.id)} />
        </div>
      )
    }
  }
}

export default Student
