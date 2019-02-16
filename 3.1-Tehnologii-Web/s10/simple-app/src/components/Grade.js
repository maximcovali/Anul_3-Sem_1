import React, { Component } from 'react'

class Grade extends Component {
  constructor(props){
    super(props)
    this.state = {
      isEditing : false,
      value : this.props.item.value,
      subject : this.props.item.subject
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
          a             
          <input type="text" id="value" name="value" onChange={this.handleChange} value={this.state.value} />
          in
          <input type="text" id="subject" name="subject" onChange={this.handleChange} value={this.state.subject} />. 
          <input type="button" value="cancel" onClick={() => this.setState({isEditing : false})} />
          <input type="button" value="save" onClick={() => { 
              this.props.onSave(item.id, {
                value : this.state.value,
                subject : this.state.subject
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
          a {item.value} in {item.subject}
          <input type="button" value="delete" onClick={() => this.props.onDelete(item.id)} />
          <input type="button" value="edit" onClick={() => this.setState({isEditing : true})} />
        </div>
      )
    }
  }
}

export default Grade
