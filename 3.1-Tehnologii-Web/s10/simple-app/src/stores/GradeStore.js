import axios from 'axios'
import {EventEmitter} from 'fbemitter'

const SERVER = 'https://webtech-2018-hypothetical-andrei.c9users.io'

class GradeStore{
    constructor(){
        this.content = []
        this.emitter = new EventEmitter()
    }
    async getAll(studentId){
        try {
            let response = await axios(`${SERVER}/students/${studentId}/grades`)
            this.content = response.data
            this.emitter.emit('GET_ALL_SUCCESS')
        } catch (e) {
            console.warn(e)
            this.emitter.emit('GET_ALL_ERROR')
        }
    }
    async addOne(studentId, grade){
        try {
            await axios.post(`${SERVER}/students/${studentId}/grades`, grade)
            this.emitter.emit('ADD_SUCCESS')
            this.getAll(studentId)
        } catch (e) {
            console.warn(e)
            this.emitter.emit('ADD_ERROR')
        }
    }
    async deleteOne(studentId, gradeId){
        try {
            await axios.delete(`${SERVER}/students/${studentId}/grades/${gradeId}`)
            this.emitter.emit('DELETE_SUCCESS')
            this.getAll(studentId)
        } catch (e) {
            console.warn(e)
            this.emitter.emit('DELETE_ERROR')
        }
    }
    async saveOne(studentId, gradeId, grade){
        try {
            await axios.put(`${SERVER}/students/${studentId}/grades/${gradeId}`, grade)
            this.emitter.emit('SAVE_SUCCESS')
            this.getAll(studentId)
        } catch (e) {
            console.warn(e)
            this.emitter.emit('SAVE_ERROR')
        }
    }

}

export default GradeStore