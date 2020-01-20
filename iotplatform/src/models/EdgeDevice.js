import Model from "./Model";

export default class EdgeDevice extends Model {
    static endpoint = "EdgeDevices"

    constructor() {
        super(EdgeDevice.endpoint);
    }
}