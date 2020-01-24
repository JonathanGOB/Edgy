<template>
    <div>
        <b-container>
        <b-row class="d-flex flex-column-reverse align-items-center">
            <h1 class="display-3"> Edgedevices </h1>
        </b-row>
            <b-row>
                <b-button v-b-modal.modal-1>Create Edge device</b-button>
                <b-modal id="modal-1" title="BootstrapVue">
                    <form @submit.prevent>
                        <div class="form-group">
                            <label class="mb-0" for="inputEmail">Email</label>
                            <input
                                    type="email"
                                    id="inputEmail"
                                    class="form-control"
                                    required
                                    autofocus
                                    v-model="email"
                            >
                        </div>

                        <div class="form-group">
                            <label class="mb-0 text-dark" for="inputPassword">Password</label>
                            <input
                                    type="password"
                                    id="inputPassword"
                                    class="form-control"
                                    v-model="password"
                                    minlength="8"
                                    required
                            >
                        </div>

                        <button type="button" class="btn btn-md btn-primary btn-block mb-3 btn-dark" @click="login">
                            Sign in
                            <font-awesome-icon icon="spinner" v-if="loading" spin/>
                        </button>

                        <div>
                            <span style="color:red">{{ error }}</span>
                        </div>
                    </form>
                </b-modal>
            </b-row>
            <b-table striped hover :items="items"></b-table>
        </b-container>

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