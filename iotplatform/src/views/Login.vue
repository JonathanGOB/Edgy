<template>
    <div class="row bg-light">
        <div class="col-12">
            <div class="bg-light vh-100">
                <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
                    <div class="card mt-5 mb-3">
                        <div class="card-body">
                            <h3 class="card-title text-center">Sign in</h3>
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
                                <br>
                                <div class="mt-4 mb-2 small d-flex">
                                    <hr class="w-25 mt-2">
                                    New to this platform?
                                    <hr class="w-25 mt-2">
                                </div>
                                <router-link
                                        :to="{name: 'register'}"
                                        class="btn btn-md btn-block btn-light"
                                >Create your own account
                                </router-link>
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
        name: "Login",
        data() {
            return {
                email: "",
                password: "",
                loading: false,
                error: "",
            }
        },
        created() {
            if(this.$store.getters.user){
                this.$router.push('/')
            }
        },

        computed: {
            user () {
                return this.$store.getters.user
            }
        },
        methods: {
            login() {
                this.error = "";
                this.loading = true;
                this.$store.dispatch('auth', {
                    Email: this.email,
                    Password: this.password
                }).then(() => {
                    this.$store.watch(
                        (getters)=>{
                            return getters.user // could also put a Getter here
                        },
                        // eslint-disable-next-line no-unused-vars
                        (newValue, oldValue)=>{
                            this.$router.push('/').catch(err => {
                                // eslint-disable-next-line no-console
                                console.log(newValue, oldValue, err)
                            })
                        },
                        //Optional Deep if you need it
                        {
                            deep:true
                        }
                    );
                }).catch((error) => {
                    this.error = error.response.data.message;
                    this.loading = false;
                })
            },
        }
    }
</script>

<style scoped>

</style>