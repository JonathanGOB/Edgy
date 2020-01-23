<template>
    <div>
        <div class="vertical-nav bg-white" id="sidebar">
            <div class="py-4 px-3 mb-4 bg-light">
                <div class="media d-flex align-items-center"><img
                        src="https://suzmakelaars.nl/wp-content/uploads/2019/11/user-placeholder-4-e1574089236199.png" alt="..."
                        width="65" class="mr-3 rounded-circle img-thumbnail shadow-sm">
                    <div class="media-body">
                        <h4 class="m-0">{{this.$store.getters.user.name}}</h4>
                        <p class="font-weight-light text-muted mb-0">{{this.$store.getters.user.email}}</p>
                    </div>
                </div>
            </div>

            <p class="text-gray font-weight-bold text-uppercase px-3 small pb-4 mb-0">Account</p>

            <ul class="nav flex-column bg-white mb-0">
                <li v-for="item in items.user" v-bind:key="item.title" class="nav-item">
                    <router-link class="nav-link text-dark font-italic" :to="{name: item.link}" >
                        <v-icon>{{item.icon}}</v-icon> {{item.title}}
                    </router-link>
                </li>
            </ul>

            <p class="text-gray font-weight-bold text-uppercase px-3 small py-4 mb-0">Devices</p>

            <ul class="nav flex-column bg-white mb-0">
                <li v-for="item in items.devices" v-bind:key="item.title" class="nav-item">
                    <router-link class="nav-link text-dark font-italic" :to="{name: item.link}" >
                        <v-icon>{{item.icon}}</v-icon> {{item.title}}
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
        data() {
            return {
                eslint: "",
                items: {
                    devices: [
                        {title: 'EdgeDevices', icon: 'mdi-monitor', link: 'about', },
                        {title: 'Sensorsdevices', icon: 'mdi-minus-network', link: 'about'},
                        {title: 'Sensors', icon: 'mdi-satellite-variant', link: 'about'},
                        {title: 'Sensordata', icon: 'mdi-floppy', link: 'about'},
                        {title: 'Logout', icon: 'mdi-account-key', link: 'about'}
                        ],
                    user: [
                        {title: 'Dashboard', icon: 'mdi-view-dashboard', link: 'about'},
                        {title: 'Account', icon: 'mdi-account-box', link: 'about'}
                    ]
                },
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

    .page-content {
        width: calc(100% - 17rem);
        margin-left: 17rem;
        transition: all 0.4s;
    }

    /* for toggle behavior */

    #sidebar.active {
        margin-left: -17rem;
    }

    #content.active {
        width: 100%;
        margin: 0;
    }

    @media (max-width: 768px) {
        #sidebar {
            margin-left: -17rem;
        }

        #sidebar.active {
            margin-left: 0;
        }

        #content {
            width: 100%;
            margin: 0;
        }

        #content.active {
            margin-left: 17rem;
            width: calc(100% - 17rem);
        }
    }
</style>