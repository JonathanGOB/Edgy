<template>
    <div>
        <Sidebar>

        </Sidebar>
        <b-container fluid>
            <SensorDevicesTable>

            </SensorDevicesTable>
        </b-container>
    </div>
</template>

<script>
    import Sidebar from "../components/Sidebar";
    import SensorDevicesTable from "../components/SensorDevicesTable";
    export default {
        name: "SensorsDevices",
        components:{
            SensorDevicesTable,
            Sidebar
        },

    }
</script>

<style scoped>

</style>