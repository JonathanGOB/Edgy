<template>
    <div>

    </div>
</template>

<script>
    export default {
        name: "Logout",
        created() {
            this.$store.dispatch('logout').then(() => {
                this.$router.push('/login')
            }).catch(() => {
                this.$store.dispatch('errorlogout')
            })
        }
    }
</script>

<style scoped>

</style>