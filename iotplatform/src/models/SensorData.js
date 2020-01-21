import Model from "./Model";
import axios from "axios";

export default class SensorData extends Model{
    static endpoint = "SensorData"
    static relations = ["Sensors", "SensorsDevice"]

    static getsensorsensordata(id){
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


    static getsensorsdevicesensordata(id){
        return new Promise((resolve, reject) => {
            axios.get(`/Api/V1/${this.relations[1]}/${id}/${this.endpoint}`)
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