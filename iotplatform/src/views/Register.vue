<template>
    <div class="row bg-light">
        <div class="col-12">
            <div class="bg-light vh-100">
                <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
                    <div class="card mt-5 mb-3">
                        <div class="card-body">
                            <h3 class="card-title text-center">Register your own account</h3>
                            <form @submit.prevent>
                                <div class="form-group">
                                    <label class="mb-0" for="inputName">Name</label>
                                    <input
                                            type="name"
                                            id="inputName"
                                            class="form-control"
                                            required
                                            autofocus
                                            v-model="name"
                                    >
                                </div>
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

                                <button class="btn btn-md btn-primary btn-block mb-3 btn-dark" @click="login">
                                    register you account
                                    <font-awesome-icon icon="spinner" v-if="loading" spin/>
                                </button>

                                <div>
                                    <span style="color:red">{{ error }}</span>
                                </div>
                                <br>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                email: "",
                name: "",
                password: "",
                loading: false,
                error: "",
            }
        },
        name: "Register",
            methods:{
            login() {

            },
        }
    }
</script>

<style scoped>

</style>