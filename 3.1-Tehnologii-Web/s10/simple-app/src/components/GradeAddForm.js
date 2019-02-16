import React, { Component } from 'react'

class GradeAddForm extends Component {
  constructor(props){
    super(props)
    this.state = {
      subject : '',
      value : -1
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
            <label for="subject">Subject</label>
            <input type="text" id="subject" name="subject" onChange={this.handleChange} />
            <label for="value">Value</label>
            <input type="text" id="value" name="value" onChange={this.handleChange} />
            <input type="button" value="add" onClick={() => this.props.onAdd({
              subject : this.state.subject,
              value : this.state.value
            })} /> 
        </form>
      </div>
    )
  }
}

export default GradeAddForm
