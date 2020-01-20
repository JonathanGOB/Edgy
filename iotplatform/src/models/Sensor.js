import Model from "./Model";
import axios from "axios";

export default class Sensor extends Model {
    static endpoint = "Sensors"

    static getsensorsdevicesensors(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/SensorsDevices/${id}/${this.endpoint}`)
                .then(response => {
                    const model = new this(response.data.data);
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static getedgedevicesensors(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/EdgeDevices/${id}${this.endpoint}`)
                .then(response => {
                    const model = new this(response.data.data);
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }
    constructor() {
        super(Sensor.endpoint);
    }
}