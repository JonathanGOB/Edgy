<template>
    <b-navbar type="dark" variant="dark">
        <b-navbar-brand>Edgy</b-navbar-brand>
        <b-navbar-nav>
            <div v-for="item in items.devices" v-bind:key="item.title">
                <b-nav-item :to="{ path: item.link }"><v-icon>{{item.icon}}</v-icon>{{item.title}}</b-nav-item>
            </div>
        </b-navbar-nav>
        <div class="ml-auto">
        <b-img v-bind="mainProps" src="https://scontent-frt3-1.xx.fbcdn.net/v/t1.0-9/54424687_1498788586918848_5011177178784595968_n.jpg?_nc_cat=102&_nc_ohc=ZkuHu6xLYW4AX_0o92d&_nc_ht=scontent-frt3-1.xx&oh=842ee679d4bf42e80ec5ac4fd347b728&oe=5ECE75CC" rounded alt="Rounded image" right></b-img>
        <b-navbar-nav>
        <b-nav-item-dropdown v-bind:text=this.$store.getters.user.name>
                <div v-for="item in items.user" v-bind:key="item.title">
                    <b-dropdown-item :to="{ path: item.link }">{{item.title}}</b-dropdown-item>
                </div>
        </b-nav-item-dropdown>
        </b-navbar-nav>
        </div>
    </b-navbar>
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
                items: {
                    devices: [
                        {title: 'Dashboard', icon: 'mdi-view-dashboard', link: '/'},
                        {title: 'EdgeDevices', icon: 'mdi-monitor', link: '/edgedevices',},
                        {title: 'Sensorsdevices', icon: 'mdi-minus-network', link: '/sensorsdevices'},
                        {title: 'Sensors', icon: 'mdi-satellite-variant', link: '/sensors'},
                        {title: 'Sensordata', icon: 'mdi-floppy', link: '/sensordata'},

                    ],
                    user: [
                        {title: 'Account', icon: 'mdi-account-box', link: '/account'},
                        {title: 'Logout', icon: 'mdi-account-key', link: '/logout'}
                    ]
                },
                mainProps: {width: 35, height: 35, class: 'm1' },
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
        transition: all 0.4s;
    }

</style>