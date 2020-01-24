<template>
    <div>
        <div class="vertical-nav bg-white" id="sidebar">
            <div class="py-4 px-3 mb-4 bg-light">
                <div class="media d-flex align-items-center"><img
                        src="https://scontent-frt3-1.xx.fbcdn.net/v/t1.0-9/54424687_1498788586918848_5011177178784595968_n.jpg?_nc_cat=102&_nc_ohc=ZkuHu6xLYW4AX_0o92d&_nc_ht=scontent-frt3-1.xx&oh=842ee679d4bf42e80ec5ac4fd347b728&oe=5ECE75CC"
                        alt="..."
                        width="65" class="mr-3 rounded-circle img-thumbnail shadow-sm">
                    <div class="media-body" v-if="this.$store.getters.user">
                        <h4 class="m-0">{{this.$store.getters.user.name}}</h4>
                        <p class="font-weight-light text-muted mb-0">{{this.$store.getters.user.email}}</p>
                    </div>
                </div>
            </div>

            <p class="text-gray font-weight-bold text-uppercase px-3 small pb-4 mb-0">Account</p>

            <ul class="nav flex-column bg-white mb-0">
                <li v-for="item in items.user" v-bind:key="item.title" class="nav-item">
                    <router-link class="nav-link text-dark font-italic" :to="{name: item.link}">
                        <v-icon>{{item.icon}}</v-icon>
                        {{item.title}}
                    </router-link>
                </li>
            </ul>

            <p class="text-gray font-weight-bold text-uppercase px-3 small py-4 mb-0">Devices</p>

            <ul class="nav flex-column bg-white mb-0">
                <li v-for="item in items.devices" v-bind:key="item.title" class="nav-item">
                    <router-link class="nav-link text-dark font-italic" :to="{name: item.link}">
                        <v-icon>{{item.icon}}</v-icon>
                        {{item.title}}
                    </router-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        components: {},
        name: "Sidebar",
        mounted() {
            if (!this.logged) {
                this.$router.push('/login')
            }
        },
        computed: {
            logged() {
                return this.$store.getters.user
            }
        },
        data() {
            return {
                eslint: "",
                items: {
                    devices: [
                        {title: 'EdgeDevices', icon: 'mdi-monitor', link: 'edgedevices',},
                        {title: 'Sensorsdevices', icon: 'mdi-minus-network', link: 'about'},
                        {title: 'Sensors', icon: 'mdi-satellite-variant', link: 'about'},
                        {title: 'Sensordata', icon: 'mdi-floppy', link: 'about'},
                        {title: 'Logout', icon: 'mdi-account-key', link: 'logout'}
                    ],
                    user: [
                        {title: 'Dashboard', icon: 'mdi-view-dashboard', link: 'home'},
                        {title: 'Account', icon: 'mdi-account-box', link: 'about'}
                    ]
                },
                created: false,
                computed: {}
                ,
            }
        },
    }
</script>

<style scoped>
    /*
*
* ==========================================
* CUSTOM UTIL CLASSES
* ==========================================
*
*/

    .vertical-nav {
        min-width: 17rem;
        width: 17rem;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.4s;
    }

</style>