<template>
    <div>
        <Sidebar>

        </Sidebar>
        <b-container fluid>
            <b-row>
                <Graph v-bind:data="data">

                </Graph>
            </b-row>
            <b-row>
                <GraphTable v-bind:data="data">

                </GraphTable>
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
                devices: {},
                data: [],
                error: ""
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
                    SensorData.getsensorsdevicesensordata(device.RowKey).then(response => {
                        this.data = response.data.data.sensordata
                    }).catch(error => {
                        this.error = error
                    })
                }).catch(error => {
                    this.error = error
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
                    SensorData.getsensorsensordata(device.RowKey).then(response => {
                        this.data = response.data.data.sensordata
                    }).catch(error => {
                        this.error = error
                    })
                }).catch(error => {
                    this.error = error
                })


            }

        }
    }
</script>

<style scoped>

</style>