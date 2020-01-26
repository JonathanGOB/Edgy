<template>
    <div>
        <b-row>
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
        <b-col>
            <b-table :items="items" :fields="headers" striped responsive="true" ref="table" class="mt-4" hover
                     :per-page="perPage"
                     :current-page="currentPage"
                     :filter="filter"
                     @filtered="onFiltered" small>
<!--                <template v-slot:cell(show_details)="row">-->
<!--                    <b-button size="sm" @click="row.toggleDetails" class="mr-2">-->
<!--                        {{ row.detailsShowing ? 'Hide' : 'Show'}} Details-->
<!--                    </b-button>-->
<!--                </template>-->
            </b-table>
        </b-col>
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
    </div>
</template>

<script>
    export default {
        name: "GraphTable",
        props: ['value', 'device'],
        data() {
            return {
                items: [],
                filter: "",
                perPage: 10,
                currentPage: 1,
                headers: ['id', 'Timestamp', 'Datavalue'],
            }
        },
        methods: {
            calculate(newval) {
                let id = 0
                newval.forEach(sensordata => {
                    sensordata["id"] = id
                    id++
                });

                this.items = newval
            },
            onFiltered(filteredItems) {
                // Trigger pagination to update the number of buttons/pages due to filtering
                this.totalRows = filteredItems.length
                this.currentPage = 1
            },
        },

        watch: {
            value: {
                // eslint-disable-next-line no-unused-vars
                handler(newval, oldval) {
                    this.calculate(newval)
                }
            }
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