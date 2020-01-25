<template>
    <div>
        <Sidebar>

        </Sidebar>
        <b-container fluid>
            <AccountEditor>

            </AccountEditor>
        </b-container>
    </div>
</template>

<script>
    import Sidebar from "../components/Sidebar";
    import AccountEditor from "../components/AccountEditor";
    export default {
        name: "Account",
        components: {AccountEditor, Sidebar},

    }
</script>

<style scoped>

</style>