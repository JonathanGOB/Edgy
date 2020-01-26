import Model from "./Model";
import axios from "axios";

export default class SensorsDevice extends Model {
    static standardroute = "SensorsDevices"
    static relation = "EdgeDevices"

    static getedgedevicesensorsdevices(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.relation}/${id}/${this.standardroute}`)
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
        super(SensorsDevice.endpoint);
    }
}