<template>
    <div>
        <form @submit.prevent>
            <b-form-row class="mt-4">
                <b-col>

                    <label class="mb-0" for="inputName">Name</label>
                    <input
                            type="text"
                            id="inputName"
                            class="form-control"
                            required
                            autofocus
                            v-model="createdevice.name"
                    >
                </b-col>
                <b-col>
                    <label class="mb-0 text-dark" for="inputDescription">Description</label>
                    <input
                            type="text"
                            id="inputDescription"
                            class="form-control"
                            v-model="createdevice.description"
                            minlength="8"
                            required
                    >
                </b-col>
                <b-col>
                    <label class="mb-0 text-dark" for="inputLocation">Location</label>
                    <input
                            type="text"
                            id="inputLocation"
                            class="form-control"
                            v-model="createdevice.location"
                            minlength="8"
                            required
                    >
                </b-col>
                <b-col>
                    <label class="mb-0 text-dark" for="inputProtocol">Protocol</label>
                    <input
                            type="text"
                            id="inputProtocol"
                            class="form-control"
                            v-model="createdevice.protocol"
                            minlength="8"
                            required
                    >
                </b-col>
                <b-col>
                    <label class="mb-0 text-dark" for="inputLocation">Edge device</label>
                    <b-form-select v-model="createdevice.selected" :options="createdevice.options"></b-form-select>
                </b-col>
                <b-col>
                    <b-button class="mt-4" block @click="createSensorDevice">
                        Create Edge device
                        <font-awesome-icon icon="spinner" v-if="createdevice.loading" spin/>
                    </b-button>
                </b-col>
            </b-form-row>
        </form>
        <b-row>
            <b-col>
                <span style="color:red">{{ error }}</span>
            </b-col>
        </b-row>
    </div>
</template>

<script>
    import EdgeDevice from "../models/EdgeDevice";
    import axios from "axios";

    export default {
        name: "SensorDevicesTable",
        mounted() {
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
            EdgeDevice.fetchall().then(response =>{
                this.edgedevices = response.data.data.edgedevices.sort(function (a, b) {
                    return a.RowKey - b.RowKey;
                });

                this.createdevice.options = []
                this.edgedevices.forEach(device => {
                    this.createdevice.options.push(device.Name)
                })
            })
        },
        data(){
            return{
                error:"",
                edgedevices: [],
                createdevice: {
                    options: [],
                    selected: "",
                    loading: false,
                    protocol: "",
                    location: "",
                    name: "",
                    description: ""
                }
            }
        },
        methods:{
            createSensorDevice() {
                this.error = "";
                if (!this.createdevice.protocol || !this.this.createdevice.selected || !this.createdevice.location || !this.createdevice.name){
                    this.error = "fill everything"
                }
                if (this.Name && this.Description && this.Location) {
                    this.loading = true;
                    axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                    EdgeDevice.create({
                        Name: this.Name,
                        Description: this.Description,
                        Location: this.Location,
                    }).then(() => {
                        EdgeDevice.fetchall().then(response => {
                            this.items = response.data.data.edgedevices.sort(function (a, b) {
                                return a.RowKey - b.RowKey;
                            });

                            let id = 0;
                            this.items.forEach(data => {
                                data.id = id
                                data.location = data.PartitionKey
                                id++
                                delete data.PartitionKey
                            })
                        }).catch(error => {
                            this.items = []
                            this.error = error
                        })
                        this.$refs.table.refresh();
                        this.loading = false;
                    }).catch((error) => {
                        this.loading = false;
                        this.error = error.response.data.data.message;
                    })
                }
            }
        }
    }
</script>

<style scoped>

</style>