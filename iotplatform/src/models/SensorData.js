import axios from "axios";

export default class SensorData {
    static endpoint = "SensorData"
    static extra = "SensorsDevices"

    static getsensorsdevicesensordata(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.extra}/${this.endpoint}/${id}`)
                .then(response => {
                    const model = new this(response.data.data);
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static getsinglesensordata(connectionstring, id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.endpoint}/${connectionstring}/${id}`)
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