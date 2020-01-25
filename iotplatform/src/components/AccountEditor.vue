<template>
    <div>
        <b-row class="mt-3">
            <b-col>
                <h1 class="display-5"> Hello {{this.$store.getters.user.name}} </h1>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-form @change="change" v-if="loaded">
                    <b-form-group
                            id="input-group-1"
                            label="Email address:"
                            label-for="input-1"
                            description="change email."
                    >
                        <b-form-input
                                id="input-1"
                                v-model="form.email"
                                type="email"
                                required
                                placeholder="Enter email"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group
                            id="input-group-2"
                            label="Name:"
                            label-for="input-2"
                            description="change name."
                    >
                        <b-form-input
                                id="input-2"
                                v-model="form.name"
                                type="text"
                                required
                                placeholder="Enter name"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group
                            id="input-group-3"
                            label="Password:"
                            label-for="input-3"
                            description="enter your current password."
                    >
                        <b-form-input
                                id="input-3"
                                v-model="form.password"
                                type="password"
                                required
                                placeholder="Enter password"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group
                            id="input-group-4"
                            label="password:"
                            label-for="input-4"
                            description="enter your new password."
                    >
                        <b-form-input
                                id="input-4"
                                v-model="form.newpassword"
                                type="password"
                                required
                                placeholder="Enter password"
                        ></b-form-input>
                    </b-form-group>
                    <b-button type="change" variant="primary">change</b-button>
                </b-form>
            </b-col>
        </b-row>
    </div>
</template>

<script>
    import User from "../models/User";
    import axios from "axios";

    export default {
        name: "AccountEditor",
        created() {
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + this.$store.state.token;
            User.fetchall().then(response => {
                this.form.name = response.data.data.user.name
                this.form.email = response.data.data.user.email
            }).then(() => {
                this.loaded = true
            })
        },

        data() {
            return {
                loaded: false,
                form: {
                    name: "",
                    email: "",
                    password: "",
                    newpassword: ""
                }
            }
        },

        methods:{
            change(){
                
            }
        }
    }
</script>

<style scoped>

</style>