import React, { Component } from 'react'
import GradeStore from '../stores/GradeStore'
import Grade from './Grade'
import GradeAddForm from './GradeAddForm'

class GradeList extends Component {
  constructor(props){
    super(props)
    this.state = {
      grades : []
    }
    this.store = new GradeStore()
    this.add = (grade) => {
      this.store.addOne(this.props.student.id, grade)
    }
    this.delete = (gradeId) => {
      this.store.deleteOne(this.props.student.id, gradeId)
    }
    this.save = (gradeId, grade) => {
      this.store.saveOne(this.props.student.id, gradeId, grade)
    }
  }
  componentDidMount(){
    this.store.getAll(this.props.student.id)
    this.store.emitter.addListener('GET_ALL_SUCCESS', () => {
      this.setState({
        grades : this.store.content
      })
    })
  }

  render() {
    return (
      <div>
        <div>
          I am the list of grades for {this.props.student.firstName}
        </div>
        <div>
          {this.state.grades.map((e, i) => <Grade item={e} key={i} onDelete={this.delete} onSave={this.save} />)}  
        </div>
        <div>
          <GradeAddForm onAdd={this.add} />
        </div>
      </div>
    )
  }
}

export default GradeList
