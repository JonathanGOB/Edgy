<template>
    <div>
        <Sidebar>

        </Sidebar>
        <b-container fluid>
            <SensorsTable>

            </SensorsTable>
        </b-container>
    </div>
</template>

<script>
    import Sidebar from "../components/Sidebar";
    import SensorsTable from "../components/SensorsTable";
    export default {
        name: "Sensors",
        components: {SensorsTable, Sidebar},

    }
</script>

<style scoped>

</style>