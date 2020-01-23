<template>
    <div>
        <b-table striped hover :items="items"></b-table>
    </div>
</template>

<script>
    import EdgeDevice from "../models/EdgeDevice";
    export default {
        name: "EdgeDevicesTable",
        mounted() {
            const edgemodel = EdgeDevice;
            edgemodel.fetchall().then(response => {
                this.items = response.data.edgedevices
            }).catch(error => {
                this.items = []
                // eslint-disable-next-line no-console
                console.log(error)
            })
        },
        data() {
            return {
                items: [

                ]
            }
        }
    }
</script>

<style scoped>

</style>