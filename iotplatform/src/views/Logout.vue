<template>
    <div>

    </div>
</template>

<script>
    export default {
        name: "Logout",
        mounted() {
            this.$store.dispatch('logout').then(() => {
                this.$router.go('/')
            })
        }
    }
</script>

<style scoped>

</style>