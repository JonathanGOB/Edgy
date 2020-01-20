import Model from "./Model";
import axios from "axios";

export default class SensorsDevice extends Model {
    static endpoint = "SensorsDevices"

    static getedgedevicesensorsdevices(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${id}/${this.endpoint}`)
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
        super(SensorsDevice.endpoint);
    }
}