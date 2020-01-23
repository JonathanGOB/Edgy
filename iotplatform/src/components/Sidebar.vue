<template>
    <div>
        <slide>
            <span>user: {{this.$store.getters.user.name}}</span>
            <router-link tag="li" to="/login">dashboard</router-link>
            <router-link tag="li" to="/">edgedevices</router-link>
            <router-link tag="li" to="/">sensorsdevices</router-link>
            <router-link tag="li" to="/">sensors</router-link>
            <router-link tag="li" to="/">logout</router-link>
        </slide>
    </div>
</template>

<script>
    import {Slide} from 'vue-burger-menu'

    export default {
        components: {
            Slide // Register your component
        },
        name: "Sidebar",
        data() {
            return {}
        }
    }
</script>

<style scoped>
</style>