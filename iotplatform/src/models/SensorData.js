import Model from "./Model";
import axios from "axios";

export default class SensorData extends Model{
    static standardroute = "SensorData"
    static relations = ["Sensors", "SensorsDevices"]

    static getsensorsensordata(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.relations[0]}/${id}/${this.standardroute}`)
                .then(response => {
                    const model = {"data": response.data};
                    resolve(model);
                })
                .catch(error => {
                    reject(error);
                })
        });
    }


    static getsensorsdevicesensordata(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.relations[1]}/${id}/${this.standardroute}`)
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
        super(SensorData.endpoint);
    }


}