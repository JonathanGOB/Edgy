import axios from 'axios';

export default class Model{


    static fetch(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.standardroute}/${id}`)
                .then(response => {
                    const model = {"data": response.data};
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
                    const model = {"data": response.data};
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
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static create(params = {}) {
        return new Promise((resolve, reject) => {
            axios.post(`/Api/V1/${this.standardroute}`, params)
                .then(response => {
                    const model = {"data": response.data};
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
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }




}