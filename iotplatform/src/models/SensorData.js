import Model from "./Model";
import axios from "axios";

export default class SensorData extends Model {
    static endpoint = "SensorData"

    static getsensorsdevicesensordata(id){
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
        super(SensorData.endpoint);
    }
}