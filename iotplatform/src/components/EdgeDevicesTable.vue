<template>
    <div>
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
                        <b-button class="mt-4" block @click="updatetable">
                            Create Edge device
                            <font-awesome-icon icon="spinner" v-if="loading" spin/>
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
        <b-row class="mt-2">
            <b-col>
                <b-button class="mt-sm-4" @click="refresh">refresh</b-button>
            </b-col>
            <b-col>
                <b-input-group size="sm" class="mt-sm-4">
                    <b-form-input
                            v-model="filter"
                            type="search"
                            id="filterInput"
                            placeholder="Type to Search"
                    ></b-form-input>
                    <b-input-group-append>
                        <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                    </b-input-group-append>
                </b-input-group>
            </b-col>
        </b-row>
        <b-table :items="items" :fields="headers" striped responsive="true" ref="table" class="mt-4" hover
                 :per-page="perPage"
                 :current-page="currentPage"
                 :filter="filter"
                 @filtered="onFiltered" small>
            <template v-slot:cell(show_details)="row">
                <b-button size="sm" @click="row.toggleDetails" class="mr-2">
                    {{ row.detailsShowing ? 'Hide' : 'Show'}} Details
                </b-button>
            </template>
            <template v-slot:cell(delete)="row">
                <b-button variant="danger" size="sm" @click="remove(row.item.RowKey)">Delete</b-button>
            </template>

            <template v-slot:cell(edit)="row">
                <b-button variant="success" size="sm" @click="edit(row.item.RowKey, row.item.location, row.item.Description, row.item.Name); modalShow = !modalShow">Edit</b-button>
            </template>

            <template v-slot:row-details="row">
                <b-card>
                    <b-row class="mb-2">
                        <b-col sm="3" class="text-sm-right"><b>Description:</b></b-col>
                        <b-col>{{ row.item.Description }}</b-col>
                    </b-row>

                    <b-row class="mb-2">
                        <b-col sm="3" class="text-sm-right"><b>Timestamp:</b></b-col>
                        <b-col>{{ row.item.Timestamp }}</b-col>
                    </b-row>
                </b-card>
            </template>
        </b-table>
        <b-row>
            <b-col>
                <b-pagination style="margin-top: 25px"
                              v-model="currentPage"
                              :total-rows="rows"
                              :per-page="perPage"
                              aria-controls="my-table"
                              pills class="mt-4"
                              :limit="3"

                >
                    <template v-slot:ellipsis-text>
                        <b-spinner small type="grow"></b-spinner>
                    </template>
                    <template v-slot:page="{ page, active }">
                        <b v-if="active">{{ page }}</b>
                        <i v-else>{{ page }}</i>
                    </template>
                </b-pagination>
            </b-col>
        </b-row>
        <b-modal v-model="modalShow" title="edit edgedevice" hide-footer>
            <b-form>
                <b-form-group
                        id="input-group-1"
                        label="Location:"
                        label-for="input-1"
                >
                    <b-form-input
                            id="input-1"
                            v-model="form.location"
                            type="email"
                            required
                            placeholder="Enter location"
                    ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-2" label="Name:" label-for="input-2">
                    <b-form-input
                            id="input-2"
                            v-model="form.name"
                            required
                            placeholder="Enter name"
                    ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-3" label="Description:" label-for="input-3">
                    <b-form-input
                            id="input-3"
                            v-model="form.description"
                            required
                            placeholder="Enter description"
                    ></b-form-input>
                </b-form-group>
                <b-button variant="success" @click=onSubmit>update</b-button>
                <span style="color:red">{{ error_modal }}</span>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
    import EdgeDevice from "../models/EdgeDevice";
    import axios from "axios";

    export default {
        name: "EdgeDevicesTable",
        mounted() {
            const edgemodel = EdgeDevice;
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
            edgemodel.fetchall().then(response => {
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
        },

        computed: {
            rows() {
                return this.items.length
            }
        },
        data() {
            return {
                modalShow: false,
                error_modal: "",
                selected_id: "",
                filter: "",
                perPage: 10,
                currentPage: 1,
                form: {
                    location: '',
                    name: '',
                    description: '',
                },

                selected_edgedevice: "",
                headers: ['id', 'location', 'Name', 'show_details', 'edit', 'delete'],
                error: "",
                loading: "",
                Description: "",
                Name: "",
                Location: "",
                items: []
            }
        },

        methods: {
            onSubmit() {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                EdgeDevice.update(this.selected_id, {
                    Location: this.form.location,
                    Name: this.form.name,
                    Description: this.form.description
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
                }).catch((error) => {
                    this.error_modal = error.response.data.data.message;
                })
            },
            createEdgeDevice() {
                this.error = "";
                if (!this.Name || !this.Description || !this.Location){
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
            },

            remove(id) {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                EdgeDevice.delete(id).then(() => {
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
                }).catch((error) => {
                    this.error = error.response.data.data.message;
                })
            },

            edit(id, location, description, name) {
                this.form.location = location
                this.form.name = description
                this.form.description = name
                this.selected_id = id
            },

            updatetable() {
                this.createEdgeDevice();
            },
            onFiltered(filteredItems) {
                // Trigger pagination to update the number of buttons/pages due to filtering
                this.totalRows = filteredItems.length
                this.currentPage = 1
            },
            refresh(){
                const edgemodel = EdgeDevice;
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                edgemodel.fetchall().then(response => {
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
            }
        }
    }
</script>

<style scoped>

</style>