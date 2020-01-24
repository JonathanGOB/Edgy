<template>
    <div>
        <div>
            <b-form-row class="mt-4">
                <b-col>
                    <label class="mb-0" for="inputName">Name</label>
                    <input
                            type="text"
                            id="inputName"
                            class="form-control"
                            required
                            autofocus
                            v-model="Name"
                    >
                </b-col>
                <b-col>
                    <label class="mb-0 text-dark" for="inputDescription">Description</label>
                    <input
                            type="text"
                            id="inputDescription"
                            class="form-control"
                            v-model="Description"
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
                            v-model="Location"
                            minlength="8"
                            required
                    >
                </b-col>
                <b-col>
                    <b-button class="mt-4" block @click="createEdgeDevice">
                        Create Edge device
                        <font-awesome-icon icon="spinner" v-if="loading" spin/>
                    </b-button>
                </b-col>
            </b-form-row>
            <b-row>
                <b-col>
                    <span style="color:red">{{ error }}</span>
                </b-col>
            </b-row>
        </div>
        <b-container>

        </b-container>
    </div>
</template>

<script>
    //import EdgeDevice from "../models/EdgeDevice";
    import EdgeDevice from "../models/EdgeDevice";

    export default {
        name: "EdgeDevicesTable",
        mounted() {
            // const edgemodel = EdgeDevice;
            // edgemodel.fetchall().then(response => {
            //     this.items = response.data.edgedevices
            // }).catch(error => {
            //     this.items = []
            //     // eslint-disable-next-line no-console
            //     console.log(error)
            // })
        },
        data() {
            return {
                error: "",
                loading: "",
                Description: "",
                Name: "",
                Location: ""
            }
        },

        methods:{
            createEdgeDevice() {
                this.loading = true;
                this.error = "";
                EdgeDevice.create({
                    Name: this.Name,
                    Description: this.Description,
                    Location: this.Location,
                }).then(() => {
                    this.loading = false;
                }).catch((error) => {
                    this.loading = false;
                    this.error = error.response.data.data.message;
                })
            }
        }
    }
</script>

<style scoped>

</style>