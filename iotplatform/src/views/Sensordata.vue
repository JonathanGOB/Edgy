<template>
    <div>
        <Sidebar>
        </Sidebar>
        <b-row>
            <b-col>
                <GraphTable :value="value">
                </GraphTable>
            </b-col>
        </b-row>

    </div>
</template>

<script>
    import Sidebar from "../components/Sidebar";
    import GraphTable from "../components/GraphTable";
    import SensorData from "../models/SensorData";
    import axios from "axios";

    export default {
        name: "Sensordata",
        components: {GraphTable, Sidebar},
        data() {
            return {
                value: [],
                interval: null
            }
        },
        created() {
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;

            SensorData.fetchall().then(response => {
                this.value = response.data.data.sensordata
            })
        },
    }
</script>

<style scoped>

</style>