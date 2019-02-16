import axios from 'axios'
import {EventEmitter} from 'fbemitter'

const SERVER = 'https://webtech-2018-hypothetical-andrei.c9users.io'

class StudentStore{
    constructor(){
        this.content = []
        this.emitter = new EventEmitter()
    }
    async getAll(){
        try {
            let response = await axios(`${SERVER}/students`)
            this.content = response.data
            this.emitter.emit('GET_ALL_SUCCESS')
        } catch (e) {
            console.warn(e)
            this.emitter.emit('GET_ALL_ERROR')
        }
    }
    async addOne(student){
        try {
            await axios.post(`${SERVER}/students`, student)
            this.emitter.emit('ADD_SUCCESS')
            this.getAll()
        } catch (e) {
            console.warn(e)
            this.emitter.emit('ADD_ERROR')
        }
    }
    async deleteOne(id){
        try {
            await axios.delete(`${SERVER}/students/${id}`)
            this.emitter.emit('DELETE_SUCCESS')
            this.getAll()
        } catch (e) {
            console.warn(e)
            this.emitter.emit('DELETE_ERROR')
        }
    }
    async saveOne(id, student){
        try {
            await axios.put(`${SERVER}/students/${id}`, student)
            this.emitter.emit('SAVE_SUCCESS')
            this.getAll()
        } catch (e) {
            console.warn(e)
            this.emitter.emit('SAVE_ERROR')
        }
    }

}

export default StudentStore