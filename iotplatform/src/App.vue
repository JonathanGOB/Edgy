<template>
    <router-view/>
</template>

<script>

    export default {
        name: 'App',

        components: {},
        computed: {
            logged() {
                return this.$store.getters.user
            }
        },

        watch: {
            // eslint-disable-next-line no-unused-vars
            $route(to, from) {
                if (!this.logged) {
                    if (this.$router.currentRoute.name != "login" && this.$router.currentRoute.name != "register") {
                        this.$router.push('/login')
                    }
                }
            }
        },

        data: () => ({
            //
        }),
    };
</script>
