<template>
    <div class="home">

        <Sidebar>
        </Sidebar>
        <div class="page-content p-5">
            <EdgeDevicesTable>
            </EdgeDevicesTable>
        </div>
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
    .page-content {
        width: calc(100% - 11rem);
        margin-left: 14rem;
        transition: all 0.4s;
    }
</style>