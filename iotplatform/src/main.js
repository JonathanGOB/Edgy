import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VeeValidate from 'vee-validate';
import {library} from "@fortawesome/fontawesome-svg-core";
import {
    faUserSecret,
    faAlignJustify,
    faSearch,
    faAngleLeft,
    faUser,
    faSpinner,
    faEye,
    faTrashAlt,
    faBars,
    faShoppingCart,
    faStar,
    faStarHalf,
    faChevronLeft,
    faHome,
    faHeart,
    faTrash,
    faChevronCircleRight,
    faChevronCircleLeft,
    faWallet,
    faSignOutAlt,
    faCog,
    faStore,
    faComments,
    faCoins,
    faFileInvoice,
    faSuitcase,
} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import VueGoogleCharts from 'vue-google-charts'

Vue.config.productionTip = false
Vue.use(VueGoogleCharts)

library.add(faUserSecret, faAlignJustify, faSearch, faAngleLeft, faUser, faSpinner, faEye, faTrashAlt, faBars, faShoppingCart, faStar, faStarHalf, faChevronLeft, faHome, faHeart, faTrash, faChevronCircleRight, faChevronCircleLeft, faWallet, faSignOutAlt, faCog, faStore, faComments, faCoins, faFileInvoice, faSuitcase);
Vue.component("font-awesome-icon", FontAwesomeIcon);

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(VeeValidate, { fieldsBagName: 'veeFields' });

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
