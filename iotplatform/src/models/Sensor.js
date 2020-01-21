import Model from "./Model";
import axios from "axios";

export default class Sensor extends Model {
    static endpoint = "Sensors"
    static relations = ["SensorDevices", "EdgeDevices"]

    static getsensorsdevicesensors(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.relations[0]}/${id}/${this.endpoint}`)
                .then(response => {
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }

    static getedgedevicesensors(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.relations[1]}/${id}${this.endpoint}`)
                .then(response => {
                    const model = {"data": response.data};
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