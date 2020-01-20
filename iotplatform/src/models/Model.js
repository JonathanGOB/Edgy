import axios from 'axios';

export default class Model{

    constructor(endpoint) {
        this.standardroute = endpoint;
    }

    static fetch(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.standardroute}/${id}`)
                .then(response => {
                    const model = new this(response.data.data);
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static fetchall(){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.standardroute}`)
                .then(response => {
                    const model = new this(response.data.data);
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static delete(id){
        return new Promise((resolve, reject) => {
            axios.delete(`/Api/V1/${this.standardroute}/${id}`)
                .then(response => {
                    const model = new this(response.data.data);
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static update(id, params = {}){
        return new Promise((resolve, reject) => {
            axios.put(`/Api/V1/${this.standardroute}/${id}`,
                {
                    params: params,
                })
                .then(response => {
                    const model = new this(response.data.data);
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }




}