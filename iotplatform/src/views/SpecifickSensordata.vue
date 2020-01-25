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
    export default {
        name: "SpecifickSensordata",
        components: {GraphTable, Graph, Sidebar},
        data(){
            return{
                data: []
            }
        },
        created() {

        }
    }
</script>

<style scoped>

</style>