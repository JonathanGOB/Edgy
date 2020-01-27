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
                            v-model="create.name"
                    >
                </b-col>
                <b-col>
                    <label class="mb-0 text-dark" for="inputDescription">Description</label>
                    <input
                            type="text"
                            id="inputDescription"
                            class="form-control"
                            v-model="create.description"
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
                            v-model="create.location"
                            minlength="8"
                            required
                    >
                </b-col>
                <b-col>
                    <label class="mb-0 text-dark" for="inputDatatype">Datatype</label>
                    <input
                            type="text"
                            id="inputDatatype"
                            class="form-control"
                            v-model="create.datatype"
                            minlength="8"
                            required
                    >
                </b-col>
                <b-col>
                    <label class="mb-0 text-dark" for="inputLocation">Sensorsdevice</label>
                    <b-form-select v-model="create.selected" :options="create.sensorsdeviceoptions"></b-form-select>
                </b-col>
                <b-col>
                    <b-button class="mt-4" block @click="createsensor">
                        Create Sensor
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

        <b-row class="mt-2">
            <b-col>
                <b-button class="mt-sm-4" @click="refresh">
                    <font-awesome-icon icon="spinner" v-if="refresh_.loading" spin/>
                    refresh
                </b-button>
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
                <b-button variant="success" size="sm"
                          @click="edit(row.item.RowKey, row.item.location, row.item.Description, row.item.Name, row.item.Datatype, row.item.SensorsDeviceId); modalShow = !modalShow">
                    Edit
                </b-button>
            </template>

            <template v-slot:cell(data)="row">
                <b-button variant="primary" size="sm"
                          @click="stats(row.item.id); modalShow = !modalShow">
                    Stats
                </b-button>
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

                    <b-row class="mb-2">
                        <b-col sm="3" class="text-sm-right"><b>Protocol:</b></b-col>
                        <b-col>{{ row.item.Datatype }}</b-col>
                    </b-row>

                    <b-row class="mb-2">
                        <b-col sm="3" class="text-sm-right"><b>Sensors device:</b></b-col>
                        <b-col>{{ create.selectorid[row.item.SensorsDeviceId]}}</b-col>
                    </b-row>

                    <b-row class="mb-2">
                        <b-col sm="3" class="text-sm-right"><b>Connectionstring:</b></b-col>
                        <b-col>{{ row.item.ConnectionString}}</b-col>
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

        <b-modal v-model="modalShow" title="edit sensordevice" hide-footer>
            <b-form>
                <b-form-group
                        id="input-group-1"
                        label="Location:"
                        label-for="input-1"
                >
                    <b-form-input
                            id="input-1"
                            v-model="modal.location"
                            type="email"
                            required
                            placeholder="Enter location"
                    ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-2" label="Name:" label-for="input-2">
                    <b-form-input
                            id="input-2"
                            v-model="modal.name"
                            required
                            placeholder="Enter name"
                    ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-3" label="Description:" label-for="input-3">
                    <b-form-input
                            id="input-3"
                            v-model="modal.description"
                            required
                            placeholder="Enter description"
                    ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-4" label="Sensors device:" label-for="input-4">
                    <b-form-select required id="input-4" v-model="modal.sensorsdevice"
                                   :options="create.sensorsdeviceoptions"></b-form-select>
                </b-form-group>

                <b-form-group id="input-group-5" label="Datatype:" label-for="input-5">
                    <b-form-input
                            id="input-5"
                            v-model="modal.datatype"
                            required
                            placeholder="Enter protocol"
                    ></b-form-input>
                </b-form-group>

                <b-button variant="success" @click=onSubmit>update</b-button>
                <span style="color:red">{{ error_modal }}</span>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
    import axios from "axios";
    import SensorsDevice from "../models/SensorsDevice";
    import Sensor from "../models/Sensor";

    export default {
        name: "SensorsTable",
        created() {
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
            SensorsDevice.fetchall().then(response => {
                this.sensorsdevices = response.data.data.sensorsdevices.sort(function (a, b) {
                    return a.RowKey - b.RowKey;
                });

                this.create.sensorsdeviceoptions = []
                this.create.selector = {}
                this.create.selectorid = {}
                this.sensorsdevices.forEach(device => {
                    this.create.sensorsdeviceoptions.push(device.Name)
                    this.create.selector[device.Name] = device
                    this.create.selectorid[device.RowKey] = device.Name
                })
            })

            Sensor.fetchall().then(response => {
                this.items = response.data.data.sensors.sort(function (a, b) {
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

        data() {
            return {
                loading_: false,
                sensorsdevices: [],
                error: "",
                loading: false,

                create: {
                    selectorid: [],
                    selector: [],
                    name: "",
                    description: "",
                    sensorsdeviceoptions: [],
                    datatype: "",
                    location: "",
                    selected: ""
                },

                modal: {
                    id: "",
                    name: "",
                    location: "",
                    description: "",
                    datatype: "",
                    sensorsdevice: ""
                },

                refresh_:{
                    loading: false
                },

                modalShow: false,
                error_modal: "",
                filter: "",
                perPage: 10,
                currentPage: 1,
                headers: ['id', 'location', 'Name', 'show_details', 'edit', 'delete', 'data'],
                items: [],
            }
        },

        computed: {
            rows() {
                return this.items.length
            }
        },


        methods: {
            onFiltered(filteredItems) {
                // Trigger pagination to update the number of buttons/pages due to filtering
                this.totalRows = filteredItems.length
                this.currentPage = 1
            },
            createsensor() {
                this.error = "";
                if (!this.create.name || !this.create.description || !this.create.location || !this.create.datatype || !this.create.selected) {
                    this.error = "fill everything"
                }
                if (this.create.name && this.create.description && this.create.location && this.create.datatype && this.create.selected) {
                    this.loading = true;
                    axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                    Sensor.create({
                        Name: this.create.name,
                        Description: this.create.description,
                        Location: this.create.location,
                        Datatype: this.create.datatype,
                        SensorsDeviceId: this.create.selector[this.create.selected].RowKey
                    }).then(() => {
                        Sensor.fetchall().then(response => {
                            this.items = response.data.data.sensors.sort(function (a, b) {
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
                        this.error = error.response.data.message;
                    })
                }
            },

            edit(id, location, description, name, datatype, sensorsdeviceid) {
                this.modal.id = id
                this.modal.location = location
                this.modal.description = description
                this.modal.name = name
                this.modal.datatype = datatype
                this.modal.sensorsdevice = this.create.selectorid[sensorsdeviceid]

            },

            onSubmit() {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                Sensor.update(this.modal.id, {
                    Name: this.modal.name,
                    Description: this.modal.description,
                    Location: this.modal.location,
                    Datatype: this.modal.datatype,
                    SensorsDeviceId: this.create.selector[this.modal.sensorsdevice].RowKey
                }).then(() => {
                    Sensor.fetchall().then(response => {
                        this.items = response.data.data.sensors.sort(function (a, b) {
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
                }).finally(() => {
                    this.modalShow = false;
                })
            },

            refresh() {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                this.refresh_.loading = true;
                Sensor.fetchall().then(response => {
                    this.items = response.data.data.sensors.sort(function (a, b) {
                        return a.RowKey - b.RowKey;
                    });
                    let id = 0;
                    this.items.forEach(data => {
                        data.id = id
                        data.location = data.PartitionKey
                        id++
                        delete data.PartitionKey
                    })
                    this.refresh_.loading = false;
                    this.$refs.table.refresh();

                }).catch(error => {
                    this.items = []
                    this.error = error
                    this.refresh_.loading = false;
                })
                this.$refs.table.refresh();
            },

            stats(id){
                this.$router.push('/sensordata/sensor/' + id)
            },

            remove(id) {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                Sensor.delete(id).then(() => {
                    Sensor.fetchall().then(response => {
                        this.items = response.data.data.sensors.sort(function (a, b) {
                            return a.RowKey - b.RowKey;
                        });
                        let id = 0;
                        this.items.forEach(data => {
                            data.id = id
                            data.location = data.PartitionKey
                            id++
                            delete data.PartitionKey
                        })
                        this.$refs.table.refresh();

                    }).catch(error => {
                        this.items = []
                        this.error = error
                    })
                    this.$refs.table.refresh();
                })
            }
        }

    }
</script>

<style scoped>

</style>