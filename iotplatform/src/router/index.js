import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "about" */ '../views/Home.vue')
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue')
  },

  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "login" */ '../views/Register.vue')
  },
  {
    path: '/edgedevices',
    name: 'edgedevices',
    component: () => import(/* webpackChunkName: "login" */ '../views/Edgedevices.vue')
  },
  {
    path: '/logout',
    name: 'logout',
    component: () => import(/* webpackChunkName: "login" */ '../views/Logout.vue')
  },
  {
    path: '/sensorsdevices',
    name: 'sensorsdevices',
    component: () => import(/* webpackChunkName: "login" */ '../views/SensorsDevices.vue')
  },
  {
    path: '/sensors',
    name: 'sensors',
    component: () => import(/* webpackChunkName: "login" */ '../views/Sensors.vue')
  },
  {
    path: '/sensordata',
    name: 'sensordata',
    component: () => import(/* webpackChunkName: "login" */ '../views/Sensordata.vue')
  },
  {
    path: '/account',
    name: 'account',
    component: () => import(/* webpackChunkName: "login" */ '../views/Account.vue')
  }
]

const router = new VueRouter({
  routes,
  mode: 'history',
  linkActiveClass: "active",
  linkExactActiveClass: "exact-active",

})

export default router
