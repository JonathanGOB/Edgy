<template>
    <div>
        <Sidebar>
        </Sidebar>
        <b-container fluid>
                <EdgeDevicesTable>
                </EdgeDevicesTable>
        </b-container>
    </div>
</template>

<script>
    import Sidebar from "../components/Sidebar";
    import EdgeDevicesTable from "../components/EdgeDevicesTable";

    export default {
        name: "Edgedevices",
        components: {
            Sidebar,
            EdgeDevicesTable
        }
    }
</script>

<style scoped>

</style>