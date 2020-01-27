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
                            v-model="create_device.name"
                    >
                </b-col>
                <b-col>
                    <label class="mb-0 text-dark" for="inputDescription">Description</label>
                    <input
                            type="text"
                            id="inputDescription"
                            class="form-control"
                            v-model="create_device.description"
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
                            v-model="create_device.location"
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
                            v-model="create_device.protocol"
                            minlength="8"
                            required
                    >
                </b-col>
                <b-col>
                    <label class="mb-0 text-dark" for="inputLocation">Edge device</label>
                    <b-form-select v-model="create_device.selected" :options="create_device.options"></b-form-select>
                </b-col>
                <b-col>
                    <b-button class="mt-4" block @click="createSensorDevice">
                        Create Sensors Device
                        <font-awesome-icon icon="spinner" v-if="create_device.loading" spin/>
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
                          @click="edit(row.item.RowKey, row.item.location, row.item.Description, row.item.Name, row.item.Protocol, row.item.EdgeDeviceId); modalShow = !modalShow">
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
                        <b-col>{{ row.item.Protocol }}</b-col>
                    </b-row>

                    <b-row class="mb-2">
                        <b-col sm="3" class="text-sm-right"><b>Edgedevice:</b></b-col>
                        <b-col>{{ create_device.selectorid[row.item.EdgeDeviceId]}}</b-col>
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

                <b-form-group id="input-group-4" label="Edge device:" label-for="input-4">
                    <b-form-select required id="input-4" v-model="form.edgedevice"
                                   :options="create_device.options"></b-form-select>
                </b-form-group>

                <b-form-group id="input-group-5" label="Protocol:" label-for="input-5">
                    <b-form-input
                            id="input-5"
                            v-model="form.protocol"
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
    import EdgeDevice from "../models/EdgeDevice";
    import axios from "axios";
    import SensorsDevice from "../models/SensorsDevice";

    export default {
        name: "SensorDevicesTable",
        beforeCreate() {
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
            EdgeDevice.fetchall().then(response => {
                this.edgedevices = response.data.data.edgedevices.sort(function (a, b) {
                    return a.RowKey - b.RowKey;
                });

                this.create_device.options = []
                this.create_device.selector = {}
                this.create_device.selectorid = {}
                this.edgedevices.forEach(device => {
                    this.create_device.options.push(device.Name)
                    this.create_device.selector[device.Name] = device
                    this.create_device.selectorid[device.RowKey] = device.Name
                })
            })

            SensorsDevice.fetchall().then(response => {
                this.items = response.data.data.sensorsdevices.sort(function (a, b) {
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
                modalShow: false,
                error_modal: "",
                loading: false,
                error: "",
                filter: "",
                perPage: 10,
                currentPage: 1,
                form: {
                    location: '',
                    name: '',
                    description: '',
                    edgedevice: '',
                    protocol: '',
                    id: '',
                },
                headers: ['id', 'location', 'Name', 'show_details', 'edit', 'delete', 'data'],
                items: [],
                edgedevices: [],
                refresh_: {
                    loading: false,
                },
                create_device: {
                    options: [],
                    selector: {},
                    selectorid: {},
                    selected: "",
                    loading: false,
                    protocol: "",
                    location: "",
                    name: "",
                    description: ""
                }
            }
        },
        methods: {
            createSensorDevice() {
                this.error = "";
                if (!this.create_device.protocol || !this.create_device.selected || !this.create_device.location || !this.create_device.name || !this.create_device.description) {
                    this.error = "fill everything"
                }
                if (this.create_device.protocol && this.create_device.selected && this.create_device.location && this.create_device.name && this.create_device.description) {
                    this.create_device.loading = true;
                    axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                    SensorsDevice.create({
                        Protocol: this.create_device.protocol,
                        Name: this.create_device.name,
                        Description: this.create_device.description,
                        Location: this.create_device.location,
                        EdgeDeviceId: this.create_device.selector[this.create_device.selected].RowKey
                    }).then(() => {
                        SensorsDevice.fetchall().then(response => {
                            this.items = response.data.data.sensorsdevices.sort(function (a, b) {
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
                        this.create_device.loading = false;
                    }).catch((error) => {
                        this.create_device.loading = false;
                        this.error = error.response.data.message;
                    })
                }
            },

            onSubmit() {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                SensorsDevice.update(this.form.id, {
                    Protocol: this.form.protocol,
                    Name: this.form.name,
                    Description: this.form.description,
                    Location: this.form.location,
                    EdgeDeviceId: this.create_device.selector[this.form.edgedevice].RowKey
                }).then(() => {
                    SensorsDevice.fetchall().then(response => {
                        this.items = response.data.data.sensorsdevices.sort(function (a, b) {
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

            edit(id, location, description, name, protocol, edgedeviceid) {
                this.form.id = id
                this.form.location = location
                this.form.description = description
                this.form.name = name
                this.form.protocol = protocol
                this.form.edgedevice = this.create_device.selectorid[edgedeviceid]
            },

            onFiltered(filteredItems) {
                // Trigger pagination to update the number of buttons/pages due to filtering
                this.totalRows = filteredItems.length
                this.currentPage = 1
            },

            stats(id){
                this.$router.push('/sensordata/sensorsdevice/' + id)
            },

            remove(id) {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                SensorsDevice.delete(id).then(() => {
                    SensorsDevice.fetchall().then(response => {
                        this.items = response.data.data.sensorsdevices.sort(function (a, b) {
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

            refresh() {
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
                this.refresh_.loading = true;
                SensorsDevice.fetchall().then(response => {
                    this.items = response.data.data.sensorsdevices.sort(function (a, b) {
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
        },
        computed: {
            rows() {
                return this.items.length
            }
        },
    }
</script>

<style scoped>

</style>