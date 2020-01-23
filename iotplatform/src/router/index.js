import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
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
  }
]

const router = new VueRouter({
  routes,
  mode: 'history',
  linkActiveClass: "active",
  linkExactActiveClass: "exact-active",

})

export default router
