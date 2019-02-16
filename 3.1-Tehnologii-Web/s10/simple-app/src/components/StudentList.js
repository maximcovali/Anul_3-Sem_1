import React, { Component } from 'react'
import Student from './Student'
import StudentStore from '../stores/StudentStore'
import StudentForm from './StudentForm'
import GradeList from './GradeList'

class StudentList extends Component {
  constructor(){
    super()
    this.store = new StudentStore()
    this.state = {
      students : [],
      showGradesFor : -1,
      selectedStudent : null
    }
    this.add = (student) => {
      this.store.addOne(student)
    }
    this.delete = (id) => {
      this.store.deleteOne(id)
    }
    this.save = (id, student) => {
      this.store.saveOne(id, student)
    }
    this.showGrades = (id) => {
      let selected = this.state.students.find((e) => e.id === id)
      this.setState({
        showGradesFor : id,
        selectedStudent : selected
      })
    }
  }
  componentDidMount(){
    this.store.getAll()
    this.store.emitter.addListener('GET_ALL_SUCCESS', () => {
      this.setState({
        students : this.store.content
      })
    })
  }
  render() {
    if (this.state.showGradesFor === -1){
      return (
        <div>
          {
            this.state.students.map((e, i) => <Student item={e} key={i} onDelete={this.delete} onSave={this.save} onSelect={this.showGrades}/>)
          }
          <StudentForm onAdd={this.add} />
        </div>
      )
    }
    else{
      return (
        <GradeList student={this.state.selectedStudent} />  
      )
    }
  }
}

export default StudentList
