<template>
    <div>
        <Sidebar>

        </Sidebar>
        <b-container fluid>
            <b-row>
                <Graph :sensors="sensors" v-bind:device="device" :value="item">

                </Graph>
            </b-row>
            <b-row>
                <b-container fluid>
                <GraphTable v-bind:device="device" :value="item">

                </GraphTable>
                </b-container>
            </b-row>
            <b-row>
                <b-col>
                    <div>
                        <span style="color:red">{{ error }}</span>
                    </div>
                </b-col>

            </b-row>
        </b-container>
    </div>
</template>

<script>
    import Sidebar from "../components/Sidebar";
    import Graph from "../components/Graph";
    import GraphTable from "../components/GraphTable";
    import SensorsDevice from "../models/SensorsDevice";
    import SensorData from "../models/SensorData";
    import Sensor from "../models/Sensor";
    import axios from "axios";
    export default {
        name: "SpecifickSensordata",
        components: {GraphTable, Graph, Sidebar},
        data(){
            return{
                sensors: null,
                devices: {},
                device: "",
                item: [],
                error: "",
                interval: null,
            }
        },
        created() {
            let level = this.$route.params.level
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
            if (level == "sensorsdevice"){
                SensorsDevice.fetchall().then(response => {
                    let items = response.data.data.sensorsdevices.sort(function (a, b) {
                        return a.RowKey - b.RowKey;
                    });

                    let id = 0;
                    this.devices = {}
                    items.forEach(data => {
                        data.location = data.PartitionKey
                        this.devices[id] = data
                        id++
                    })

                }).then(() => {
                    let id = this.$route.params.id
                    let device = this.devices[id]
                    this.device = this.devices[id]
                    SensorData.getsensorsdevicesensordata(device.RowKey).then(response => {
                        response = response.data.data.sensordata
                        response = response.sort(function (a, b) {
                            return new Date(a.Timestamp) - new Date(b.Timestamp);
                        });

                        this.item = response
                        this.interval = setInterval(this.update, 2000)
                        Sensor.getsensorsdevicesensors(this.device.RowKey).then(response =>
                        {
                            this.sensors = response.data.data.sensors
                        })
                    }).catch(error => {
                        this.error = error.response.data.message
                    })
                }).catch(error => {
                    this.error = error.response.data.message
                })
            }

            if (level == "sensor"){
                Sensor.fetchall().then(response => {
                    let items = response.data.data.sensors.sort(function (a, b) {
                        return a.RowKey - b.RowKey;
                    });

                    let id = 0;
                    this.devices = {}
                    items.forEach(data => {
                        data.location = data.PartitionKey
                        this.devices[id] = data
                        id++
                    })

                }).then(() => {
                    let id = this.$route.params.id
                    let device = this.devices[id]
                    this.device = this.devices[id]
                    SensorData.getsensorsensordata(device.RowKey).then(response => {
                        response = response.data.data.sensordata
                        response = response.sort(function (a, b) {
                            return new Date(a.Timestamp) - new Date(b.Timestamp);
                        });

                        this.item = response
                        this.interval = setInterval(this.update, 2000)
                    }).catch(error => {
                        this.error = error.response.data.data.message
                    })
                }).catch(error => {
                    this.error = error.response.data.data.message
                })
            }
        },

        methods: {
            update(){
                let level = this.$route.params.level
                if(level == "sensor") {
                    SensorData.getsensorsensordata(this.device.RowKey).then(response => {
                        response = response.data.data.sensordata
                        response = response.sort(function (a, b) {
                            return new Date(a.Timestamp) - new Date(b.Timestamp);
                        });
                        this.item = response
                    }).catch(error => {
                        this.error = error.response.data.data.message
                    })
                }
                else if (level == "sensorsdevice"){
                    SensorData.getsensorsdevicesensordata(this.device.RowKey).then(response => {
                        response = response.data.data.sensordata
                        response = response.sort(function (a, b) {
                            return new Date(a.Timestamp) - new Date(b.Timestamp);
                        });
                        this.item = response
                    }).catch(error => {
                        this.error = error.response.data.message
                    })
                }
            },

        },
        // eslint-disable-next-line no-unused-vars
        beforeRouteLeave (to, from, next) {
            clearInterval(this.interval)
            next()
        }
    }
</script>

<style scoped>

</style>