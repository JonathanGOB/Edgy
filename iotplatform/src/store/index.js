import Vue from 'vue'
import Vuex from 'vuex'
import User from "../models/User";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: null,
    user: null,
  },
  getters: {
    user: (state) => state.user,
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
